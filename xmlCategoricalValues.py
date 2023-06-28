# Identification of categorical values in xml by clustering and density analysis
# Does not work for only one document

import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

def extract_values_from_xml(xml_string):

    root = ET.fromstring(xml_string)
    values = []
    for value in root.findall('value'):
        if value.text is not None:
            stripped_value = value.text.strip()
            if stripped_value:
                values.append(stripped_value)
    return values

def calculate_silhouette_score(X, labels):
    score = silhouette_score(X, labels)
    return score


def cluster_values(values):
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform(values)

    # For the silhouette score we try as many k as there are distinct values +1
    # However if k is bigger than the number of values, it will not work
    # Therefore we take the smaler value of unique values +1 and the number of values
    max_clusters = min((len(set(values)) + 1), len(values))

    kmeans_model = None
    clusters = None
    compactness = None
    best_score = -1
    best_clusters = 2

    for k in range(2, max_clusters):
        kmeans = KMeans(n_clusters=k, n_init='auto')
        labels = kmeans.fit_predict(X)
        score = calculate_silhouette_score(X, labels)

        if score > best_score and k != len(values):
            best_score = score
            kmeans_model = kmeans
            best_clusters = k
            clusters = labels
            # Check if any cluster has different values
            has_different_values = any(
                len(set([values[i] for i in range(len(values)) if labels[i] == cluster_id])) > 1 for cluster_id in
                range(k))

            # Set compactness based on whether there are different values
            compactness = 1 if has_different_values else kmeans_model.inertia_

    # clusters = kmeans_model.fit_predict(X)
    # compactness = kmeans_model.inertia_
    return clusters, compactness, best_clusters

def categoriesCluster(xml_list):
    categorical_values = []

    for xml_string in xml_list:
        values = extract_values_from_xml(xml_string)
        # Skip clustering if values list is empty
        if not values:
            continue
        clusters, compactness, best_clusters = cluster_values(values)

        # Check if overall compactness is 0 -> higher compactness means less dense clusters
        if compactness == 0:
            tag_name = ET.fromstring(xml_string).tag
            tag_values = list(set([values[i] for i, c in enumerate(clusters)]))
            categorical_values.append([tag_name] + tag_values)

    return categorical_values


def categoriesPredefined(xml_list):
    categorical_values = []

    for xml_string in xml_list:
        values = extract_values_from_xml(xml_string)
        # Skip clustering if values list is empty
        if not values:
            continue

        # Check if there are fewer than 3 distinct values per XML row
        if len(set(values)) < 3 and len(set(values)) > 1:
            tag_name = ET.fromstring(xml_string).tag
            tag_values = list(set(values))
            categorical_values.append([tag_name] + tag_values)

    return categorical_values