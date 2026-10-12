# EcoSort — AI-Based Waste Classification & Recycling Assistant

A responsive student-project prototype with an HTML/CSS/JavaScript frontend and a Python Flask backend. Users can upload an image and receive a possible waste category, a disposal suggestion, and an eco tip.

## Important project note
This version is a **demo prototype**, not a trained AI image-recognition model. It uses image filename keywords and very simple color heuristics, so its results can be wrong. For a genuine AI project, replace `demo_classify()` in `app.py` with a trained image classifier (for example, a TensorFlow/Keras or PyTorch model trained on a labeled waste dataset). Always follow local waste-disposal rules.

## Requirements
- Python 3.10 or newer
- VS Code (recommended)
- Internet is only needed to install packages; the demo itself runs locally

## Run in VS Code on Windows
1. Extract the ZIP file.
2. Open the extracted `AI_Waste_Classification_Recycling_Assistant` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Run these commands one at a time:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

5. Open this address in your browser: **http://127.0.0.1:5000**
6. To stop the server, click the terminal and press **Ctrl+C**.

### If PowerShell blocks activation
Open a **Command Prompt** terminal in VS Code and run:

```bat
py -m venv .venv
.venv\Scripts\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
python app.py
```

## Features
- Responsive EcoSort web interface
- Image upload, preview, and drag-and-drop
- PNG, JPG, JPEG, and WEBP support; 8 MB upload limit
- Demo categories: Plastic, Paper, Metal, Glass, Organic, E-waste, General
- Recycling guidance and eco tips
- Flask JSON API at `/api/classify`

## Project structure

```text
AI_Waste_Classification_Recycling_Assistant/
├── app.py
├── requirements.txt
├── README.md
├── templates/
│   └── index.html
└── static/
    ├── css/style.css
    ├── js/script.js
    └── uploads/.gitkeep
```
