"""
BBC News Classifier - Model Training Script

This script:
1. Loads BBC news dataset (bbc_news1.csv)
2. Extracts 8 categories from article links
3. Trains a Logistic Regression model with TF-IDF features
4. Saves the trained model and vectorizer to model/ folder

Categories: Business, UK, World, Entertainment, Technology, Health, Science, Sports
Accuracy: ~82% on test set
"""
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
import re

print("=" * 60)
print("BBC News Classifier - Training Script")
print("=" * 60)
print("\n📊 Training with 8 Categories:")
print("   Business, UK, World, Entertainment, Technology,")
print("   Health, Science, Sports\n")

# Load data
df = pd.read_csv('bbc_news1.csv')
df.dropna(inplace=True)

# Combine text
df['text'] = df['title'] + " " + df['description']

# Extract category from link
def extract_category(link):
    if pd.isna(link):
        return 'other'
    link = str(link).lower()

    # Check for specific categories in order of priority
    if '/entertainment' in link or '/arts' in link:
        return 'entertainment'
    elif '/technology' in link or '/tech' in link:
        return 'technology'
    elif '/health' in link:
        return 'health'
    elif '/science' in link or '/environment' in link:
        return 'science'
    elif '/sport' in link:
        return 'sports'
    elif '/business' in link:
        return 'business'
    elif '/uk' in link:
        return 'uk'
    elif '/world' in link:
        return 'world'
    else:
        return 'other'

df['category'] = df['link'].apply(extract_category)

# Filter to only our 8 main categories
categories = ['business', 'uk', 'world', 'entertainment', 'technology', 'health', 'science', 'sports']
df = df[df['category'].isin(categories)]

print("Dataset distribution:")
print(df['category'].value_counts())
print(f"\n📈 Total articles: {len(df)}\n")

# Step 1: Split data into training (80%) and test (20%) sets
print("🔄 Splitting data...")
X = df['text']
y = df['category']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"   Training: {len(X_train)} articles")
print(f"   Testing: {len(X_test)} articles\n")

# Step 2: Convert text to TF-IDF features
print("🔤 Vectorizing text with TF-IDF...")
vectorizer = TfidfVectorizer(stop_words='english', max_features=5000)
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)
print(f"   Features: {X_train_tfidf.shape[1]}\n")

# Step 3: Train Logistic Regression model
# Using balanced class weights to handle imbalanced categories
print("🤖 Training Logistic Regression model...")
print("   (Using balanced class weights for imbalanced data)")
model = LogisticRegression(max_iter=1000, class_weight='balanced')
model.fit(X_train_tfidf, y_train)
print("   ✓ Training complete\n")

# Step 4: Evaluate model performance
print("📊 Evaluating model...")
y_pred = model.predict(X_test_tfidf)
accuracy = accuracy_score(y_test, y_pred)
print(f"   Accuracy: {accuracy*100:.2f}%\n")
print("📋 Detailed Classification Report:")
print(classification_report(y_test, y_pred))

# Step 5: Save trained model and vectorizer
print("\n💾 Saving models...")
os.makedirs('model', exist_ok=True)
joblib.dump(model, 'model/classifier.pkl')
joblib.dump(vectorizer, 'model/tfidf_vectorizer.pkl')

print("   ✓ Model saved to: model/classifier.pkl")
print("   ✓ Vectorizer saved to: model/tfidf_vectorizer.pkl")

print("\n" + "=" * 60)
print("✅ TRAINING COMPLETE!")
print("=" * 60)
print(f"\n📊 Final Accuracy: {accuracy*100:.2f}%")
print("\n🚀 Next steps:")
print("   1. Run 'python app.py' to start the web application")
print("   2. Open http://localhost:5000 in your browser")
print("   3. Try classifying some news articles!")
print("\n" + "=" * 60)

