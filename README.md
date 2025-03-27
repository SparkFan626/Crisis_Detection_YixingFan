# Crisis Detection on Reddit - GSoC 2025 Submission

This project includes three tasks focusing on identifying and analyzing crisis-related posts from Reddit. The tasks are implemented using Python and various NLP and data visualization libraries. All scripts are designed to run locally.

---

## 📦 Folder Structure

```
project-folder/
│
├── scripts/                # Python scripts for each task
│   ├── task1_fetch_reddit_posts.py
│   ├── task2_sentiment_risk_analysis.py
│   └── task3_location_mapping.py
│
├── output/                 # Output data and visualizations
│   ├── task1_filtered_reddit_posts.csv
│   ├── task2_sentiment_risk_classified.csv
│   ├── task2_distribution_plot.png
│   └── task3_crisis_heatmap.html
│
├── requirements.txt
├── test_walkthrough.ipynb
└── README.md
```

---

## 📌 Tasks Overview

### ✅ Task 1: Reddit Data Extraction

- **Goal:** Extract Reddit posts related to mental health crises.
- **Approach:**
  - Use `praw` (Reddit API wrapper) to fetch posts from 25+ mental health-related subreddits.
  - Filter posts using a list of predefined crisis-related keywords (e.g. *suicidal*, *panic attack*).
  - Clean the text by removing emojis, punctuation, and stopwords.
- **Output:**
  - `output/task1_filtered_reddit_posts.csv` – Preprocessed dataset of relevant posts.

---

### ✅ Task 2: Sentiment & Risk Classification

- **Goal:** Classify the emotional sentiment and risk level of each post.
- **Approach:**
  - Use `nltk`'s VADER sentiment analyzer to label posts as *Positive*, *Neutral*, or *Negative*.
  - Apply keyword-based classification (with TF-IDF context) to tag posts as:
    - *High-Risk*
    - *Moderate Concern*
    - *Low Concern*
- **Output:**
  - `output/task2_sentiment_risk_classified.csv` – Dataset with added sentiment and risk columns.
  - `output/task2_distribution_plot.png` – Bar chart of sentiment and risk level distribution.

---

### ✅ Task 3: Crisis Geolocation & Visualization

- **Goal:** Visualize regional patterns of distress-related posts on a map.
- **Approach:**
  - Use `spaCy` to extract geographic entities from post content.
  - Use `geopy` to geocode locations into coordinates, filtering only **North American** locations (USA, Canada, Mexico).
  - Filter out non-location terms (e.g., “Netflix”, “Phobia”) using a custom banlist.
  - Generate:
    - A **heatmap** of frequently mentioned regions.
    - **Markers** for the top 5 most mentioned valid locations in North America.
- **Output:**
  - `output/task3_crisis_heatmap.html` – Interactive map showing distress intensity.

---

## 🛠️ How to Run

### 1. 🐍 Python Environment

- Python **3.10** is required  
  Reason: Compatibility with `spaCy`, `scikit-learn`, and `nltk` used in this project.

```bash
python --version
# Make sure output is Python 3.10.x
```

### 2. 🧪 Create and Activate Virtual Environment

```bash
# Create a virtual environment
py -3.10 -m venv env
# Activate it
# Windows:
env\Scripts\activate
# macOS/Linux:
source env/bin/activate
```

### 3. 📦 Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. 🚀 Run the Scripts

```bash
# Task 1: Fetch and clean Reddit posts
python scripts/task1_fetch_reddit_posts.py

# Task 2: Sentiment & risk classification
python scripts/task2_sentiment_risk_analysis.py

# Task 3: Geolocation and heatmap
python scripts/task3_location_mapping.py
```

All output files (CSV, HTML map, and visual plots) will be saved to the `/output/` folder.

---

## 📚 Key Libraries Used

- `praw` - Reddit API access  
- `nltk` - VADER sentiment, stopword removal  
- `emoji` - Remove emojis from text  
- `scikit-learn` - TF-IDF analysis  
- `spaCy` - Named Entity Recognition (NER)  
- `geopy` - Location geocoding  
- `folium` - Interactive maps and heatmaps  
- `matplotlib` / `seaborn` - Data visualization

---

💡 Additionally, a Jupyter Notebook (`test_walkthrough.ipynb`) is included to demonstrate and validate outputs from all three tasks interactively.
## 👨‍💻 Author

- **Name:** Yixing Fan
- **Email:** fanyixing0626@gmail.com  
- **LinkedIn:** [https://www.linkedin.com/in/yixing-spark-fan/](https://www.linkedin.com/in/yixing-spark-fan/)  
- **GitHub:** [https://github.com/SparkFan626](https://github.com/SparkFan626)
- **For GSoC 2025**
