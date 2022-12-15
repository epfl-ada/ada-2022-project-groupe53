import numpy as np
import csv

from category import Category
from topic import Topic
from article import Article
from urllib.parse import unquote

class Graph:
    """Graph class
    articles : dict, the articles of the graph, keys are the titles of the articles
    categories : dict, the categories of the graph, keys are the names of the categories
    topics : dict, the topics of the graph, keys are the names of the topics

    matrix_articles : dict, the adjacency matrix of the articles graph
    matrix_categories : dict, the adjacency matrix of the categories graph
    matrix_topics : dict, the adjacency matrix of the topics graph

    authorized_levels : list, the authorized levels of the graph
    levels_map : dict, the map between the levels and the corresponding matrix and vertices

    backlicks : int, the number of backlinks in the graph
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
        self.paths = []
        self.finished = []


    """"""
    def nb_vertices(self , level ):

        assert level in self.authorized_levels
        _ , vertices = self.levels_map[level]
        return len(vertices)
    
    def nb_unique_edges(self, level ):
        
        assert level in self.authorized_levels
        matrix , _ = self.levels_map[level]
        
        return sum([len(matrix[title]) for title in matrix.keys()])

    def update_graph(self, file_path , mode='Initialization', verbose= False,paths_mode=False,finished = True):
        with open(file_path,encoding="utf8") as file:
            tsv_file = csv.reader(file, delimiter="\t")
            for line in tsv_file:
                # Skip empty or commented lines 
                if len(line)==0 or line[0].startswith("#"):
                    continue
                else:
                    #deocde strings in line frtom utf8
          
                    if mode == 'common_sense_edges' :
                        path = line[3].split(';')
                        backlick = 0 
                        article1 = -1
                        

                        for i in range(len(path)-1):
                            if path[i+1] == '<':
                                backlick += 1
                                continue
                            elif path[i]== '<': 
                                article1 = article1-backlick 
                            else:
                                article1 =i
                                backlick = 0
                            
                            
                                self.add_edge(path[article1],path[i+1])
                        if paths_mode:
                            new_path = self.remove_backclick(path)
                            self.paths.append(new_path)
                            self.finished.append(finished)
                           
                       
                                                   
                    elif mode == 'Initialization' :           
                        article = Article(line[0],line[1].split('.')[1], line[1].split('.')[-1])
                        self.add_article(article)
                        #update the categories
                        category = self.update_categories(article.category,article)
                        #update the topics
                        self.update_topics(article.topic,category)

                    else:
                        self.add_edge(line[0],line[1])
    
        if verbose :
            print("The graph has {} articles, {} categories, and {} topics.".format(
                self.nb_vertices("articles"), self.nb_vertices("categories"),  self.nb_vertices("topics")))
            print("The number of edges is :\n{} in the articles graph,\n{} in the categories graph,\n{} in the topics graph.".format(
                self.nb_unique_edges("articles"), self.nb_unique_edges("categories"),  self.nb_unique_edges("topics")))

    def remove_backclick(self,path):
        n = len(path)
        remove_idx = []
        for i in range(n):
            if path[i] == '<':
                remove_idx.append(i)
        for i in range(len(remove_idx)):
            del path[remove_idx[i]-2*i]
            del path[remove_idx[i]-2*i-1]
        return path
    def add_article(self,article):
        #add article to the graph
        self.articles[article.title] = article
       
    def update_categories(self, category,article):
        # Checks if the category was already initialized
        if category not in self.categories: 
            self.categories[category] = Category(category, article.topic)
            self.categories[category].add_article(article)
        else:
            self.categories[category].add_article(article)
        return self.categories[category]
    
    def update_topics(self, topic,category):
        if topic not in self.topics: 
            self.topics[topic] = Topic(topic)
            self.topics[topic].add_category(category)
        else:
            self.topics[topic].add_category(category)


         
    def add_edge(self,article1,article2):
       
        if(article1 == article2):
            return
        # update the articles graph     
        success  = self.update_level(article1,article2,"articles")
        if success:
            if self.matrix_articles[article1][article2]> 1:
                return

            category1 = self.articles[article1].category
            category2 = self.articles[article2].category
            
            # update the categories graph  
            self.update_level(category1,category2,"categories")
            
            topic1 = self.articles[article1].topic
            topic2 = self.articles[article2].topic
            
            # update the topics graph 
            self.update_level(topic1,topic2,"topics")

    def  update_level (self , vertex1, vertex2, level):
        # checks that the level is authorized
        assert level in self.authorized_levels

        # Choose the  matrix and the vertices corresponding to the level
        matrix , vertices = self.levels_map[level]
            
        # Verify if the vertices are already in the graph    
        if vertex1  not in vertices or vertex2 not in vertices:
            return 0

      

        # We don't add edges between the same vertex
        if vertex2 == vertex1:
            return 0

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
        vertices[vertex1].update_neighbors(vertices[vertex2],out=True)
        vertices[vertex2].update_neighbors(vertices[vertex1],out=False)

        return 1

            
    def get_topic_of_article(self,article):
        if article not in self.articles:
            return None
        return self.articles[article].topic

    def get_weight_of_link(self,article1,article2):
        if article1 not in self.matrix_articles or article2 not in self.matrix_articles[article1]:
            return 0
        return self.matrix_articles[article1][article2]