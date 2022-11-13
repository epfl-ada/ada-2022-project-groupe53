import numpy as np

from category import Category
from topic import Topic
from article import Article

class Graph:
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

        if category not in self.categories: #if category not already initialized
            self.categories[category] = Category(category,article.topic)
            self.nb_categories += 1
       

        self.categories[category].add_article(article)






    def update_topics(self, topic,article):

        if topic not in self.topics:  #if topic not already initialized
            self.topics[topic] = Topic(topic)
            self.nb_topics += 1
       
     
        self.topics[topic].add_category(article.category)
            



    def add_edge(self,article1,article2):
        print(article1,article2)
        if article1 == '<' or article2 == '<':
            self.backlicks += 0.5
           
        else:
            if  article1 not in self.articles or article2 not in self.articles:
                print("Article not found")
                return

            category1 = self.articles[article1].category
            category2 = self.articles[article2].category
          
            assert category1 in self.categories
            assert category2 in self.categories

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


