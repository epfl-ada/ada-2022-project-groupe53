from Vertex import Vertex

class Topic(Vertex):
    """Topic class
    title : String, the title of the topic
    categories : Dictionnar of categories, key is the title of the category, value is the category object
    """
    def __init__(self, title):
        super().__init__(title)
        self.categories = {}
        self.seen_articles = {}
        
    
    """
    Returns:
    The number of different categories in the topic"""
    def get_nb_different_categories(self):
        return len(self.categories)

    """
    Returns:
    The number of different articles in the topic"""
    def get_nb_different_articles(self):
        return sum([category.get_nb_different_articles() for category in self.categories.values()])   

    """
    Args:
    category : String, the category to add to the categories belongig to the topic
    """
    def add_category(self, category):
        self.categories[category.title]=category



    def add_seen_article(self,article):
        self.seen_articles[article]=article

    def get_nb_seen_articles(self):
        return len(self.seen_articles)
       