


class Category:

    def __init__(self, title,topic):
        self.articles = {}
        self.title = title
        self.topic = topic
        self.neighbors_out =  {}
        self.neighbors_in =  {}
        self.out_weight = 0
        self.in_weight = 0
        self.size = 0


    def add_article(self, article):
        self.articles[article.id]=article
        self.size += 1
    
    def update_neighbors(self,category,out=True):
      

        if out:
            self.out_weight += 1
            if category not in self.neighbors_out :
                self.neighbors_out[category] = 1
            else:
                self.neighbors_out[category] += 1
        else:

            self.in_weight += 1
            if category not in self.neighbors_in :
                self.neighbors_in[category] = 1
            else:
                self.neighbors_in[category] += 1
        


    
       