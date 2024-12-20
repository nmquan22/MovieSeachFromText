import os
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from pyvi.ViTokenizer import tokenize

english_stopwords = set(stopwords.words("english"))
# Load and preprocess documents
corpus = []
doc_ids = []
for filename in os.listdir("Data"):
    file_path = os.path.join("Data", filename)
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)
        text = data["Overview"]
        #print(text)
        tokens = word_tokenize(text.lower())
        
        tokens = [PorterStemmer().stem(token) for token in tokens if token not in english_stopwords]
        
        corpus.append(" ".join(tokens))
        doc_ids.append(filename)

# Create TF-IDF vectorizer
vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform(corpus)

# Create index
index = {}
#for token, idx in vectorizer.vocabulary_.items():
    #index[token] = {doc_ids[i]: tfidf_matrix[i, idx] for i in range(len(doc_ids))}
for token, idx in vectorizer.vocabulary_.items():
    index[token] = {doc_ids[i]: tfidf_matrix[i, idx] for i in range(len(doc_ids))}
    #print(token)
# Save to JSON
with open("indexUpdate.json", "w") as f:
    json.dump(index, f)
print(f"Index successfully created and saved to indexUpdate.json")

