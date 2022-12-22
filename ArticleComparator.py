import pandas as pd
import numpy as np
import torch
from sentence_transformers import SentenceTransformer

from transformers import BertTokenizer, BertModel
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from nltk.tokenize import WordPunctTokenizer
from ekphrasis.classes.preprocessor import TextPreProcessor


from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import TfidfVectorizer

"""
ArticleComparator class uses latent Dirichlet allocation (LDA) to compare articles. 
The class takes in a list of articles and a number of topics as arguments to its constructor. 
It has methods to clean the text in the articles, build a dataframe of the articles and their cleaned text,
and to build an LDA model with the cleaned text. 
The compare_articles method takes in two articles and returns their similarity according to the LDA model.
"""

class ArticleComparator :

    def __init__(self,plain_text_path, article_list ):
        """
        @param plain_text_path: String, the path to the folder containing the articles
        @param article_list: List of Strings, the list of articles to be considered when building the model
        @param nb_topics: Integer, the number of topics to be considered when building the model
        """
        # Initialize the path from which the articles will be read
        self.plain_text_path = plain_text_path
        # Initialize the list of articles to be considered whe building the model
        self.article_list = article_list
        # Initialize the bert model to be used for embedding
        self.bert_model =  SentenceTransformer('bert-base-nli-mean-tokens')
        # Initialize the dataframe of articles and their text and embeddings
        self.articles_df = self.build_article_df()

    def build_article_df (self):
        """
        @return: Pandas DataFrame, the dataframe of articles and their preprocessed text
        """

        # Create a dataframe with the articles as index and the text as column
        articles_df = pd.DataFrame(columns=['text', 'article_embedding', 'title_embedding'])

        # Go through the articles and add them to the dataframe
        for article in self.article_list :
            if article!= 'Pikachu':
                with open(self.plain_text_path+article+".txt") as f:
                    # Read the text of the article
                    text = f.read()
                   
                    # Remove the header
                    text = text.split("Related subjects:")[1]
                    text = text.split("\n\n")[1]

                    #Add the article to the dataframe after preprocessing the text, and computing the embedding
                    articles_df.loc[article] = [text , self.bert_model.encode(text), self.bert_model.encode(article.replace("_", " "))]
        return articles_df
    

    def compare_articles(self, article1, article2):
        """
        @param article1: String, the name of the first article
        @param article2: String, the name of the second article
        @return: Float, the cosine similarity between the two articles
        """

        # Compute the cosine similarity between the two articles
        embedding1 = self.articles_df.loc[article1]['article_embedding']
        embedding2 = self.articles_df.loc[article2]['article_embedding']
        return self.cosine_similarity(embedding1, embedding2)

    def compare_titles(self, article1, article2):
        """
        @param article1: String, the name of the first article
        @param article2: String, the name of the second article
        @return: Float, the cosine similarity between the two article titles 
        """

        # Compute the cosine similarity between the two articles
        embedding1 = self.articles_df.loc[article1]['title_embedding']
        embedding2 = self.articles_df.loc[article2]['title_embedding']
        return self.cosine_similarity(embedding1, embedding2)
    
    # define a cosine similarity function that gives values between 0 and 1
    def cosine_similarity(self, v1, v2):
        return np.abs(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))).round(2)
