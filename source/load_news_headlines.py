"""
load_news_headlines.py
"""

import requests
import pandas as pd
import time
import csv
import json

API_DIR = "/Users/john/Desktop/FINAL_SEMESTER/machine_learning/final_project/api_keys.txt"
HEADLINES_DIR = "/Users/john/Desktop/FINAL_SEMESTER/machine_learning/final_project/data/headlines.csv"


"""
A class for loading in news headlines from saved csv files
"""
class News_Loader:

    """
    Constructor
    """
    def __init__(self, api_key_dir: str, headlines_dir: str):
        self.api_key_dir = api_key_dir
        self.headlines_dir = headlines_dir
        self.headlines = []
        self.sources = {}


    """
    gets data from nyt api and writes it as csv to the given directory
    """
    def get_nyt_data(self, url: str, api_key: str, csv_dir: str):
        data = {"headline": [], "source": [], "date": []}

        for i in range(1, 201):
            payload = {"q": "covid", "api-key": api_key, "begin_date": "20200101", "end_date": "20200419",
                       "page": str(i)}
            response = requests.get(url=url, params=payload)
            try:
                response_list = response.json()["response"]["docs"]
            except:
                print("Fault")

            for val in response_list:
                data["headline"].append(val["headline"]["main"])
                data["source"].append(val["source"])
                data["date"].append(val["pub_date"])

            print("Writing page", str(i))
            time.sleep(6)

        df = pd.DataFrame.from_dict(data)
        df.to_csv(csv_dir, mode='a', header=False)


    """
    gets data from newsapi.org
    """
    def get_newsapi_data(self, url: str, api_key: str, csv_dir: str):
        payload = {"q": "covid", "apiKey": api_key, "pageSize": 100}
        response = requests.get(url=url, params=payload)
        articles_list = response.json()['articles']
        data = {"headline": [], "source":[ ], "date": []}

        for article in articles_list:
            data["headline"].append(article["title"])
            data["source"].append(article["source"]["name"])
            data["date"].append(article["publishedAt"])

        df = pd.DataFrame.from_dict(data)
        df.to_csv(csv_dir, mode='a', header=False)


    """
    gets data from openblender.io that is stored in a json 
    """
    def get_blender_data(self, json_dir: str, csv_dir: str):
        with open(json_dir) as f:
            j = json.loads(f.read())

        data = {"headline": [], "source": [], "date": []}

        for key in j["source_lst"].keys():
            added = False
            for src in j["source_lst"][key]:
                if "usatoday" in src:
                    data["source"].append("USA Today")
                elif "wsj" in src:
                    data["source"].append("Wall Street Journal")
                elif "cnn" in src:
                    data["source"].append("CNN")
                else:
                    continue

                data["headline"].append(src)
                data["date"].append(j["timestamp.date"][key])

        tot = 0
        for i in range(len(data["headline"])):
            if "(cnn business)" in data["headline"][i]:
                data["headline"][i] = data["headline"][i].replace("(cnn business)", "")
                tot += 1
            if "https" in data["headline"][i]:
                data["headline"][i] = data["headline"][i].split("https")[0]
                tot += 1

        df = pd.DataFrame.from_dict(data)
        df.to_csv(csv_dir, mode='a', header=False)


    """
    reads api_keys file and parses them
    """
    def read_api_keys(self, nyt=False, newsapi=False, blender=False):
        with open(self.api_key_dir) as f:
            for line in f.read().split("\n"):
                line = line.split("|")
                if line[0] == "NYT" and nyt == True:
                    self.get_nyt_data(line[1], line[2], line[3])
                elif line[0] == "NEWSAPI" and newsapi == True:
                    self.get_newsapi_data(line[1], line[2], line[3])
                elif line[0] == "BLENDER" and blender == True:
                    self.get_blender_data(line[1], line[2], line[3])



    """
    Collects all stored data and stores them in memory
    """
    def load_news_data(self):
        with open(self.headlines_dir) as csv_file:
            reader = list(csv.reader(csv_file, delimiter=','))
            for row in reader[1:]:
                if row[2] not in self.sources.keys():
                    self.sources[row[2]] = []
                self.sources[row[2]].append(row[1])

        for source in self.sources.keys():
            self.headlines += self.sources[source]

        to_sort = sorted(zip(self.sources.keys(), self.sources.values()), key=lambda x: len(x[1]), reverse=True)
        d = {}
        for key, val in to_sort:
            d[key] = val
        self.sources = d


    """
    merge all data files to one file
    """
    def merge_data_files(self):
        data = {"headline": [], "source": [], "date": []}
        with open(self.api_key_dir) as f:
            text = f.read()
            lines = text.split("\n")[:-1] if len(text.split("\n")[-1]) == 0 else text.split("\n")
            for line in lines:
                line = line.split("|")
                with open(line[3]) as csv_file:
                    reader = list(csv.reader(csv_file, delimiter=','))
                    for row in reader[1:]:
                        data["headline"].append(row[1].lower())
                        data["source"].append(row[2])
                        data["date"].append(row[3])

        df = pd.DataFrame.from_dict(data)
        df.to_csv(self.headlines_dir)


    """
    Finds data about article distribution, percentage of total articles one source contributes to data set
    """
    def article_distribution(self):
        try:
            n = len(self.headlines)
            print("Total news articles:", n)
            for source in self.sources:
                print(source + ": " + str(len(self.sources[source])) + " articles, " + str(round(len(self.sources[source]) / n, 6)) + " of dataset")
            print("=============================================")
        except:
            print("Data has not been loaded")



if __name__=='__main__':
    pass




