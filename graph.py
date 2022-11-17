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
        self.articles = {}
        self.categories = {}
        self.topics =  {}     
       
        
        self.matrix_articles = {}
        self.matrix_categories = {}
        self.matrix_topics =  {}

        self.backlicks = 0
        self.memory = {}

    def nb_verteces(self , level = "articles"):

        assert level in ["articles", "categories", "topics"]

        if level == "articles":
            return len(self.articles)
        elif level == "categories":
            return len(self.categories)
        elif level == "topics":
            return len(self.topics)
    
    def nb_unique_edges(self, level = "articles"):
        
        assert level in ["articles", "categories", "topics"]

        if level == "articles":
            matrix = self.matrix_articles
        elif level == "categories":
            matrix = self.matrix_categories
        elif level == "topics":
            matrix = self.matrix_topics
        
        return sum([len(matrix[title]) for title in matrix.keys()])

    def nb_total_edges_out(self, level = "articles"):
        
        assert level in ["articles", "categories", "topics"]

        if level == "articles":
            verteces = self.articles
        elif level == "categories":
            verteces = self.categories
        elif level == "topics":
            verteces = self.topics
        
        return sum([vertex.get_total_out_weight() for vertex in verteces.values()])

    def nb_total_edges_in(self, level = "articles"):
        
        assert level in ["articles", "categories", "topics"]

        if level == "articles":
            verteces = self.articles
        elif level == "categories":
            verteces = self.categories
        elif level == "topics":
            verteces = self.topics
        
        return sum([vertex.get_total_in_weight() for vertex in verteces.values()])


    def update_graph(self, file_path , edges=False, verbose= False):
        with open(file_path) as file:
            tsv_file = csv.reader(file, delimiter="\t")
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
                        article = Article(line[0],line[1].split('.')[1], line[1].split('.')[-1])
                        self.add_article(article)
        if verbose :
            print("The graph has {} articles, {} categories, and {} topics.".format(
                self.nb_verteces("articles"), self.nb_verteces("categories"),  self.nb_verteces("topics")))
            print("The number of edges is :\n{} in the articles graph,\n{} in the categories graph,\n{} in the topics graph.".format(
                self.nb_unique_edges("articles"), self.nb_unique_edges("categories"),  self.nb_unique_edges("topics")))
    
    def add_article(self,article):
        #add article to the graph
        self.articles[article.title] = article
        #update the categories
        category = self.update_categories(article.category,article)
        #update the topics
        self.update_topics(article.topic,category)

    def update_categories(self, category,article):
        # Checks if the category was already initialized
        if category not in self.categories: 
            self.categories[category] = Category(category, article.topic)
            self.categories[category].add_article(article)
        return self.categories[category]
    
    def update_topics(self, topic,category):
        # Checks if the category was already initialized
        if topic not in self.topics: 
            self.topics[topic] = Topic(topic)
            self.topics[topic].add_category(category)

   
         
    def add_edge(self,article1,article2):
        if article1 == '<' :
            self.backlicks += 0.5
            article1 = self.previous_article

        if article2 == '<' :
            self.backlicks += 0.5
            self.previous_article = article1
           

        else:
            if  article1 not in self.articles or article2 not in self.articles:
                return

            assert article1 in self.articles
            assert article2 in self.articles

            ## update the articles-matrix
            if article1 not in self.matrix_articles:
                self.matrix_articles[article1] = {}
                self.matrix_articles[article1][article2] = 1
            else:
                if article2 not in self.matrix_articles[article1]:
                    self.matrix_articles[article1][article2] = 1
                else:
                    self.matrix_articles[article1][article2] += 1
            # update the articles attributes
            self.articles[article1].update_neighbors(self.articles[article2],out=True)
            self.articles[article2].update_neighbors(self.articles[article1],out=False)

            category1 = self.articles[article1].category
            category2 = self.articles[article2].category
            
            assert category1 in self.categories
            assert category2 in self.categories
            
            ## update the category-matrix
            if category1== category2:
                return
            if category1 not in self.matrix_categories:
                self.matrix_categories[category1]= {}
                self.matrix_categories[category1][category2] = 1
            else:
                if category2 not in self.matrix_categories[category1]:
                    self.matrix_categories[category1][category2] = 1
                else:
                    self.matrix_categories[category1][category2] += 1
            
            #update categories attributes
            self.categories[category1].update_neighbors(category2,out=True)
            self.categories[category2].update_neighbors(category1,out=False)
            
            topic1 = self.articles[article1].topic
            topic2 = self.articles[article2].topic

            assert topic1 in self.topics
            assert topic2 in self.topics

            ## update the topic-matrix
            if topic1== topic2:
                return
            if topic1 not in self.matrix_topics:
                self.matrix_topics[topic1]= {}
                self.matrix_topics[topic1][topic2] = 1
            else:
                if topic2 not in self.matrix_topics[topic1]:
                    self.matrix_topics[topic1][topic2] = 1
                else:
                    self.matrix_topics[topic1][topic2] += 1
            
            #update topics attributes
            self.topics[topic1].update_neighbors(topic2,out=True)
            self.topics[topic2].update_neighbors(topic1,out=False)



    

            
   