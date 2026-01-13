"""
BBC News Classifier - Flask Backend
Loads trained model and provides prediction API
"""

from flask import Flask, render_template, request
import joblib
import os

app = Flask(__name__)

# Load models at startup (IMPORTANT for gunicorn)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

MODEL_PATH = os.path.join(BASE_DIR, "model", "classifier.pkl")
VECTORIZER_PATH = os.path.join(BASE_DIR, "model", "tfidf_vectorizer.pkl")

model = joblib.load(MODEL_PATH)
vectorizer = joblib.load(VECTORIZER_PATH)

print("✓ Models loaded successfully")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    # Get text from HTML form (NOT JSON)
    text = request.form.get("text", "").strip()

    if not text:
        return render_template(
            "index.html",
            error="Please enter some text to classify."
        )

    try:
        X = vectorizer.transform([text])
        prediction = model.predict(X)[0]

        if hasattr(model, "predict_proba"):
            confidence = model.predict_proba(X).max() * 100
            confidence = f"{confidence:.1f}%"
        else:
            confidence = "N/A"

        return render_template(
            "index.html",
            category=prediction.upper(),
            confidence=confidence
        )

    except Exception as e:
        return render_template(
            "index.html",
            error=f"Prediction failed: {str(e)}"
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
