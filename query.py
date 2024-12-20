import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import os
import json
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


english_stopwords = set(stopwords.words("english"))
def compute_df(index):
    df = {}
    for term, docs in index.items():
        # Count documents where score > 0
        df[term] = sum(1 for score in docs.values() if score > 0)
    return df

def compute_tf_idf(term, query_tokens, index,df):
    N = len(set(doc_id for docs in index.values() for doc_id in docs))
    # Term Frequency
    tf = query_tokens.count(term) / len(query_tokens)
    print(f"tf:{tf}")
    # Inverse Document Frequency
    
    print(f"Number of document content{df[term]}")
    idf = np.log((N / (1 + df[term])))  
    print(f"idf{idf}")
    print("Total number of documents")
    print(N)
    return tf * idf

def search(query, index_file="indexUpdate.json", top_k=12):
    # Load index
    with open(index_file, "r", encoding="utf-8") as file:
        index = json.load(file)
    
    # Process query
    tokens = word_tokenize(query.lower())
    tokens = [PorterStemmer().stem(token) for token in tokens if token not in english_stopwords]
    print(tokens)
    
    df = compute_df(index)

    vocabulary = list(index.keys()) #All of word to index 
    query_vector = {}
    for token in tokens:
        if token in vocabulary:
            query_vector[token] = compute_tf_idf(token, tokens, index,df)

    # Build document vectors
    doc_vectors = {}
    for token, docs in index.items():
        for doc_id, score in docs.items():
            if doc_id not in doc_vectors:
                doc_vectors[doc_id] = {}
            doc_vectors[doc_id][token] = score

    # Convert vectors to numpy arrays
    doc_ids = list(doc_vectors.keys())
    query_vec = np.array([query_vector.get(token, 0) for token in vocabulary])
    doc_matrix = np.array([
        [doc_vectors[doc_id].get(token, 0) for token in vocabulary] for doc_id in doc_ids
    ])

    # Compute cosine similarity
    query_vec = query_vec.reshape(1, -1)
    print(f"query vector : {query_vec}")
    print(f"doc_matrix:{doc_matrix}")
    similarities = cosine_similarity(query_vec, doc_matrix).flatten()

    # Rank results
    results = sorted(zip(doc_ids, similarities), key=lambda x: -x[1])[:top_k]
    return results
# Test the search function
query = "Joker batman"
results = search(query)

# Print results
print("Top Search Results:")
for rank, (doc_id, score) in enumerate(results, start=1):
    print(f"{rank}. Document: {doc_id}, Similarity Score: {score:.4f}")