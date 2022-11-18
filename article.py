from Vertex import Vertex

class Article(Vertex): 
    """Article class    
    topc : String, the topic of the article
    category : String, the category of the article
    """
    def __init__(self,title,topic,category):
        self.topic = topic
        self.category =  category
        super().__init__(title)




