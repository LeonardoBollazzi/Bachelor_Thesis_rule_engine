from sklearn.exceptions import ConvergenceWarning
import warnings
import paragraphObject
from sklearn.feature_extraction.text import TfidfVectorizer
import torch
from transformers import BertTokenizer, AutoModel
from sklearn.cluster import KMeans
import numpy as np
import germanStopwords

# Using Word embeddings
def perform_text_clustering(paragraphs, clusterObjects, num_clusters):

    for cN in range(num_clusters):
        paragraphs[cN].clusterN = cN

    paragraph_texts = [p.content for p in paragraphs]

    # Load the tokenizer and model
    tokenizer = BertTokenizer.from_pretrained("bert-base-german-cased")
    model = AutoModel.from_pretrained("bert-base-german-cased")

    # Tokenize the texts
    encoded_inputs = tokenizer(paragraph_texts, padding=True, truncation=True, return_tensors="pt")

    # Pass the encoded inputs through the model to get the BERT embeddings
    with torch.no_grad():
        outputs = model(**encoded_inputs)
        bert_embeddings = outputs.last_hidden_state[:, 0, :].numpy()

    # Convert the paragraph_texts to TF-IDF vectors with custom stop words
    vectorizer = TfidfVectorizer(stop_words=germanStopwords.german_stopwords)
    tfidf_vectors = vectorizer.fit_transform(paragraph_texts)
    tfidf_embeddings = tfidf_vectors.toarray()

    # Concatenate BERT embeddings and TF-IDF vectors
    embeddings = np.concatenate((bert_embeddings, tfidf_embeddings), axis=1)

    # Cluster the embeddings using K-means
    kmeans = KMeans(n_clusters=num_clusters)
    clusters = kmeans.fit_predict(embeddings)

    # Assign the cluster labels to each paragraph
    for i, p in enumerate(paragraphs):
        p.provClust = clusters[i]

    # Adjust order
    freeNum = []
    for cluster_id in range(num_clusters):
        cluster_paragraphs = [p for p in paragraphs if p.provClust == cluster_id]
        clusterNList = [cP.clusterN for cP in cluster_paragraphs if cP.clusterN is not None]
        if not clusterNList:
            if freeNum:
                min_clusterN = min(freeNum)
            else:
                min_clusterN = num_clusters - cluster_id
            for cP in cluster_paragraphs:
                cP.clusterN = min_clusterN
        else:
            min_clusterN = min(clusterNList)
            for cP in cluster_paragraphs:
                cP.clusterN = min_clusterN
            if len(clusterNList) > 1:
                freeNum.append(max(clusterNList))

    for i, obj in enumerate(clusterObjects):
        cluster_paragraphs = [p for p in paragraphs if p.clusterN == i]
        clusterObjects[i].paragraphs = cluster_paragraphs


    # Return the clusters and paragraphs
    return clusterObjects

def getTextCluster(paragraphs, clusters,k):
    num_clusters = k
    result = perform_text_clustering(paragraphs,clusters, num_clusters)
    return result

'''
# Not using word embeddins

def perform_text_clustering(paragraphs, clusters, num_clusters):
    warnings.filterwarnings("ignore", category=FutureWarning)
    warnings.filterwarnings("ignore", category=ConvergenceWarning)

    # Extract the content from each Paragraph object
    texts = [paragraph.modContent for paragraph in paragraphs]

    # Convert the list of texts into a matrix of TF-IDF features
    vectorizer = TfidfVectorizer(stop_words=germanStopwords.german_stopwords)
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Perform clustering using KMeans
    kmeans = KMeans(n_clusters=num_clusters)
    kmeans.fit(tfidf_matrix)

    # Get the cluster labels
    labels = kmeans.labels_

    # Dictionary used to store paragraphs in correct order
    dict = []
    # Assign cluster labels to each Paragraph object
    for i, paragraph in enumerate(paragraphs):
        paraClusterN = labels[i]
        position = None
        for dictEntry in dict:
            if paraClusterN == dictEntry[1]:
                position = dictEntry[0]
                break

        if position == None:
            position = len(dict)
            dict.append([position, paraClusterN])

        for cluster in clusters:
            if cluster.clusterN == position:
                # Inherit from the cluster by changing the paragraph's class
                paragraph.set_parentClusterN(cluster.clusterN)
                cluster.paragraphs.append(paragraph)
                break

    return clusters

def getTextCluster(paragraphs, clusters,k):
    num_clusters = k
    result = perform_text_clustering(paragraphs,clusters, num_clusters)
    return result
'''