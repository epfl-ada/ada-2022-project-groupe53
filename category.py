from Vertex import Vertex

class Category(Vertex):
    """Category class
    title : String, the title of the category
    topic : String, the topic of the category
    articles : Dictionnar of articles, key is the title of the article, value is the article object
    """
    def __init__(self, title, topic):
        super().__init__(title)
        self.topic = topic
        self.articles = {}

    """"
    Returns:
    The number of different articles in the category
    """
    def get_nb_different_articles(self):
        return len(self.articles)   

    """
    Args:
    article : String, the article to add to the articles belongig to the category
    """
    def add_article(self, article):
        self.articles[article.title]=article
