# Law Enforcement Digital Evidence Tamper Detector 🕵️‍♂️🔍

A comprehensive web-based application designed for law enforcement agencies to analyze digital image evidence and detect potential tampering or forgery. The application utilizes a suite of advanced forensic techniques and cryptographic hashing to ensure the integrity and authenticity of digital evidence.

## 🌟 Features

- **Multi-layered Forensic Analysis**: Evaluates images using multiple detection algorithms:
  - **ELA (Error Level Analysis)**: Detects areas of an image that have different compression levels, highlighting potential digital alterations.
  - **CNN (Convolutional Neural Network)**: Deep learning model trained to identify tampering artifacts.
  - **SIFT (Scale-Invariant Feature Transform)**: Detects copy-move forgeries by matching keypoints within the image.
  - **pHash (Perceptual Hashing)**: Analyzes structural similarities visually.
  - **Metadata Analysis**: Exposes stripping or modification of EXIF data.
- **Strict Maximum Rule Logic**: Classifies an image as "Tampered ❌" if the most suspicious trait detected by *any* of the forensic methods exceeds the predefined threshold (>= 0.5).
- **Cryptographic Evidence Tracking**: Automatically generates SHA256, SHA3, and Blake2b hashes for every uploaded evidence file.
- **Secure Audit Logging**: Maintains a tamper-proof log of all analyses including timestamps, hashes, and final decisions.
- **Web-safe Format Handling**: Automatically converts non-web-friendly formats (like `.tif` and `.bmp`) for seamless browser viewing without altering the original analysis.

## 🛠️ Technology Stack

- **Backend**: Python, Flask, Gunicorn
- **Computer Vision & Machine Learning**: OpenCV, TensorFlow, Scikit-learn, Pillow, ImageHash
- **Deployment**: Docker, Docker Compose

## 🚀 Getting Started

### Prerequisites
Make sure you have [Docker](https://docs.docker.com/get-docker/) installed on your machine.

### Installation & Deployment

1. **Clone the repository**
   ```bash
   git clone https://github.com/Namrata226/Law_enforcement_digital_evidence_tamper_detector.git
   cd Law_enforcement_digital_evidence_tamper_detector
