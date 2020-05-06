"""
cluster.py
"""

"""
prepares data and runs it through k means clustering
"""
from load_news_headlines import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import random
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
random.seed(1)

class Cluster:

    """
    constructor
    """
    def __init__(self):
        self.news_loader = News_Loader(API_DIR, HEADLINES_DIR)
        self.news_loader.load_news_data()
        self.X = None

    """
    prepares data for clustering
    """
    def prepare_data(self):
        vectorizer = TfidfVectorizer(max_features=2000, use_idf=True)
        random.shuffle(self.news_loader.headlines)
        self.X = vectorizer.fit_transform(self.news_loader.headlines)

    """
    give document embedding
    """
    def assign_data(self, data):
        self.X = data

    """
    runs the clustering algorithm
    """
    def k_means_clustering(self, k: int):
        km = KMeans(n_clusters=k, init='k-means++', max_iter=100, n_init=1, random_state=3)

        try:
            km.fit(self.X)
        except:
            print("No data has been prepared. Call the prepare_date method.")

        #print out article distribution
        self.news_loader.article_distribution()


        count = Counter(km.labels_)
        clusters = [{} for i in range(len(count.keys()))]
        cluster_articles = [{} for i in range(len(count.keys()))]

        #cluster gets dictionary of source : number of articles in it
        for i in range(len(km.labels_)):
            key = None
            for source in self.news_loader.sources:
                if self.news_loader.headlines[i] in self.news_loader.sources[source]:
                    key = source
                    break

            if key != None:
                clusters[km.labels_[i]][key] = 1 if key not in clusters[km.labels_[i]].keys() else clusters[km.labels_[i]][key] + 1
                if key not in cluster_articles[km.labels_[i]].keys():
                    cluster_articles[km.labels_[i]][key] = []
                cluster_articles[km.labels_[i]][key].append(self.news_loader.headlines[i])


        #sort clusters by most articles to least
        for i in range(len(clusters)):
            vals = sorted(zip(clusters[i].keys(), clusters[i].values()), key=lambda x: x[1], reverse=True)
            d = {}
            for key, val in vals:
                d[key] = val
            clusters[i] = d

        #displaying cluster information
        for i in range(len(clusters)):
            cluster = clusters[i]
            print("Cluster", str(i) + ": " + str(count[i]) + " articles,", round(count[i]/len(self.news_loader.headlines), 6), "of dataset")
            for source in cluster.keys():
                print(source + ": " + str(cluster[source]) + " articles, " + str(round(cluster[source]/count[i], 6)) + " of cluster")
            print()

        print("=============================================")

        wc = WordCloud(max_words=40)
        for i in range(len(clusters)):
            text = []
            for val in cluster_articles[i].values():
                text += val
            to_show = wc.generate(' '.join(text))
            plt.imshow(to_show)
            plt.show()


if __name__=='__main__':
    cluster = Cluster()
    cluster.prepare_data()
    cluster.k_means_clustering(2)

