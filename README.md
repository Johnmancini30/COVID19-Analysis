# COVID19-Analysis
This is a project in analyzing COVID19 related news headlines. I wanted to see if applying clustering algorithms to them would seperate them in any interesting ways. It turns out, the K-means clustering is good at seperating articles by publication. 

<h4>Here is a Break Down of Articles by Publication: </h4>

![pie chart of article distribituon](/images/Article-Distribution.png)

<h4>BERT and K-Means Clustering</h4>

We use BERT to perform sentence embedding on each headline. This converts each headline into a 768 dimensional numpy array. This numpy arrays maintain sentence context and similarity to others. Here is the results of applying K-Means to these sentence embeddings: 

<h4>Cluster 0</h4>

![pie chart of article distribution in cluster 0](/images/Cluster-0-Article-Distribution.png)

<h4>Cluster 1</h4>

![pie chart of article distribution in cluster 1](/images/Cluster-1-Article-Distribution.png)
