


class Category:
    """Category class
    
    """
    def __init__(self, title, topic):
        self.title = title
        self.topic = topic
        self.articles = {}
        self.neighbors_out =  {}
        self.neighbors_in =  {}
    
    def get_nb_different_articles(self):
        return len(self.articles)   

    def get_nb_different_out_neighbours(self):
        return len(self.neighbors_out)
    
    def get_nb_different_in_neighbours(self):
        return len(self.neighbors_in)
    
    def get_total_out_weight(self):
        return sum(self.neighbors_out.values())
    
    def get_total_in_weight(self):
        return sum(self.neighbors_in.values())


    """
    Args:

    """
    def add_article(self, article):
        # Add the article to the articles dict
        self.articles[article.title]=article

    """
    Args:

    """
    def update_neighbors(self,category,out=True):
        if out:
            # Update the number of outgoing links 
            if category not in self.neighbors_out :
                # If the category is not in the neighbors_out dict, add it
                self.neighbors_out[category] = 1
            else:
                # If the category is already in the neighbors_out dict, update the number of time the link was encountred 
                self.neighbors_out[category] += 1
        else:
            # Update the number of incoming links
            if category not in self.neighbors_in :
                # If the category is not in the neighbors_in dict, add it
                self.neighbors_in[category] = 1
            else:
                # If the category is already in the neighbors_in dict, update the number of times the link was encountred 
                self.neighbors_in[category] += 1
        


    
       