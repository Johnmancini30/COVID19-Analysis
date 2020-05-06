"""
This is a file for creating sentence, or headline, embeddings with BERT
"""
from sentence_transformers import SentenceTransformer
from cluster import *
import umap
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import decomposition
from mpl_toolkits.mplot3d import Axes3D

class BERT_Embedding:

    #constructor
    def __init__(self):
        self.cl = Cluster()


    """
    does document embedding with BERT
    """
    def prepare_data(self):
        model = SentenceTransformer('bert-base-nli-mean-tokens')
        sentence_embeddings = model.encode(self.cl.news_loader.headlines)
        self.cl.assign_data(sentence_embeddings)


    """
    runs the k means clustering algorithm on the document embedding
    """
    def k_means_cluster(self):
        self.cl.k_means_clustering(2)


    """
    umap
    """
    def u_map(self):
        colors = [0 for i in range(len(self.cl.X))]
        for i in range(len(self.cl.news_loader.headlines)):
            j = 0
            for key in self.cl.news_loader.sources.keys():
                if self.cl.news_loader.headlines[i] in self.cl.news_loader.sources[key]:
                    colors[i] = j
                    break
                j += 1
            if colors[i] >= 10:
                colors[i] = 9


        reducer = umap.UMAP()
        embedding = reducer.fit_transform(self.cl.X)
        plt.scatter(embedding[:, 0], embedding[:, 1], c=[sns.color_palette()[x] for x in colors])
        plt.gca().set_aspect('equal', 'datalim')
        plt.title('UMAP projection of the Iris dataset', fontsize=24)
        plt.show()


    """
    applying PCA to the sentence embeddings
    """
    def PCA(self):
        pca = decomposition.PCA(n_components=3)
        pca.fit(self.cl.X)
        X = pca.transform(self.cl.X)

        colors = [0 for i in range(len(self.cl.X))]
        for i in range(len(self.cl.news_loader.headlines)):
            j = 0
            for key in self.cl.news_loader.sources.keys():
                if self.cl.news_loader.headlines[i] in self.cl.news_loader.sources[key]:
                    colors[i] = j
                    break
                j += 1
            if colors[i] >= 10:
                colors[i] = 9

        fig = plt.figure(1, figsize=(4, 3))
        ax = Axes3D(fig, rect=[0, 0, .95, 1], elev=48, azim=134)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=[sns.color_palette()[x] for x in colors])

        plt.show()


if __name__=='__main__':
    b = BERT_Embedding()
    b.prepare_data()
    #b.u_map()
    b.PCA()

