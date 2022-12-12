import pandas as pd
import numpy as np

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

    def __init__(self,plain_text_path, article_list, nb_topics ):
        """
        @param plain_text_path: String, the path to the folder containing the articles
        @param article_list: List of Strings, the list of articles to be considered when building the model
        @param nb_topics: Integer, the number of topics to be considered when building the model
        """
        # Initialize the lemmatizer, stop words, tokenizer and normalizer 
        # used to clean the text
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.tokenizer=WordPunctTokenizer()
        self.text_processor = TextPreProcessor(
                # Terms that will be normalized 
                normalize=['email', 'percent', 'money', 'phone', 'user','time', 'url', 'date', 'number'],
                # Terms that will be annotated
                tokenizer=self.tokenizer.tokenize
        )

        # Initialize the path from which the articles will be read
        self.plain_text_path = plain_text_path
        # Initialize the list of articles to be considered whe building the model
        self.article_list = article_list
        # Initialize the dataframe of articles and their preprocessed text
        self.articles_df = self.build_article_df()
        # Initialize the LDA model
        self.lda = self.build_lda_model(nb_topics = nb_topics)

    def build_article_df (self):
        """
        @return: Pandas DataFrame, the dataframe of articles and their preprocessed text
        """

        # Create a dataframe with the articles as index and the text as column
        articles_df = pd.DataFrame(columns=['text'])

        # Go through the articles and add them to the dataframe
        for article in self.article_list :
            if article!= 'Pikachu':
                with open(self.plain_text_path+article+".txt") as f:
                    # Read the text of the article
                    text = f.read()
                   
                    # Remove the header
                    text = text.split("Related subjects:")[1]
                    text = text.split("\n\n")[1]

                    #Add the article to the dataframe after preprocessing the text
                    articles_df.loc[article] = self.preprocess_text( text)
        return articles_df
    
    def build_lda_model(self, nb_topics = 10):
        """
        @param nb_topics: Integer, the number of topics to be considered when building the model
        @return: LatentDirichletAllocation, the LDA model
        """
        # Perform tf-idf
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(self.articles_df['text'])

        # Perform latent dirichlet allocation
        lda = LatentDirichletAllocation(n_components=nb_topics, random_state=53)
        lda.fit(X)
        return lda

    def compare_articles(self, article1, article2):
        # Get the index of the article in the dataframe
        index1 = self.articles_df.index.get_loc(article1)
        index2 = self.articles_df.index.get_loc(article2)
        # Get the lda vector of the two articles
        lda_vector1 = self.lda.components_[:,index1]
        lda_vector2 = self.lda.components_[:,index2]
        # Compute the cosine similarity
        similarity = np.dot(lda_vector1, lda_vector2) / (np.linalg.norm(lda_vector1) * np.linalg.norm(lda_vector2))
        return similarity
        
    def preprocess_text(self, text, lemmatize = True, remove_stopwords = True, caseFolding = True, normalize= True): 
        # Convert to lower case
        if caseFolding:
            text = text.lower()
        # Normalize text
        if normalize:
            text = self.text_processor.pre_process_doc(text)
        # Tokenize text
        if remove_stopwords:
            text = [word for word in text if word not in self.stop_words]
        # Lemmatize text
        if lemmatize:
            text = [self.lemmatizer.lemmatize(word) for word in text]
        return ' '.join(text)