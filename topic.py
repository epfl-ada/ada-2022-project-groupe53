from Vertex import Vertex

class Topic(Vertex):
    """Topic class
    Args:

    """
    def __init__(self, title):
        super().__init__(title)
        self.categories = {}
    
    def get_nb_different_categories(self):
        return len(self.categories)

    def get_nb_different_articles(self):
        return sum([category.get_nb_different_articles() for category in self.categories.values()])   

    def add_category(self, category):
        self.categories[category.title]=category
