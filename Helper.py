import pandas as pd
import csv 
from bs4 import BeautifulSoup
import re 



def create_links_df (path='data/links.tsv'):
    """
    @param path: String, the path to the links file

    @return: Pandas DataFrame, the dataframe of links between articles, 
            with the name of the article from which the link is coming
            and the name of the article to which the link is going
    """
    # Create a dictionary of links with the index of the line as key
    # and the name of the article from which the link is coming and 
    # the name of the article to which the link is going as values
    dict_links = {}
    
    # Read the links file
    with open(path) as file:
        tsv_file = csv.reader(file, delimiter="\t")
        # Go through the lines of the file
        for j , line in enumerate(tsv_file):
            # Skip empty or commented lines 
            if len(line)==0 or line[0].startswith("#"):
                continue
            else : 
                # Add the link to the dictionary
                dict_links[j] = [line[0],line[1]]
    
    # Create a dataframe from the dictionary, entries are unique.
    return pd.DataFrame.from_dict(dict_links, orient='index', columns=['From', 'To'])

def update_links_df_position (links_df, truth_graph, html_base_path='data/wpcd/wp/'):
    """
    @param links_df: Pandas DataFrame, the dataframe of links between articles,
                    with the name of the article from which the link is coming
                    and the name of the article to which the link is going
    @param truth_graph : Object containing list of nodes and adjacency matrix
    @param html_base_path: String, the path to the html files

    @return: Pandas DataFrame, the dataframe of links between articles, 
            with the name of the article from which the link is coming
            and the name of the article to which the link is going
            and the position of the link in the article
    """

    # We are using a dynamic programming approach to avoid the list of links in an article several times
    # We keep the links of each article in a dictionary
    # The key is the name of the article and the value is the list of articles to which it is linked to
    # ordered by the order of apparition in the article
    linked_articles = {}

    def get_position(article1, article2, linked_articles=linked_articles):
        """
        @param article1: String, the name of the article from which the link is coming
        @param article2: String, the name of the article to which the link is going

        @return: List of Int, the positions of the link in the article and the number of links in the article
        """
        
        links = [] 

        # Check that both articles are part of the nodes of the graph 
        if article1 in truth_graph.articles and article2 in truth_graph.articles:
            # If the list of links of article1 is already computed, r
            if article1 in linked_articles:
                # return the positions of article2 in the list of links of article1, and the number of links in article1
                return  [i for i, x in enumerate(linked_articles[article1]) if x == clean_string(article2)],len(linked_articles[article1])

            # If the list of links of article1 is not computed, compute it
            try : 
                # Open the html file of article1
                with open(html_base_path+'{}/{}.htm'.format(article1[0],article1)) as fp:
                    soup = BeautifulSoup(fp, 'html.parser')

            except : 
                # If the file does not exist, return an empty list and 0 
                linked_articles[article1] = []
                return [],0

            # Search for all the links in the html file
            for link in soup.findAll('a'):
                href = link.get('href')
                # If the link is not None and starts with ../../wp/, it is a link to another article
                if  href !=None and href.startswith("../../wp/"):
                    # Get the name of the article to which the link is going
                    article = href.split("/")[-1].split(".")[0]
                    # add it to the list of links
                    links.append(article)

            #keep only links in existing in the truth graph 
            only = [link for link in links if link in truth_graph.matrix_articles[article1]]

            # Add the list of links to the dictionary (to avoid computing it several times)
            linked_articles[article1] = only

            # return the positions of article2 in the list of links of article1, and the number of links in article1
            return [i for i, x in enumerate(only) if x == clean_string(article2)], len(only)

    # For each link, get the positions (if it appears several times) or the position of the link in the article
    links_df[['positions','nb_links']] = links_df.apply(lambda row: pd.Series(get_position(row['From'],row['To']), dtype=object), axis=1)

def update_link_df_weights (links_df, cs_graph):
    """
    @param links_df: Pandas DataFrame, the dataframe of links between articles,
                    with the name of the article from which the link is coming
                    and the name of the article to which the link is going
                    and the postion of the link in the article
    @param cs_graph: Object containing list of nodes and adjacency matrix

    @return: Pandas DataFrame, the dataframe of links between articles, 
            with the name of the article from which the link is coming
            and the name of the article to which the link is going
            and the position of the link in the article
            and the weight of the link
    """
    # For each link, get the weight of the link in the graph
    links_df['weight'] = links_df.apply(lambda row: cs_graph.get_weight_of_link(row['From'],row['To']), axis=1)
    
# create a function that clean a string from each occurence of % and the 2 caracters after it
def clean_string(string):
    """
    @param string: String, the string to clean

    @return: String, the cleaned string
    """
    # Create a list of the occurences of % in the string
    occurences = [m.start() for m in re.finditer('%', string)]
    # For each occurence, remove the 2 caracters after it
    for occurence in occurences:
        string = string[:occurence] + string[occurence+3:]
    return string

def create_paths_finished_df(data_path = "data/paths_finished.tsv"):    
    # Create a df with path, start, end, length
    df_paths_finished = pd.DataFrame(columns=['path', 'start', 'end', 'length'])
    counter = 0
    discarded_paths = 0

    # Read the paths from the paths_finished.tsv file
    with open(data_path,encoding="utf8") as file:
                tsv_file = csv.reader(file, delimiter="\t")
                #For each line in the file
                for line in tsv_file:
                    # Skip empty or commented lines 
                    if len(line)==0 or line[0].startswith("#"):
                        continue
                    else:   
                        path = line[3].split(';')
                        # Discard paths that contain backclicks or Pikachu
                        if path.__contains__('<') or path.__contains__('Pikachu'):
                            discarded_paths += 1
                            continue
                        # Set the start node as the fist node in the path
                        start = path[0]
                        # Set the end node as the last node in the path
                        end = path[-1]
                        # Set the length of the path
                        length = len(path)
                        # Add the path to the dataframe
                        df_paths_finished.loc[counter] = [path, start, end, length]
                        counter += 1
    print("Discarded paths due to backclicks: ", discarded_paths)
    print("Number of paths retained: ", len(df_paths_finished))
    return df_paths_finished




    