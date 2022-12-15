import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer


"""
ArticleComparator class uses BERT to compare articles. 
The class takes in the path to plaintext articles and a list of articls names.
It has methods to clean the text in the articles, build a dataframe of the articles and their embeddings.
The compare_articles method takes in two articles content and returns their similarity according to BERT model.
The compare_titles method takes in two articles titles and returns their similarity according to BERT model.
"""

class ArticleComparator :

    def __init__(self,plain_text_path, article_list ):
        """
        @param plain_text_path: String, the path to the folder containing the articles
        @param article_list: List of Strings, the list of articles to be considered when building the modell
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
                    # Get the title of the article
                    text = text.split("\n")
                    title = text[2]
                    # Remove the title from the text
                    text = " ".join(text[3:])

                    #Add the article to the dataframe after preprocessing the text, and computing the embedding
                    articles_df.loc[article] = [text , self.bert_model.encode(text), self.bert_model.encode(title)]
        return articles_df
    

    def compare_articles(self, article1, article2):
        """
        @param article1: String, the name of the first article
        @param article2: String, the name of the second article
        @return: Float, the cosine similarity between the two articles
        """

        # Compute the cosine similarity between the two articles content
        embedding1 = self.articles_df.loc[article1]['article_embedding']
        embedding2 = self.articles_df.loc[article2]['article_embedding']
        return self.cosine_similarity(embedding1, embedding2)

    def compare_titles(self, article1, article2):
        """
        @param article1: String, the name of the first article
        @param article2: String, the name of the second article
        @return: Float, the cosine similarity between the two article titles 
        """

        # Compute the cosine similarity between the two articles titles
        embedding1 = self.articles_df.loc[article1]['title_embedding']
        embedding2 = self.articles_df.loc[article2]['title_embedding']
        return self.cosine_similarity(embedding1, embedding2)
    
    # define a cosine similarity function that gives values between 0 and 1
    def cosine_similarity(self, v1, v2):
        return np.abs(np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))).round(2)
