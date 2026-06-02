from flask import Flask, render_template, request, redirect, url_for
import os
import secrets

from modules.hashing import hash_score
from modules.phash import phash_score
from modules.metadata import metadata_score
from modules.ela import ela_score
from modules.sift import sift_score
from modules.cnn import cnn_score
from modules.logger import log_evidence

app = Flask(__name__)
# Secure key no longer used for session state as per user request for statelessness
app.secret_key = "law_enforcement_secure_key_locked_v3"

UPLOAD_FOLDER = "static/uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# In-memory user database for demo purposes
users_db = {'admin': 'admin'}

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = None
    success = None
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if len(password) < 6:
            error = "Password must be at least 6 characters."
        elif username in users_db:
            error = "Username already exists."
        else:
            users_db[username] = password
            # Instantly return perfectly to the login screen with a success banner!
            return render_template('login.html', success="Account created successfully! Please log in.")
            
    return render_template('signup.html', error=error, success=success)


@app.route('/')
def home():
    # Always show login page when visiting the main site
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    if username in users_db and users_db[username] == password:
        # Render the detector immediately without establishing a persistent session
        return render_template('index.html')
    else:
        return render_template('login.html', error="Invalid Credentials. Please try again.")


@app.route('/detect', methods=['POST'])
def detect():
    file = request.files['image']

    if file:
        filename = file.filename.replace(" ", "_")   # avoid space issues
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        # Ensure web-safe display format (Browsers do not support .tif)
        display_filename = filename
        if filename.lower().endswith(('.tif', '.tiff', '.bmp')):
            from PIL import Image
            img = Image.open(filepath)
            display_filename = filename.rsplit('.', 1)[0] + '.jpg'
            img.convert('RGB').save(os.path.join(app.config['UPLOAD_FOLDER'], display_filename), 'JPEG')

        image_path = "uploads/" + display_filename

        # 🔐 HASH
        _, sha256, sha3, blake2b = hash_score(filepath)

        # 🔍 ANALYSIS
        e, ela_image = ela_score(filepath)
        p = phash_score(filepath)
        m = metadata_score(filepath)
        s = sift_score(filepath)
        c = cnn_score(filepath)

        # 🔥 FINAL SCORE (MAXIMUM RULE LOGIC)
        # Using strict maximum rule logic as requested by user.
        # The image is evaluated entirely based on its most suspicious trait.
        
        score = max(e, s, c, p, m)

        # 🎯 DECISION
        if score >= 0.5:
            result = "Tampered ❌"
        else:
            result = "Authentic ✅"

        log_evidence("admin", file.filename, sha256, sha3, blake2b, result)

        return render_template(
            "index.html",
            result=result,
            score=round(score, 3),
            image=image_path,
            ela_image=ela_image,
            ela=round(e, 3),
            phash=round(p, 3),
            metadata=round(m, 3),
            sift=round(s, 3),
            cnn=round(c, 3),
            sha256=sha256,
            sha3=sha3,
            blake2b=blake2b
        )

    return "Error"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
