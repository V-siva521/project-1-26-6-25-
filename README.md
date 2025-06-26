# project-1-26-6-25-

## How to Run This Project

### 1. Unzip and Set Up
- Unzip the repository and open a terminal in the project folder.

### 2. (Recommended) Create a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Upgrade pip, setuptools, and wheel
```bash
pip install --upgrade pip setuptools wheel
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

### 5. Download the spaCy English Model
```bash
python -m spacy download en_core_web_sm
```

### 6. Run the Flask Web App
```bash
python app.py
```
- Open your browser and go to [http://localhost:5000](http://localhost:5000)

### 7. (Optional) Use the Notebook
- Open `final.ipynb` in VS Code or Jupyter Lab for interactive exploration and ML experiments.

---

**If you have any issues, make sure your Python version is 3.12 or higher and all dependencies are installed in your virtual environment.**