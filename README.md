# Biometric-Authentication-System-Based-on-Heartbeat-Signals-Using-Edge-AI
A biometric authentication system based on heartbeat signals (e.g., ECG/PPG or related signals), featuring a complete pipeline for data acquisition, feature extraction, model training, and real-time inference, designed for Edge AI scenarios (local execution with low latency).

Objective

To build a prototype capable of verifying or identifying users based on their physiological “heartbeat signature,” enabling efficient local recognition suitable for deployment on resource-constrained devices.

Features

Heartbeat signal acquisition via microcontroller (Arduino) and serial communication.

Signal preprocessing and heartbeat feature extraction.

Machine learning model training for authentication.

Real-time authentication using local (edge) inference.

Modular script structure covering the full pipeline (capture → features → training → real-time).

High-Level Architecture

Acquisition (Arduino / sensor → Serial)
The microcontroller reads heartbeat sensor data and transmits samples through a serial interface.

Ingestion and Storage (Python)
Serial data is received and stored as raw datasets for labeling and processing.

Feature Extraction
Signal cleaning, windowing/segmentation, and extraction of temporal and/or frequency-domain features.

Model Training
Supervised training using user-labeled data and export of the trained model.

Real-Time Authentication
Live signal input is processed and classified to accept or reject a user.

Requirements

Python 3.9+ (recommended)

Typical dependencies (indicative):

numpy, scipy, pandas

scikit-learn

pyserial

(optional) matplotlib for visualization

Arduino IDE (or PlatformIO) to upload firmware to the microcontroller

Note: Exact dependencies may vary. Adding a requirements.txt file is recommended.

Installation

Clone the repository and create a virtual environment:

git clone https://github.com/lucaceppi/Biometric-Authentication-System-Based-on-Heartbeat-Signals-Using-Edge-AI.git
cd Biometric-Authentication-System-Based-on-Heartbeat-Signals-Using-Edge-AI

python -m venv .venv
# Linux/Mac
source .venv/bin/activate
# Windows
# .venv\Scripts\activate

pip install -r requirements.txt


If requirements.txt is not available, install dependencies manually:

pip install numpy scipy pandas scikit-learn pyserial matplotlib

Usage
1) Arduino Firmware

Open the Arudino code/ folder.

Compile and upload the sketch to your board.

Verify through the Serial Monitor that data is transmitted in a stable format (one sample per line or simple CSV).

Important: take note of the serial port (e.g., COM3 or /dev/ttyUSB0) and baud rate.

2) Signal Acquisition (Serial → Dataset)

Data capture script:

collect_seril.py

Example execution:

python collect_seril.py --port /dev/ttyUSB0 --baud 115200 --out data/raw/user01_session01.csv


Recommendations:

Record multiple sessions per user (ideally on different days).

Keep acquisition conditions consistent (sensor placement, pressure, posture).

Properly label users and sessions.

3) Feature Extraction

features.py

Example:

python features.py --input data/raw --output data/features --window 4 --overlap 0.5


(Parameters are indicative. Adjust window size and overlap according to signal type and sampling rate.)

4) Model Training

train_model.py

Example:

python train_model.py --data data/features --model_out models/auth_model.pkl


Evaluation suggestions:

Split data by session (train on older sessions, test on newer ones).

Report FAR/FRR/EER for verification tasks, or accuracy/F1-score for identification.

5) Real-Time Authentication

realtime_auth.py

Example:

python realtime_auth.py --port /dev/ttyUSB0 --baud 115200 --model models/auth_model.pkl


Expected output (conceptual):

Window-based decisions: ACCEPT / REJECT (or identified user).

Configurable decision threshold for verification scenarios.

Repository Structure

Arudino code/ — firmware for data acquisition and serial transmission

collect_seril.py — serial data capture

features.py — preprocessing and feature extraction

train_model.py — model training and saving

realtime_auth.py — real-time authentication and inference

Edge AI Considerations

For deployment on edge devices:

Prefer lightweight models (e.g., logistic regression, linear SVMs, small trees, compact neural networks).

Minimize computationally expensive features.

Export models to efficient formats if required (e.g., ONNX, TFLite) and apply quantization when possible.

Security, Privacy, and Ethics

Heartbeat signals are sensitive biometric data; avoid storing raw signals unnecessarily.

Anonymize user identifiers and protect datasets (encryption at rest, access control).

Ensure informed consent for any human data collection.

Consider common threats such as replay attacks, synthetic signal injection, data poisoning, and spoofing.

Roadmap (Proposed)

Add requirements.txt or pyproject.toml.

Include additional scripts for:

signal filtering (bandpass, notch, normalization),

heartbeat segmentation (peak detection),

automated FAR/FRR/EER evaluation.

Centralize configuration via YAML/JSON.

Add tests and CI pipeline.

Contributing

Fork the repository

Create a feature branch (feature/my-improvement)

Submit a Pull Request with a clear description of changes

License

Specify the project license here (e.g., MIT, Apache-2.0, GPL-3.0).
If no license exists yet, adding a LICENSE file is strongly recommended.
