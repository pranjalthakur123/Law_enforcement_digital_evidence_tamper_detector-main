import cv2
import numpy as np
import tensorflow as tf
import os

MODEL_PATH = "models/cnn_model.h5"
_model = None

def get_model():
    global _model
    if _model is None and os.path.exists(MODEL_PATH):
        try:
            _model = tf.keras.models.load_model(MODEL_PATH)
        except:
            return None
    return _model

def cnn_score(path):
    try:
        model = get_model()
        if model is None:
            return 0.5  # Neutral prediction if model fails to load

        img = cv2.imread(path)
        if img is None:
            return 0
            
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        
        # Rescaling exactly as in training (1./255)
        img = img.astype('float32') / 255.0
        
        # Inference
        prediction = model.predict(np.expand_dims(img, axis=0), verbose=0)
        
        return float(prediction[0][0])
    except Exception as e:
        print("CNN Error:", e)
        return 0