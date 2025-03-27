import praw
import pandas as pd
import re
import nltk
import emoji
import os
from nltk.corpus import stopwords

# ========== Step 1: Download NLTK stopwords ==========
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# ========== Step 2: Set up Reddit API client ==========
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT"),
    username=os.getenv("REDDIT_USERNAME"),
    password=os.getenv("REDDIT_PASSWORD")
)

# ========== Step 3: Define keywords and subreddits ==========
keywords = [
    "depressed", "suicidal", "addiction help", "mental breakdown", "self harm",
    "overwhelmed", "relapse", "panic attack", "feel hopeless", "i want to die",
    "lost will", "crying all night", "emotional numbness", "can't go on", "need therapy"
]

subreddits = [
    # Primary mental health and crisis support
    "depression", "SuicideWatch", "mentalhealth", "Anxiety", "addiction", "offmychest",
    "sad", "mentalillness", "PTSD", "BPD", "depersonalization", "lonely", "grief", "socialanxiety",
    
    # Additional mental health support
    "CPTSD", "traumatoolbox", "depression_help", "anxietyhelp", "OCD", "ADHD", "bipolar",
    "bipolarreddit", "depressionregimens", "mentalhealthsupport", "mentalhealthuk",
]

posts_data = []

# ========== Step 4: Fetch and filter Reddit posts ==========
for subreddit in subreddits:
    print(f"📥 Fetching from r/{subreddit} ...")
    try:
        for post in reddit.subreddit(subreddit).hot(limit=200):
            content = (post.title or "") + " " + (post.selftext or "")
            
            if any(kw in content.lower() for kw in keywords):
                # ========== Step 5: Preprocess text ==========
                clean_text = content.lower()
                clean_text = emoji.replace_emoji(clean_text, replace="")  # Remove emojis
                clean_text = re.sub(r'[^\w\s]', '', clean_text)          # Remove punctuation
                clean_text = ' '.join(word for word in clean_text.split() if word not in stop_words)

                # ========== Step 6: Store matched post ==========
                posts_data.append({
                    "post_id": post.id,
                    "timestamp": post.created_utc,
                    "content": clean_text,
                    "upvotes": post.score,
                    "comments": post.num_comments,
                    "url": post.url
                })
    except Exception as e:
        print(f"⚠️ Skipped r/{subreddit} due to error: {e}")

# ========== Step 7: Save results to CSV ==========
df = pd.DataFrame(posts_data)
df.to_csv("output/task1_filtered_reddit_posts.csv", index=False)
print(f"✅ Successfully saved {len(df)} posts to output/task1_filtered_reddit_posts.csv")
