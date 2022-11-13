

class Topic:
    def __init__(self, name):
        self.name = name
        self.categories = {}
        self.categories_fq = {}
        self.size = 0


    def add_category(self, category):
        if category not in self.categories:
            self.categories[category] = category
            self.categories_fq[category] = 1
        else:
            self.categories_fq[category] += 1


   