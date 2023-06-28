### Using Bert tokenizer (Word embedding)

import torch
from transformers import BertTokenizer, AutoModel
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
import numpy as np
import germanStopwords as stopWord
import warnings
from sklearn.exceptions import ConvergenceWarning

def find_optimal_clusters(paragraphs, max_clusters):
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    texts = [paragraph.modContent for paragraph in paragraphs]

    # Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained("bert-base-german-cased")
    model = AutoModel.from_pretrained("bert-base-german-cased")

    # Tokenize the texts
    encoded_inputs = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")

    # Pass the encoded inputs through the model to get the BERT embeddings
    with torch.no_grad():
        outputs = model(**encoded_inputs)
        bert_embeddings = outputs.last_hidden_state[:, 0, :].numpy()

    # Convert the paragraph_texts to TF-IDF vectors with custom stop words
    vectorizer = TfidfVectorizer(stop_words=stopWord.german_stopwords)
    tfidf_vectors = vectorizer.fit_transform(texts)
    tfidf_embeddings = tfidf_vectors.toarray()

    # Concatenate BERT embeddings and TF-IDF vectors
    combined_embeddings = np.concatenate((bert_embeddings, tfidf_embeddings), axis=1)

    silhouette_scores = []
    for num_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
        kmeans.fit(combined_embeddings)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(combined_embeddings, labels)
        silhouette_scores.append(silhouette_avg)

    # Calculate the optimal value of k
    optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2  # Adding 2 to account for starting from k=2

    return optimal_k

def get_Optimal_K(paragraphs):
    max_clusters = len(paragraphs) - 1
    optimalK = find_optimal_clusters(paragraphs, max_clusters)
    print("Optimal K: " + str(optimalK) + "\n")
    return optimalK

'''
# withouth word embedding

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.exceptions import ConvergenceWarning
import warnings

import germanStopwords


def find_optimal_clusters(paragraphs, max_clusters):
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    texts = [paragraph.modContent for paragraph in paragraphs]

    # Convert the list of texts into a matrix of TF-IDF features
    vectorizer = TfidfVectorizer(stop_words=germanStopwords.german_stopwords)
    tfidf_matrix = vectorizer.fit_transform(texts)

    silhouette_scores = []
    for num_clusters in range(2, max_clusters + 1):
        kmeans = KMeans(n_clusters=num_clusters, n_init='auto')
        kmeans.fit(tfidf_matrix)
        labels = kmeans.labels_
        silhouette_avg = silhouette_score(tfidf_matrix, labels)
        silhouette_scores.append(silhouette_avg)

    # Calculate the optimal value of k
    optimal_k = silhouette_scores.index(max(silhouette_scores)) + 2  # Adding 2 to account for starting from k=2

    return optimal_k

def get_Optimal_K(paragraphs):
    max_clusters = (len(paragraphs) - 1)
    optimalK = find_optimal_clusters(paragraphs, max_clusters)
    print("optimal: " + str(optimalK) + "\n")
    return optimalK
'''