# Law Enforcement Digital Evidence Tamper Detector
## Basic Project Documentation

### 1. Project Overview
The **Law Enforcement Digital Evidence Tamper Detector** is a specialized digital forensics tool. Its primary purpose is to help investigators determine if digital image evidence has been manipulated, forged, or altered. It uses a combination of deep learning and traditional computer vision algorithms to analyze images, ensuring the integrity of evidence.

### 2. Architecture & Workflow
The application follows a client-server architecture:
- **Frontend**: A web interface built with HTML/CSS where users authenticate and upload image evidence.
- **Backend**: A Python Flask server that handles file uploads, pre-processing, and orchestrates the forensic analysis.
- **Forensic Engine**: A suite of modules that independently analyze the image and return a suspicion score (0 to 1). The application uses a **Strict Maximum Rule Logic**, meaning if taking the maximum score across all modules is $\ge 0.5$, the image is flagged as "Tampered ❌".

### 3. Core Forensic Modules
Each module in the `modules/` directory serves a distinct purpose:

#### a) Error Level Analysis (ELA) - `ela.py`
- **Theory**: Analyzes the compression artifacts in JPEG images. When an image is modified and saved, the modified sections will have a different error level than the untouched sections.
- **Implementation**: It re-saves the image at a known quality level (e.g., 90%) and calculates the absolute difference between the original and the newly saved image. Bright areas in the ELA output indicate higher discrepancies.

#### b) Convolutional Neural Network (CNN) - `cnn.py` & `models/`
- **Theory**: Deep learning models are capable of picking up complex, invisible artifacts of manipulation that traditional algorithms might miss.
- **Implementation**: Uses a pre-trained Keras/TensorFlow model (`model.h5`) that classifies the input image based on spatial features learned from a large dataset of tampered and authentic images.

#### c) Scale-Invariant Feature Transform (SIFT) - `sift.py`
- **Theory**: Primarily used for detecting **copy-move** forgeries. SIFT extracts keypoints that are invariant to scaling and rotation.
- **Implementation**: It extracts features from the image and uses a matching algorithm (like FLANN) to find identical patches within the same image. A high number of robust matches strongly indicates a copy-move forgery.

#### d) Perceptual Hashing (pHash) - `phash.py`
- **Theory**: Generates a signature for an image based on its structural and visual features.
- **Implementation**: Used to determine visual similarity. In forensic contexts, it can be compared against a database of known originals or known forged images.

#### e) Metadata Analysis - `metadata.py`
- **Theory**: EXIF data contains crucial details (camera model, GPS, software). Tampering tools often strip or alter this metadata.
- **Implementation**: Extracts the EXIF data using PIL. If expected structural tags are missing or software manipulation tags (e.g., "Photoshop") are present, the suspicion score increases.

### 4. Integrity and Logging - `hashing.py` & `logger.py`
- **Cryptographic Hashing**: To maintain the "Chain of Custody", every uploaded image is immediately hashed using **SHA-256**, **SHA-3**, and **Blake2b**.
- **Audit Logging**: The final result, timestamp, user (e.g., 'admin'), and cryptographic hashes are written to local log files to ensure that the analysis can be verified later.

### 5. Setup & Execution
The application is thoroughly containerized for isolated execution:
- **Docker**: `docker-compose up --build -d` completely builds the environment, installs `requirements.txt`, and serves the application via Gunicorn.
- **Local**: Python 3.x virtual environment -> `pip install -r requirements.txt` -> `python app.py`.

### 6. Future Scope
- Integration with an actual encrypted relational database (e.g., PostgreSQL) instead of in-memory dictionaries for user management.
- Further expansion of the CNN dataset to handle advanced AI-generated deepfakes (e.g., GANs, Diffusion Models).
