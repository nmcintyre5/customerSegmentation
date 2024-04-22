import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler, normalize
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from jupyterthemes import jtplot
jtplot.style(theme='monokai', context='notebook', ticks=True, grid=False) 

# Function for data preprocessing
def preprocess_data(data):
    # Fill null values with median
    data.loc[data['MINIMUM_PAYMENTS'].isnull(), 'MINIMUM_PAYMENTS'] = data['MINIMUM_PAYMENTS'].median()
    data.loc[data['CREDIT_LIMIT'].isnull(), 'CREDIT_LIMIT'] = data['CREDIT_LIMIT'].median()
    
    # Drop duplicates and unnecessary columns
    data.drop_duplicates(inplace=True)
    data.drop('CUST_ID', axis=1, inplace=True)
    
    return data

# Function for visualizing histograms
def visualize_histograms(data):
    plt.figure(figsize=(10, 50))
    for i, col in enumerate(data.columns):
        plt.subplot(17, 1, i + 1)
        sns.histplot(data[col], kde_kws={"color": "b", "lw": 3})
        plt.title(col)
    plt.tight_layout()

# Function for determining optimal number of clusters
def find_optimal_clusters(data):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    scores = []
    for i in range(1, 20):
        kmeans = KMeans(n_clusters=i)
        kmeans.fit(data_scaled[:, :7])
        scores.append(kmeans.inertia_)
    
    plt.plot(range(1, 20), scores, marker='o', linestyle='-', color='b')
    plt.xticks(np.arange(1, 21, 1))
    plt.xlabel('Number of clusters')
    plt.ylabel('Inertia')
    plt.title('Elbow Method for Optimal k')
    plt.show()

# Function for k-means clustering
def perform_clustering(data, n_clusters):
    scaler = StandardScaler()
    data_scaled = scaler.fit_transform(data)
    
    kmeans = KMeans(n_clusters)
    kmeans.fit(data_scaled)
    
    cluster_centers = scaler.inverse_transform(kmeans.cluster_centers_)
    cluster_centers_df = pd.DataFrame(data=cluster_centers, columns=data.columns)
    
    return kmeans.labels_, cluster_centers_df

# Function for saving output to a file
def save_output_to_file(filename, content):
    with open(filename, 'w') as file:
        file.write(content)

# Load the data
cc_df = pd.read_csv('marketing_data.csv')

# Preprocess the data
cc_df = preprocess_data(cc_df)

# Visualize histograms
visualize_histograms(cc_df)

# Find optimal number of clusters
find_optimal_clusters(cc_df)

# Perform k-means clustering
cluster_labels, cluster_centers_df = perform_clustering(cc_df, 6)

# Save cluster centers to a file
save_output_to_file('cluster_centers.txt', cluster_centers_df.to_string())

# Display cluster summary
cluster_summary = cluster_centers_df.median()
print("\nCluster Summary:")
print(cluster_summary)

# Plot cluster characteristics using a heatmap
plt.figure(figsize=(30, 6))
sns.heatmap(cluster_centers_df, cmap='viridis', annot=True, fmt=".2f", linewidths=.1)
plt.title('Cluster Characteristics')
plt.xlabel('Feature')
plt.ylabel('Cluster')
plt.show()

# Describe each cluster based on the median values of features
for cluster_label, cluster_data in cluster_centers_df.iterrows():
    print(f"\nCluster {cluster_label} Profile:")
    print(cluster_data)

# Apply principal component analysis (PCA)
pca = PCA(n_components=2)
principal_comp = pca.fit_transform(cc_df)
pca_df = pd.DataFrame(data=principal_comp, columns=['pca1', 'pca2'])

# Visualize clusters in a scatter plot
plt.figure(figsize=(10, 10))
ax = sns.scatterplot(x="pca1", y="pca2", hue="cluster", data=pd.concat([pca_df, pd.DataFrame({'cluster': cluster_labels})], axis=1), palette=['red', 'green', 'blue', 'pink', 'yellow', 'purple'])
plt.show()

