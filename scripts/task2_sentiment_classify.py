import pandas as pd
import re
from nltk.sentiment import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
import nltk

# Download VADER lexicon for sentiment analysis
nltk.download('vader_lexicon')

# ========== Step 1: Load cleaned Reddit data ==========
print("📥 Loading preprocessed Reddit posts...")
df = pd.read_csv("output/task1_filtered_reddit_posts.csv")

# ========== Step 2: Sentiment Classification using VADER ==========
print("🔍 Running sentiment analysis (VADER)...")
sia = SentimentIntensityAnalyzer()

def classify_sentiment(text):
    score = sia.polarity_scores(text)['compound']
    if score >= 0.3:
        return "Positive"
    elif score <= -0.3:
        return "Negative"
    else:
        return "Neutral"

df['sentiment'] = df['content'].apply(classify_sentiment)

# ========== Step 3: Risk Level Detection based on keywords ==========
print("🚨 Assessing risk levels using keyword matching...")

# Optional: Use TF-IDF to extract common terms (not used directly here)
tfidf = TfidfVectorizer(max_features=100)
tfidf_matrix = tfidf.fit_transform(df['content'])
feature_names = tfidf.get_feature_names_out()

# Define high-risk keywords for crisis detection
high_risk_keywords = [
    "end it", "no longer", "don’t want to", "suicide", "kill myself", "disappear",
    "can’t go on", "worthless", "give up", "hopeless"
]

# Moderate-risk phrases
def classify_risk(text):
    text_lower = text.lower()
    if any(phrase in text_lower for phrase in high_risk_keywords):
        return "High-Risk"
    elif any(word in text_lower for word in ["feel lost", "need help", "relapse", "panic", "empty", "depressed"]):
        return "Moderate Concern"
    else:
        return "Low Concern"

df['risk_level'] = df['content'].apply(classify_risk)

# ========== Step 4: Save results to CSV ==========
df.to_csv("output/task2_sentiment_risk_classified.csv", index=False)
print("✅ Classification complete. File saved to output/task2_sentiment_risk_classified.csv")

# ========== Step 5: Visualize results ==========
print("📊 Generating bar plots...")
plt.figure(figsize=(10, 4))

plt.subplot(1, 2, 1)
sns.countplot(x='sentiment', data=df)
plt.title("Sentiment Distribution")

plt.subplot(1, 2, 2)
sns.countplot(x='risk_level', data=df, order=["Low Concern", "Moderate Concern", "High-Risk"])
plt.title("Risk Level Distribution")

plt.tight_layout()
plt.savefig("output/task2_distribution_plot.png")
plt.show()
