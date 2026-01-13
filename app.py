"""
BBC News Classifier - Flask Backend
Loads trained model and provides prediction API
"""
from flask import Flask, render_template, request, jsonify
import joblib
import os

app = Flask(__name__)

# Global variables for model and vectorizer
model = None
vectorizer = None

def load_models():
    """
    Load the trained Logistic Regression model and TF-IDF vectorizer
    These were saved during training in train_model.py
    """
    global model, vectorizer
    try:
        model = joblib.load('model/classifier.pkl')
        vectorizer = joblib.load('model/tfidf_vectorizer.pkl')
        print("✓ Models loaded successfully")
        print("  - Classifier: Logistic Regression (8 categories)")
        print("  - Vectorizer: TF-IDF")
    except FileNotFoundError:
        print("⚠ Model files not found. Please run 'python train_model.py' first")
    except Exception as e:
        print(f"⚠ Error loading models: {e}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    text = data.get('text', '')

    if not text:
        return jsonify({'error': 'No text provided'}), 400

    # Transform and predict
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]

    # Get class names
    classes = model.classes_

    return jsonify({
        'prediction': str(pred),
        'confidence': float(max(proba)) * 100,  # Convert to percentage
        'scores': {str(c): float(p) * 100 for c, p in zip(classes, proba)}
    })

if __name__ == '__main__':
    load_models()
    app.run(debug=True)

