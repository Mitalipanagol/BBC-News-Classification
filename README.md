# 📰 BBC News Classifier

> **An end-to-end machine learning web application that automatically classifies BBC news articles into 8 categories using Natural Language Processing.**

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.0+-orange.svg)
![Accuracy](https://img.shields.io/badge/Accuracy-81.6%25-brightgreen.svg)

---

## 🎯 What This Project Does

This is a **complete ML pipeline** - from raw data to a deployed web application. It:

1. **Trains** a Logistic Regression model on 32,642+ BBC news articles
2. **Classifies** articles into **8 categories** with **81.6% accuracy**
3. **Deploys** the model as an interactive Flask web app

**Categories:** Business, UK, World, Entertainment, Technology, Health, Science, Sports

---

## 🏗️ How It Works (The Full Pipeline)

```
📊 Data (bbc_news1.csv)
    ↓
🔄 train_model.py
    ├─ Extracts categories from article links
    ├─ Converts text to TF-IDF features (5000 features)
    ├─ Trains Logistic Regression (balanced class weights)
    └─ Saves model → model/classifier.pkl
                  → model/tfidf_vectorizer.pkl
    ↓
🌐 app.py (Flask Backend)
    ├─ Loads saved models
    ├─ Provides /predict API endpoint
    └─ Serves web interface
    ↓
💻 User enters news text → Gets category prediction
```

**Key Technical Decision:** Used `class_weight='balanced'` in Logistic Regression to handle imbalanced categories (some categories have more articles than others).

## 📁 Project Structure

```
bbc-news-classifier/
│
├── 📂 model/                          # Trained models (created by train_model.py)
│   ├── classifier.pkl                 # Logistic Regression model
│   └── tfidf_vectorizer.pkl          # TF-IDF vectorizer
│
├── 📂 templates/
│   └── index.html                     # Web interface
│
├── 📂 static/
│   └── style.css                      # Styling
│
├── 📂 notebooks/                      # (Optional) Jupyter exploration
│   └── exploration.ipynb
│
├── 📄 app.py                          # Flask backend (loads models)
├── 📄 train_model.py                  # Model training script
├── 📄 requirements.txt                # Python dependencies
├── 📄 test_examples.txt               # Sample inputs for testing
├── 📄 .gitignore                      # Excludes dataset from git
└── 📄 README.md                       # This file
```

**Note:** The dataset (`bbc_news1.csv`) is excluded from git due to size. See [Dataset](#-dataset) section below.

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- BBC News dataset (`bbc_news1.csv`) - see [Dataset](#-dataset) section

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Train the Model
```bash
python train_model.py
```

**What happens:**
- Loads `bbc_news1.csv` (32,642+ articles)
- Extracts 8 categories from article links
- Trains Logistic Regression with TF-IDF features
- Saves models to `model/` folder
- **Output:** `classifier.pkl` and `tfidf_vectorizer.pkl`

**Expected output:**
```
Training with 8 Categories...
Total articles: 32,642
Accuracy: 81.6%
✓ Models saved
```

### Step 3: Run the Web Application
```bash
python app.py
```

**What happens:**
- Loads `model/classifier.pkl` and `model/tfidf_vectorizer.pkl`
- Starts Flask server on `http://localhost:5000`
- Provides web interface for predictions

### Step 4: Use the App
1. Open browser → `http://localhost:5000`
2. Enter news article text
3. Click "Classify"
4. Get predicted category!

**Example:**
```
Input: "Apple shares surge after record iPhone sales..."
Output: Business (Confidence: 92%)
```

---

## 🧠 Technical Details

### Model Architecture

| Component | Specification | Details |
|-----------|--------------|---------|
| **Algorithm** | Logistic Regression | Multi-class classification (one-vs-rest) |
| **Vectorization** | TF-IDF | 5000 max features, English stop words removed |
| **Class Balancing** | `class_weight='balanced'` | Handles imbalanced categories |
| **Training Split** | 80/20 | 26,113 train / 6,529 test articles |
| **Random State** | 42 | Ensures reproducibility |
| **Max Iterations** | 1000 | Convergence parameter |
| **Solver** | lbfgs | Default solver for multi-class |

### Accuracy Measurement
- **Metric:** Classification accuracy on held-out test set (20% of data)
- **Validation:** Stratified split maintains category distribution
- **Evaluation:** Precision, Recall, F1-Score per category
- **Overall Accuracy:** 81.6% across all 8 categories

### Why These Choices?

**1. Logistic Regression over Deep Learning:**
- ✅ Fast training (~10 seconds vs hours)
- ✅ Interpretable results
- ✅ Excellent for text classification with TF-IDF
- ✅ No GPU required

**2. Balanced Class Weights:**
- Problem: Some categories have 8,000+ articles, others have <500
- Solution: `class_weight='balanced'` gives more weight to minority classes
- Result: Better recall for Health (76%), Science (75%), Technology (62%)

**3. TF-IDF over Word Embeddings:**
- ✅ Simpler, faster
- ✅ Works well for news classification
- ✅ No pre-trained models needed

## 📊 Model Performance

| Category      | Precision | Recall | F1-Score | Training Articles |
|---------------|-----------|--------|----------|-------------------|
| Sports        | 95%       | 95%    | 95%      | 8,395            |
| World         | 88%       | 81%    | 84%      | 8,385            |
| UK            | 85%       | 72%    | 78%      | 9,670            |
| Business      | 69%       | 80%    | 74%      | 2,646            |
| Entertainment | 61%       | 82%    | 70%      | 1,865            |
| Health        | 53%       | 76%    | 62%      | 688              |
| Science       | 43%       | 75%    | 54%      | 563              |
| Technology    | 38%       | 62%    | 47%      | 430              |

**Overall Accuracy: 81.6%**

### Key Features:
- ✅ **Balanced Class Weights**: Prevents bias toward categories with more training data
- ✅ **High Recall for Minority Classes**: Health (76%), Science (75%), Technology (62%)
- ✅ **Excellent Sports Classification**: 95% F1-score (largest category)

---

## 📊 Dataset

### Source
BBC News dataset containing 32,642+ articles with:
- **Title:** Article headline
- **Description:** Article summary
- **Link:** URL (used to extract category)

### Category Extraction
Categories are extracted from article URLs:
```python
# Example: /news/business/article-123 → "business"
# Example: /news/uk-england-london-456 → "uk"
```

### Distribution
| Category      | Articles | Percentage |
|---------------|----------|------------|
| Sports        | 8,395    | 25.7%      |
| World         | 8,385    | 25.7%      |
| UK            | 9,670    | 29.6%      |
| Business      | 2,646    | 8.1%       |
| Entertainment | 1,865    | 5.7%       |
| Health        | 688      | 2.1%       |
| Science       | 563      | 1.7%       |
| Technology    | 430      | 1.3%       |

**Note:** Dataset is **imbalanced** - this is why we use `class_weight='balanced'`

### Getting the Dataset

**⚠️ Important:** The dataset (`bbc_news1.csv`) is **not included** in this repository due to file size (>100MB).

#### **Option 1: Download from Kaggle (Recommended)**
```bash
# Visit: https://www.kaggle.com/datasets/hgultekin/bbcnewsarchive
# Or search "BBC News Archive" on Kaggle
# Download and place in project root as bbc_news1.csv
```

#### **Option 2: Use Alternative BBC Dataset**
- [BBC News Classification Dataset](https://www.kaggle.com/c/learn-ai-bbc/data)
- [BBC Full Text Document Classification](https://www.kaggle.com/datasets/shivamkushwaha/bbc-full-text-document-classification)

#### **Option 3: Create Your Own**
Scrape BBC News (ensure compliance with BBC's terms of service):
```python
# Example structure needed:
# title, description, link
# "Apple shares rise", "Tech giant reports...", "/news/business/article-123"
```

**Expected Format:**
```csv
title,description,link
"Article Title","Article description","/news/category/article-id"
```

---

## 🖼️ Screenshots

### Web Interface
![Web Interface](screenshots/interface.png)
*Clean, user-friendly interface for news classification*

### Prediction Example
![Prediction Example](screenshots/prediction.png)
*Real-time classification with confidence scores*

**Note:** Screenshots folder not included in repository. To add your own:
1. Run the app: `python app.py`
2. Take screenshots of the interface
3. Create `screenshots/` folder
4. Add images: `interface.png`, `prediction.png`

---

## 🧪 Example Usage

### Try These Sample Inputs

See `test_examples.txt` for more examples, or try these:

**Business:**
```
Apple shares surge after record iPhone sales. The tech giant reported quarterly
earnings that beat analyst expectations, with revenue up 15% year-over-year.
```
→ Predicted: **Business** (92% confidence)

**Health:**
```
Mental health services face unprecedented demand post-pandemic. Therapists report
waiting lists of up to six months as anxiety and depression cases surge.
```
→ Predicted: **Health** (88% confidence)

**Sports:**
```
Manchester United signs star striker for record fee. The Premier League club paid
£100 million to secure the Brazilian forward.
```
→ Predicted: **Sports** (95% confidence)

**Technology:**
```
Google unveils new AI chatbot to compete with ChatGPT. The search giant announced
its latest artificial intelligence tool at a developer conference.
```
→ Predicted: **Technology** (85% confidence)

---

## 🛠️ Technologies Used

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **ML Framework** | scikit-learn | Model training & prediction |
| **Vectorization** | TF-IDF | Text → numerical features |
| **Backend** | Flask | Web server & API |
| **Frontend** | HTML/CSS/JavaScript | User interface |
| **Model Storage** | joblib | Save/load trained models |

---

## 🎯 What Makes This Project Stand Out

### 1. **Real-World Problem**
- Not a toy dataset (32,642 articles)
- Handles imbalanced classes (realistic scenario)
- Production-ready web interface

### 2. **Complete Pipeline**
```
Data → Training → Model → Backend → Frontend → User
```
Not just a Jupyter notebook - full deployment!

### 3. **Technical Decisions Explained**
- Why Logistic Regression? (Fast, interpretable, effective)
- Why balanced weights? (Handles imbalanced data)
- Why TF-IDF? (Works well for text classification)

### 4. **Clean Code Structure**
- Separate training script
- Modular Flask app
- Clear documentation
- Professional naming

---

---

## 🌐 Deployment

### Deploy to Cloud (Optional)

This app can be deployed to various platforms:

#### **Option 1: Render (Recommended - Free)**
```bash
# 1. Create render.yaml:
services:
  - type: web
    name: bbc-news-classifier
    env: python
    buildCommand: "pip install -r requirements.txt"
    startCommand: "python app.py"

# 2. Push to GitHub
# 3. Connect to Render.com
# 4. Deploy!
```

#### **Option 2: Heroku**
```bash
# 1. Create Procfile:
web: python app.py

# 2. Deploy:
heroku create bbc-news-classifier
git push heroku main
```

#### **Option 3: Railway**
```bash
# 1. Push to GitHub
# 2. Import to Railway.app
# 3. Auto-deploys!
```

#### **Option 4: AWS/GCP/Azure**
- Use EC2/Compute Engine/App Service
- Install dependencies
- Run `python app.py`
- Configure security groups/firewall

**Note:** For production deployment:
- Set `debug=False` in `app.py`
- Use production WSGI server (gunicorn)
- Add environment variables for sensitive data
- Enable HTTPS

---

## 📈 Future Improvements

- [ ] Add confidence threshold filtering
- [ ] Deploy to cloud (see [Deployment](#-deployment) section)
- [ ] Add more categories (e.g., Politics, Environment)
- [ ] Implement A/B testing for different models
- [ ] Add user feedback loop for continuous improvement
- [ ] Create REST API documentation (Swagger/OpenAPI)
- [ ] Add model versioning and experiment tracking (MLflow)

---

## 🤝 Contributing

This is a portfolio project, but suggestions are welcome!

---

## 📧 Contact

**Built by:** Mitali P.A
**LinkedIn:** https://www.linkedin.com/in/mitali-anagolkar/
**Email:** mitalipanagol@gmail.com

---

## 📄 License

This project is open source and available under the MIT License.

---

*Built with Python, scikit-learn, and Flask | 2024*

