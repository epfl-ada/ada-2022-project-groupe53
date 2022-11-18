import numpy as np
import csv

from category import Category
from topic import Topic
from article import Article

class Graph:
    """Graph class
    Args:
    """
    def __init__(self):
        self.articles = {}
        self.categories = {}
        self.topics =  {}     
       
        self.matrix_articles = {}
        self.matrix_categories = {}
        self.matrix_topics =  {}

        self.authorized_levels = ["articles", "categories", "topics"]
        self.levels_map = {"articles": (self.matrix_articles,self.articles),
                         "categories": (self.matrix_categories, self.categories),
                          "topics": (self.matrix_topics, self.topics)}

        self.backlicks = 0

    def nb_verteces(self , level ):

        assert level in self.authorized_levels
        _ , verteces = self.levels_map[level]
        return len(verteces)
    
    def nb_unique_edges(self, level ):
        
        assert level in self.authorized_levels
        matrix , _ = self.levels_map[level]
        
        return sum([len(matrix[title]) for title in matrix.keys()])

    def nb_total_edges_out(self, level ):
        
        assert level in self.authorized_levels
        _ , verteces = self.levels_map[level]
        
        return sum([vertex.get_total_out_weight() for vertex in verteces.values()])

    def nb_total_edges_in(self, level):
        
        assert level in self.authorized_levels
        _ , verteces = self.levels_map[level]
        
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
        if topic not in self.topics: 
            self.topics[topic] = Topic(topic)
            self.topics[topic].add_category(category)

         
    def add_edge(self,article1,article2):
        if article1 == '<' :
            self.backlicks += 0.5
            article1 = self.previous_article

        elif article2 == '<' :
            self.backlicks += 0.5
            self.previous_article = article1
           
        else:      
            # update the articles graph     
            self.update_level(article1,article2,"articles")

            category1 = self.articles[article1].category
            category2 = self.articles[article2].category
            
            # update the categories graph  
            self.update_level(category1,category2,"categories")
            
            topic1 = self.articles[article1].topic
            topic2 = self.articles[article2].topic
            
            # update the topics graph 
            self.update_level(topic1,topic2,"topics")

    def update_level (self , vertex1, vertex2, level):
        # checks that the level is authorized
        assert level in self.authorized_levels

        # Choose the  matrix and the verteces corresponding to the level
        matrix , verteces = self.levels_map[level]
            
        # Verify if the verteces are already in the graph    
        assert vertex1 in verteces
        assert vertex2 in verteces

        # We don't add edges between the same vertex
        if vertex2 == vertex1:
            return

        ## update the matrix
        if vertex1 not in matrix:
            matrix[vertex1] = {}
            matrix[vertex1][vertex2] = 1
        else:
            if vertex2 not in matrix[vertex1]:
                matrix[vertex1][vertex2] = 1
            else:
                matrix[vertex1][vertex2] += 1
        # update the vertex attributes
        verteces[vertex1].update_neighbors(verteces[vertex2],out=True)
        verteces[vertex2].update_neighbors(verteces[vertex1],out=False)

    

            
   