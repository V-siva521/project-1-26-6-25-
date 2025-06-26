from flask import Flask, render_template, request, jsonify
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re
import pickle
import os

app = Flask(__name__)

# Load the data
modules_df = pd.read_csv('courses.csv')
qa_df = pd.read_csv('ques_ans.csv')

# Initialize the model components
vectorizer = TfidfVectorizer()
clf = LogisticRegression(max_iter=1000)

def preprocess(text):
    # Convert to lowercase and remove special characters
    text = text.lower()
    text = re.sub(r'[^a-zA-Z\s]', '', text)
    # Split into words and remove common English stop words
    stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once'}
    words = text.split()
    words = [word for word in words if word not in stop_words]
    return " ".join(words)

# Keyword filters
keyword_filters = {
    'supervised': lambda df: df[df['Keywords_Tags_Skills_Interests_Categories']
                                .str.contains('supervised', case=False, na=False)],
    'unsupervised': lambda df: df[df['Keywords_Tags_Skills_Interests_Categories']
                                  .str.contains('unsupervised', case=False, na=False)],
    'beginner': lambda df: df[df['Course_Level'].str.lower() == 'beginner'],
    'intermediate': lambda df: df[df['Course_Level'].str.lower() == 'intermediate'],
    'advanced': lambda df: df[df['Course_Level'].str.lower() == 'advanced'],
}

# Train the model
def train_model():
    modules_df['processed_text'] = modules_df['Module'].astype(str).apply(preprocess)
    X = vectorizer.fit_transform(modules_df['processed_text'])
    y = modules_df['Course_Level']
    clf.fit(X, y)

# Initialize the model
train_model()

def smart_predict(question):
    question_lower = question.lower()
    matched_keywords = [kw for kw in keyword_filters if kw in question_lower]
    
    if matched_keywords:
        df_filtered = modules_df
        for kw in matched_keywords:
            df_filtered = keyword_filters[kw](df_filtered)
        return df_filtered.head().to_dict('records')
    
    question_proc = preprocess(question)
    vec = vectorizer.transform([question_proc])
    predicted_level = clf.predict(vec)[0]
    return modules_df[modules_df['Course_Level'] == predicted_level].head().to_dict('records')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    question = data.get('question', '')
    results = smart_predict(question)
    return jsonify(results)

@app.route('/qa', methods=['POST'])
def get_qa():
    data = request.get_json()
    question = data.get('question', '')
    # Simple keyword matching for Q&A
    matches = qa_df[qa_df['Question'].str.contains(question, case=False, na=False)]
    if not matches.empty:
        return jsonify({'answer': matches.iloc[0]['Answer']})
    return jsonify({'answer': 'I don\'t have a specific answer for that question.'})

if __name__ == '__main__':
    app.run(debug=True)
