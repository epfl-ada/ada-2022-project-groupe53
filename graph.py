import numpy as np

from category import Category
from topic import Topic
from article import Article

class Graph:
    def __init__(self):
         self.categories = {}
         self.articles = {}
         self.topics = {}
         self.matrix = {{}}



    def add_article(self,article):

        #add article to the graph
        self.articles[article.title] = article
        
        #update the categories
        self.update_categories(self, article.category,article)

        #update the topics
        self.update_topics(self, article.topic,article)





    def update_categories(self, category,article):

        if category not in self.categories: #if category not already initialized
            self.categories[category] = Category(category)
        else : 
            self.categories[category].add_article(article)






    def update_topics(self, topic,article):

        if topic not in self.topics:  #if topic not already initialized
            self.topics[topic] = Topic(topic)
        else :
            self.topics[topic].add_article(article)



    def add_edge(self,category1,category2):
        assert category1 in self.categories
        assert category2 in self.categories

        if category1 not in self.matrix:
            self.matrix[category1][category2] = 1
            
        else:
            if category2 not in self.matrix[category1]:
                self.matrix[category1][category2] = 1
            else:
                self.matrix[category1][category2] += 1
            



