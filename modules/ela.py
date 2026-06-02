from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import os

def ela_score(path):
    try:
        original = Image.open(path).convert('RGB')

        filename = os.path.basename(path)
        ela_filename = "ela_" + filename.rsplit('.', 1)[0] + ".jpg"

        temp_path = "static/uploads/temp.jpg"
        ela_full_path = "static/uploads/" + ela_filename

        # Resave at fixed quality to induce compression error difference
        original.save(temp_path, 'JPEG', quality=85)
        compressed = Image.open(temp_path)

        # Calculate difference
        diff = ImageChops.difference(original, compressed)
        diff_np = np.array(diff)
        
        # Convert to grayscale to evaluate intensity anomalies
        gray_diff = np.mean(diff_np, axis=2)
        
        # Anomaly Detection: Compare high error regions (p99) to background median error (p50)
        flattened = gray_diff.flatten()
        max_err = np.percentile(flattened, 99)
        median_err = np.percentile(flattened, 50)
        
        # True tampering usually has a spike in max error compared to background error
        ratio = max_err / (median_err + 1e-5)
        
        # An anomaly ratio > 15 is highly suspicious
        score = min(ratio / 15.0, 1.0)

        # Normalization for visual ELA image output
        scale = 255.0 / (np.max(diff_np) + 1)
        diff = ImageEnhance.Brightness(diff).enhance(scale)

        diff.save(ela_full_path, "JPEG")

        return score, "uploads/" + ela_filename
    except Exception as e:
        print("ELA Error:", e)
        filename = os.path.basename(path)
        ela_filename = "ela_" + filename.rsplit('.', 1)[0] + ".jpg"
        return 0.0, "uploads/" + ela_filename