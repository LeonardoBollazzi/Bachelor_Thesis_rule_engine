# Association Analysis

import pandas as pd
import xml.etree.ElementTree as ET
from mlxtend.frequent_patterns import apriori, association_rules

def associationRules(categorical_values, paragraph_objects):
    # Extract relevant values from XML and create a DataFrame
    data = []
    for paragraph in paragraph_objects:
        root = ET.fromstring(paragraph.xml)
        row = {}
        for column_values in categorical_values:
            column_name = column_values[0]
            elements = root.findall('.//' + column_name)
            if elements:
                values = [element.text if element.text is not None else '' for element in elements]
                row[column_name] = '/'.join([column_name + '/' + value for value in values])
        row['clusterN'] = paragraph.clusterN  # Add the cluster information
        data.append(row)

    df = pd.DataFrame(data)

    # Apply one-hot encoding
    one_hot_encoding = pd.get_dummies(df, prefix='', prefix_sep='')
    one_hot_encoding = one_hot_encoding.astype(bool)  # Convert values to boolean

    # Initialize the association list
    association_list = []

    # Iterate over unique cluster values
    for cluster in df['clusterN'].unique():
        # Filter the DataFrame for the specific cluster
        cluster_df = one_hot_encoding[df['clusterN'] == cluster]
        pd.set_option('display.max_columns', None)

        # Perform association analysis for the cluster
        frequent_itemsets = apriori(cluster_df, min_support=0.9, use_colnames=True)

        rules = pd.DataFrame()
        if not frequent_itemsets.empty:
            rules = association_rules(frequent_itemsets, metric="confidence", min_threshold=0.7)

        # Check if there are rules
        if not rules.empty:
            # Filter rules with antecedents not containing 'clusterN'
            filtered_rules = rules[
                ~rules['antecedents'].apply(lambda x: any(item.split('/')[0] == 'clusterN' for item in x))]

            # Filter rules with antecedents not containing 'clusterN' and consequents containing only 'clusterN'
            filtered_rules = filtered_rules[
                filtered_rules['consequents'].apply(lambda x: len(list(x)) == 1 and list(x)[0].split('/')[0] == 'clusterN')]

            # Check if there are filtered rules
            if not filtered_rules.empty:
                # Extract antecedents and consequents
                antecedents = filtered_rules['antecedents'].tolist()
                consequents = filtered_rules['consequents'].tolist()

                # Find the list of Paragraph objects with the current cluster number
                paragraph_objs = [p for p in paragraph_objects if p.clusterN == cluster]

                antecedent_lists = [[str(item) for item in max(antecedents, key=len)]] if antecedents else []
                consequent_lists = [[str(item) for item in consequent] for consequent in consequents]

                # Add the association rules to the ruleA variable of each Paragraph object
                for paragraph_obj in paragraph_objs:
                    paragraph_obj.ruleA = [antecedent_lists, [paragraph_obj.clusterN]]
                    paragraph_obj.clusterRule = [antecedent_lists, [paragraph_obj.clusterN]]
