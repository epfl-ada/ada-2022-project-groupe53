

class Article: 
    """Article class


    Args:
    id : sclar
    title : string
    category : string, main category of the article
    topic : string, general topic of the article
    """
    def __init__(self,id,title,category,topic):
        self.category = category
        self.id = id
        self.title = title
        self.topic = topic


