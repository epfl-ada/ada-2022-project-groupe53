


class Category:

    def __init__(self, title,topic):
        self.articles = {}
        self.title = title
        self.topic = topic


    def add_article(self, article):
        self.articles.append(article)