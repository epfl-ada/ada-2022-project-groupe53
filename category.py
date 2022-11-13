


class Category:

    def __init__(self, title,topic):
        self.articles = {}
        self.title = title
        self.topic = topic
        self.neighbors =  {}
        self.out_weight = 0
        self.in_weight = 0
        self.size = 0


    def add_article(self, article):
        self.articles[article.id]=article
        self.size += 1
    
    def update_neighbors(self,category,out=True):
        if category not in self.neighbors:
            self.neighbors[category] = 1
        else:
            self.neighbors[category] += 1

        if out:
            self.out_weight += 1
        else:
            self.in_weight += 1
        
