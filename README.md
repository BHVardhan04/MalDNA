# 🧬 MalDNA: Advanced DNA-Powered Malware Analysis Platform

Welcome to **MalDNA**, a secure, state-of-the-art malware analysis and threat intelligence platform. MalDNA applies genomic-inspired DNA-based fingerprinting, machine learning, deep learning, and blockchain audit logs to analyze, classify, and track malware mutations and lineages.

---

## 🚀 Key Features

*   **🧬 DNA-Based Fingerprinting:** Converts binary opcodes into DNA-like sequences and computes similarities using genomic algorithms (Levenshtein distance, Cosine similarity, Count Vectorizer, Shannon Entropy).
*   **🧠 Hybrid Analysis Engine:** Integrates static analysis, dynamic analysis, and hybrid heuristic feature extraction.
*   **📊 Interactive Dashboard:** A premium, dark-mode real-time dashboard displaying threat statistics, lineage charts, and recent scans.
*   **🔗 Blockchain Traceability:** Utilizes blockchain concepts/logs to record tamper-proof audit trails for forensic validation.
*   **👾 Malware Mutation Tracking:** Maps lineage and calculates evolutionary distances between malware variants.
*   **🛡️ Multi-Factor Authentication & Rate Limiting:** Enforces JWT-based token security, input validation, and API request throttling.

---

## 📁 Repository Structure

```text
MalDNA-main/
├── backend/                  # Flask RESTful API & Machine Learning Backend
│   ├── app/                  # Main Flask application logic
│   │   ├── controllers/      # Blueprints for user, DNA, threat, blockchain, reports, etc.
│   │   ├── models/           # MongoDB document schemas (user, malware, dna, lineage, etc.)
│   │   ├── schemas/          # Data validation schemas
│   │   ├── services/         # DNA analysis, blockchain auditing, static/dynamic, classification services
│   │   └── utils/            # Logging, security testing, feature extraction utilities
│   ├── ml/                   # Machine learning model definitions & training logic
│   ├── run.py                # Server entry point and CLI commands
│   └── requirements.txt      # Project backend Python package requirements
├── dataset/                  # Malware feature pickles & datasets
└── frontend/                 # Rich responsive web frontend (Vanilla HTML, CSS, JS)
    ├── assets/               # Fonts, icons, and illustrations
    ├── css/                  # Curated styling sheets (dna, reports, lineage, etc.)
    ├── js/                   # Interactive dashboard, lineage, real-time threat, and DNA visualization logic
    ├── pages/                # Admin panels, forensic logs, user portal, threat maps
    ├── docs/                 # Platform documentation markdown files (empty placeholders)
    └── index.html            # Gateway page to the application
```

---

## 🛠️ Tech Stack

*   **Backend:** Python 3.12, Flask, MongoDB (via MongoEngine), Redis (Caching)
*   **Machine Learning:** Scikit-Learn, NumPy, SciPy, Matplotlib, Levenshtein
*   **Frontend:** HTML5, CSS3 (Vanilla responsive layout), JavaScript (Modern ES6+)
*   **Security:** Cryptography, python-jose, flask-jwt-extended, flask-limiter

---

## 📥 Prerequisites & Setup

### 1. Database & Environment
You need to have **MongoDB** and **Redis** installed and running on your local machine.

*   **MongoDB:** Default connection URI is `mongodb://localhost:27017/maldna_db`.
*   **Redis:** Default port `6379`.

### 2. Installation

Clone the repository and install dependencies from the root directory:

```bash
# Install package dependencies
pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the `backend/` directory or root with the following configurations:

```env
FRONTEND_ORIGIN=http://127.0.0.1:8080
MONGODB_URI=mongodb://localhost:27017/maldna_db
DB_NAME=maldna_db
UPLOAD_FOLDER=dataset/
JWT_SECRET_KEY=your-super-secret-key-here
```

---

## 💻 Running the Platform

### Start the Backend Server
Run the Flask server from the `backend/` directory:

```bash
cd backend
python run.py --port 5001 --host 0.0.0.0 --debug
```
*The backend API will be available at `http://127.0.0.1:5001/`.*

### Start the Frontend Client
You can serve the static files in the `frontend/` directory using any HTTP server:

```bash
# Using Python built-in server (runs on port 8080)
cd frontend
python -m http.server 8080
```
*Open `http://127.0.0.1:8080/index.html` in your browser to access the dashboard.*

---

## 🛠️ CLI Utilities

The backend application provides command-line tools for analysis and training:

### 1. Analyze a Malware Sample
Run static, dynamic, and hybrid heuristic analysis on a binary file:
```bash
python run.py cli analyze <file_path>
```

### 2. Train the Machine Learning Classifier
Train models (e.g., Random Forest) from a dataset CSV/pickle:
```bash
python run.py cli train-ml-model --dataset <path_to_dataset> --model random_forest --test_size 0.2
```

### 3. Train the Deep Learning Model
Train deep neural network classification models:
```bash
python run.py cli train-dl
```

---

## 📄 Documentation

Additional system-specific instructions can be found in [frontend/docs/](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/):
*   [Setup_Guide.md](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/Setup_Guide.md)
*   [System_Architecture.md](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/System_Architecture.md)
*   [User_Guide.md](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/User_Guide.md)
*   [API_Documentation.md](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/API_Documentation.md)
*   [Report_Generation.md](file:///c:/Users/HARSHA%20VARDHAN/Personal/MalDNA-main/MalDNA-main/frontend/docs/Report_Generation.md)
