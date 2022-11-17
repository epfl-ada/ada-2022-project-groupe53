

class Article: 
    """Article class
    Args:
    id : sclar
    title : string
    category : string, main category of the article (last one in the categories.tsv)
    topic : string, the most general category of the article (first one in categories.tsv)
    """
    def __init__(self,id,title,category):
        self.category = category
        self.id = id
        self.title = title



