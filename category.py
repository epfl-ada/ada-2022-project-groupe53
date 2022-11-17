


class Category:
    """Category class
    Args:
    id : sclar
    title : string
    topic : string, the most general category to which can belong the category (first one in categories.tsv)
    articles : dict of Article, key is the id of articles belonging to the category, value is the article object
    neighbors_out : dict, keys are the categories to which the category is linked (outgoing), values are the number of times the link appears
    neighbors_in : dict, keys are the categories from which the category is linked (incoming), values are the number of times the link appears
    out_weight : int , the number of time the category is linked to another category (outgoing links)
    in_weight : int , the number of time the category is linked to another category (incoming links)
    size : int, the number of articles in the category
    """
    def __init__(self, title):
        self.articles = {}
        self.title = title
    
        self.neighbors_out =  {}
        self.neighbors_in =  {}
        self.out_weight = 0
        self.in_weight = 0
        self.size = 0


    """
    Args:
    article : Article object to add to the category
    Adds the article to the category and updates the size of the category
    """
    def add_article(self, article):
        # Add the article to the articles dict
        self.articles[article.id]=article
        # Update the size of the category
        self.size += 1
    
    """
    Args:
    Category : neighbour category object to add to the category
    Out : boolean, True if the link is outgoing, False if the link is incoming
    """
    def update_neighbors(self,category,out=True):
        if out:
            # Update the number of outgoing links 
            self.out_weight += 1
            if category not in self.neighbors_out :
                # If the category is not in the neighbors_out dict, add it
                self.neighbors_out[category] = 1
            else:
                # If the category is already in the neighbors_out dict, update the number of time the link was encountred 
                self.neighbors_out[category] += 1
        else:
            # Update the number of incoming links
            self.in_weight += 1
            if category not in self.neighbors_in :
                # If the category is not in the neighbors_in dict, add it
                self.neighbors_in[category] = 1
            else:
                # If the category is already in the neighbors_in dict, update the number of times the link was encountred 
                self.neighbors_in[category] += 1
        


    
       