from Vertex import Vertex

class Article(Vertex): 
    """Article class
    Args:

    """
    def __init__(self,title,topic,category):
        self.topic = topic
        self.category =  category
        super().__init__(title)




