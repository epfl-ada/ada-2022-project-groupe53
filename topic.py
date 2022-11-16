

class Topic:
    """Topic class
    Args:
    name : String
    categories : dict of Category, key is the id of categories belonging to the topic, value is the category object
    categories_count : dict, keys are the categories belonging to the topic, 
                        values are the number of times the category appears 
                        (Can be usufull to get some statistics about the topic)
    topic : string, the most general category of the article (first one in categories.tsv)
    size : int, the number of categories in the topic
    """
    def __init__(self, name):
        self.name = name
        self.categories = {}
        self.categories_count = {}
        self.size = 0

    """"
    Args:
    category : Category object to add to the topic
    Adds the category to the topic and updates the size of the topic
    """
    
    def add_category(self, category):

        if category not in self.categories:
            # Add the category to the categories dict
            self.categories[category] = category
            # Update the size of the topic
            self.categories_count[category] = 1
        else:
            # If the category is already in the categories dict, update the number of times 
            self.categories_count[category] += 1


   