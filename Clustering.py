import numpy as np
import pandas as pd

#Plotting
import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

#General sklrean preprocessing
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

#Dim reduction
#from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

#CLustering
from sklearn.cluster import KMeans
from sklearn.cluster import AgglomerativeClustering

#Scipy for dendrogram
from scipy.cluster.hierarchy import dendrogram
from scipy.cluster.hierarchy import linkage
from scipy.spatial.distance import pdist


def cluster_plotting(reduction_alg, clustering_alg):
    """
    Extract wrangled dataframe, perform dimensionality reduction with reduction_alg and clustering with clustering_alg
    Plot the results

        args:
            reduction_alg - sklearn reduction algorithm and hyperparameters
            clustering_alg - sklearn clustering algorithm and hyperpaprameters

        returns:
            None
    """
    df = pd.read_csv("./data/WrangledDf.csv", header=0)
    np_df = df.drop("Muscle cells", axis = 1).to_numpy()
    data, cells = np_df[:, 1:], np_df[:, 0]

    #Visualizer
    visual_pipe = Pipeline([
                            ("reduction", reduction_alg)
                          ])
    visual_res = visual_pipe.fit_transform(data)
    df["Red1"] = visual_res[:,0]
    df["Red2"] = visual_res[:,1]

    #Clustering
    cluster_pipe = Pipeline([
                             ("scaler", StandardScaler()),
                             ("cluster", clustering_alg)
                           ])

    cluster_res = cluster_pipe.fit_predict(data)
    df["Labels"] = cluster_res
    plot = sns.scatterplot(x = "Red1", y = "Red2", data = df, hue = "Labels", style = "Muscle cells")
    plt.title(str(reduction_alg) + " visualization of " + str(clustering_alg) + " clustering")
    plt.gca().set_aspect('equal', 'datalim')


reduction_alg = TSNE(n_components = 2, perplexity = 80)
clustering_alg = KMeans(n_clusters = 4, n_init = 30, random_state = 0)

cluster_plotting(reduction_alg, clustering_alg)



df = pd.read_csv("./data/WrangledDf.csv", header=0)
np_df = df.drop("Muscle cells", axis = 1).to_numpy()
data, cells = np_df[:, 1:], np_df[:, 0]

def plot_dendrogram(data, metric_pdist: str = "euclidean", metric_linkage: str = "euclidean", method_linkage: str = "ward", **kwargs):
    """
    Compute the distance and linkage matrix from data
    Plot dendrogram

        args:
           data(float) - m * n array of numerical data (m samples, n features)
           metric_pdist(str) - distance norm for calculating the distance matrix, see scipy.spatial.distance.pdist()
           metric_linkage(str)  - distance norm for computing linkage matrix, see scipy.cluster.hierarchy.linkage()
           method_linkage(str) - algorithm for computing the linkage matrix, see scipy.cluster.hierarchy.linkage()
           **kwargs - extra arguments for scipy.cluster.hierarchy.dendrogram(), including labels from sklearn hierarchical clustering results

        returns:
           None
        """
    distance_matrix = pdist(data, metric = metric_pdist)
    linkage_matrix = linkage(distance_matrix, method = method_linkage, metric = metric_linkage, optimal_ordering = False)
    dendrogram(linkage_matrix, **kwargs)

cluster = AgglomerativeClustering(n_clusters = None, distance_threshold = 0)
model = cluster.fit(data)
df["Labels"] = model.labels_
len(model.labels_)

fig = plt.figure(figsize=(25, 10))
plt.title('Hierarchical clustering dendrogram')
plot_dendrogram(data, truncate_mode = "level")
fig.savefig("Dendrogram.png")
