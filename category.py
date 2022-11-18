from Vertex import Vertex

class Category(Vertex):
    """Category class
    
    """
    def __init__(self, title, topic):
        super().__init__(title)
        self.topic = topic
        self.articles = {}
        
    def get_nb_different_articles(self):
        return len(self.articles)   

    """
    Args:

    """
    def add_article(self, article):
        self.articles[article.title]=article
