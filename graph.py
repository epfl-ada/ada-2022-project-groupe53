import numpy as np
import csv

from category import Category
from topic import Topic
from article import Article

class Graph:
    """Graph class
    Args:
    categories : dict of Category, key is the id of categories, value is the category object
    topics : dict of Topic, key is the name of topics, value is the topic object
    articles : dict of Article, key is the id of articles, value is the article object
    """
    def __init__(self):
         self.categories = {}
         self.articles = {}
         self.topics = {}
         self.matrix = {}
         self.nb_articles = 0
         self.nb_categories = 0
         self.nb_topics = 0
         self.backlicks = 0
         self.edges = 0



    def add_article(self,article):
        self.nb_articles += 1
        #add article to the graph
        self.articles[article.title] = article
        
        #update the categories
        self.update_categories(article.category,article)

        #update the topics
        self.update_topics(article.topic,article)


    def update_categories(self, category,article):
        # Checks if the category was already initialized
        if category not in self.categories: 
            
            self.categories[category] = Category(category,article.topic)
            self.nb_categories += 1
        self.categories[category].add_article(article)

    def update_topics(self, topic,article):
        if topic not in self.topics:  #if topic not already initialized
            self.topics[topic] = Topic(topic)
            self.nb_topics += 1
       
     
        self.topics[topic].add_category(article.category)
            
    def add_edge(self,article1,article2):
        if article1 == '<' or article2 == '<':
            self.backlicks += 0.5
           
        else:
            if  article1 not in self.articles or article2 not in self.articles:
                print("Article not found : {} or {}".format(article1,article2))
            
                return

            category1 = self.articles[article1].category
            category2 = self.articles[article2].category
          
            assert category1 in self.categories
            assert category2 in self.categories

            
            if category1== category2:
                return
            if category1 not in self.matrix:
                self.matrix[category1]= {}
                self.matrix[category1][category2] = 1
            

            else:
                if category2 not in self.matrix[category1]:
                    self.matrix[category1][category2] = 1
                else:
                    self.matrix[category1][category2] += 1
                

            self.edges += 1
            #update categories attributes
            self.categories[category1].update_neighbors(category2,out=True)
            self.categories[category2].update_neighbors(category1,out=False)


    def update_graph(self, file_path , edges=False, verbose= False):
        with open(file_path) as file:
            tsv_file = csv.reader(file, delimiter="\t")
            idx = 0
            for line in tsv_file:
                # Skip empty or commented lines 
                if len(line)==0 or line[0].startswith("#"):
                    continue
                else:
                    if edges :
                        articles = line[3].split(';')
                        for i in range(len(articles)-1):
                            self.add_edge(articles[i],articles[i+1])
                    else :           
                        article = Article(idx,line[0],line[1].split('.')[-1],line[1].split('.')[1])
                        idx+=+1
                        self.add_article(article)
        if verbose :
            print("The graph has {} articles, \n{} categories, \n{} topics,\nand {} edges.".format(
                self.nb_articles, self.nb_categories, self.nb_topics, self.edges))