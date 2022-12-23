from bs4 import BeautifulSoup
import pandas as pd
import random
import csv 
import re 
import numpy as np

################################################### Functions to generate and update the links dataframe ###################################################

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

################################################### Function to generate the finished and optimal paths dataframe ###################################################

def create_paths_finished_df(data_path = "data/paths_finished.tsv"):    
    """
    @param data_path: String, the path to the paths_finished.tsv file

    @return: Pandas DataFrame, the dataframe of paths between articles,
            with the name of the article from which the path is coming
            and the name of the article to which the path is going
            and the length of the path
    """
    
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

def dijkstra(adj, source, destination):
    """
    @param adj: Dictionary, the adjacency matrix of the graph
    @param source: String, the name of the source node
    @param destination: String, the name of the destination node

    @return: List, the shortest path between the source and the destination
    """
    try:
        #create a dictionary to store the distances of each node from the source
        distances = {}
        #create a dictionary to store the previous node of each node
        previous = {}
        #create a list of the nodes that have been visited
        visited = []
        #create a list of the nodes that have not been visited
        unvisited = []
        #create a list of the nodes that have not been visited
        for node in adj:
            #initialize the distance of each node to infinity
            distances[node] = float("inf")
            #initialize the previous node of each node to None
            previous[node] = None
            #add the node to the unvisited list
            unvisited.append(node)
        #set the distance of the source to 0
        distances[source] = 0
        #while the unvisited list is not empty
        while unvisited:
            #sort the unvisited list by the distance of each node from the source
            unvisited.sort(key=lambda node: distances[node])
            #get the node with the smallest distance from the source
            current_node = unvisited.pop(0)
            #add the node to the visited list
            visited.append(current_node)
            #if the current node is the destination
            if current_node == destination:
                #create a list to store the shortest path
                path = []
                #while the current node is not the source
                while current_node != source:
                    #add the current node to the path
                    path.append(current_node)
                    #set the current node to the previous node
                    current_node = previous[current_node]
                #add the source to the path
                path.append(source)
                #reverse the path
                path.reverse()
                #return the path
                return path
            #for each neighbor of the current node
            for neighbor in adj[current_node]:
                #if the neighbor has not been visited
                if neighbor not in visited:
                    #calculate the distance of the neighbor from the source
                    new_distance = distances[current_node] + 1
                    #if the distance of the neighbor from the source is smaller than the current distance
                    if neighbor in distances and new_distance < distances[neighbor] :
                        #update the distance of the neighbor from the source
                        distances[neighbor] = new_distance
                        #update the previous node of the neighbor
                        previous[neighbor] = current_node

    #if the destination is not reachable from the source          
    except:
        pass
    return [] 

################################################### Function to interpolate function from points  ###################################################

def get_intrapolation(number, lista):
    """
    @param number: Integer, the number of samples to get from interpolation
    @param lista: List, the list of numbers to interpolate from


    @return: List, the interpolated list
    """
    # Maps the input list to a list of percentages from 0 to 1
    def map_to_percentage (row):
        return [i/(len(row)-1) for i, x in enumerate(row)]

    # Finds the indices of the elements in the list before and after the given number
    def get_index_before_after (number, lista):
        for i in range(len(lista)):
            if lista[i] > number:
                return i-1, i
        # If the number is greater than the last element in the list, 
        # return the index of the last element for both the element before and after
        return len(lista)-1, len(lista)-1

    # Map the input list to a list of percentages
    percentage_list = map_to_percentage(lista)
    result = []
    # Iterate over a range of numbers from 0 to the input number
    for i in range(number+1):
        # Find the indices of the elements in the list before and after the current number
        index_before, index_after = get_index_before_after(i/number, percentage_list)
        # If the elements before and after are the same, 
        # the intrapolated value is simply the value of that element
        if lista[index_after] == lista[index_before]:
            value = lista[index_after]
            result.append(round(value,2))
        # If the elements before and after are different, 
        # perform linear intrapolation using these elements
        else :
            value = ((lista[index_after] - lista[index_before])/(percentage_list[index_after]-percentage_list[index_before])) * (i/number-percentage_list[index_before])+ lista[index_before]
            result.append(round(value,2))
    # Return the list of intrapolated values
    return result

def get_intrapolation_mean (number , lista ):
    return round(np.mean(get_intrapolation(number, lista))*100)

def shufle_dico (dico):
    keys = list(dico.keys())
    random.shuffle(keys)

    ShuffledStudentDict = dict()
    for key in keys:
        ShuffledStudentDict.update({key: dico[key]})
    return ShuffledStudentDict

############################################### 
def convert_paths_to_df (source_df,similarity="article_similarity" ):
    # create a df to store percentage_path and article_similarity
    test = pd.DataFrame(columns=['percentage_path', similarity])
    # for each entry in df_paths_finished_filter_game
    counter = 0
    for index, row in source_df.iterrows():
        path = row[similarity]
        # for each value in article_similarity
        for i in range(len(path)):
            # add a new entry in df_paths_finished_filter_game_percentage
            test.loc[counter] = [i, path[i]]
            counter += 1
    return test


################################################### Function is used to create a dataframe with the vertices of a given level  ###################################################


#Level can be "articles", "categories" or "topics"
def vertices_to_df(graph, level):
    #Check that the level is valid
    assert level in graph.authorized_levels
    #Get the vertices of the given level
    _, verteces = graph.levels_map[level]
    #Create the header of the dataframe
    header =["Topic", "Category", "degree", "out_degree", "in_degree", "total_weight" ,"total_weight_out", "total_weight_in","average_weight_per_edge", "average_weight_out", "average_weight_in"]  
    #Remove the columns that are not relevant for the given level
    if level == "categories":
        header.remove("Category")
        header.append("nb_articles")
        header.append("nb_seen_articles")
    if level == "topics":
        header.remove("Topic")
        header.remove("Category")
        header.append("nb_categories")
        header.append("nb_articles")
        header.append("nb_seen_articles")
    
    df = pd.DataFrame(columns=header)
    
    #Fill the dataframe with the vertices
    for vertex in verteces.values():
        nb_unique_outgoing_edges = vertex.get_nb_different_out_neighbours()
        nb_unique_incoming_edges = vertex.get_nb_different_in_neighbours()
        nb_unique_edges = nb_unique_outgoing_edges + nb_unique_incoming_edges

        #We only keep the vertices that have at least one edge
        if (nb_unique_edges != 0) :
            total_weight_out = vertex.get_total_out_weight()
            total_weight_in = vertex.get_total_in_weight()
            total_weight = total_weight_out + total_weight_in
            average_weight_out = round(total_weight_out/nb_unique_outgoing_edges, 2) if nb_unique_outgoing_edges != 0 else 0
            average_weight_in = round(total_weight_in/nb_unique_incoming_edges,2) if nb_unique_incoming_edges != 0 else 0
            average_weight_per_edge = round(total_weight/nb_unique_edges, 2)

            if level == "articles":
                df.loc[vertex.title] = [vertex.topic, vertex.category, nb_unique_edges, nb_unique_outgoing_edges, nb_unique_incoming_edges, total_weight, total_weight_out, total_weight_in, average_weight_per_edge, average_weight_out, average_weight_in]
                df["Topic"].astype("category")
                df["Category"].astype("category")
            elif level == "categories":
                df.loc[vertex.title]= [vertex.topic, nb_unique_edges, nb_unique_outgoing_edges, nb_unique_incoming_edges, total_weight, total_weight_out, total_weight_in, average_weight_per_edge, average_weight_out, average_weight_in, vertex.get_nb_different_articles(),vertex.get_nb_seen_articles()]
                df["Topic"].astype("category")
            else:
                df.loc[vertex.title]= [nb_unique_edges, nb_unique_outgoing_edges, nb_unique_incoming_edges, total_weight, total_weight_out, total_weight_in, average_weight_per_edge, average_weight_out, average_weight_in, vertex.get_nb_different_categories(), vertex.get_nb_different_articles(),vertex.get_nb_seen_articles()]
    return df

################################################### Function that draws the graph given a dataframe ###################################################

def draw_graph (graph, df_topics):
    n = len(df_topics)
    #set colors of a palette
    color = sns.color_palette('dark', n)

    labels = list(graph.topics.keys())
    #Map each category to a color
    color_map = {category: color[i] for i, category in enumerate(graph.topics.keys())}

    G1 = nx.DiGraph()
    #Add the edges to the graph
    for key, value in graph.matrix_topics.items():
        for key2, value2 in value.items():
                G1.add_edge(key,key2,weight=value2, color=color_map[key])

    #Add the nodes to the graph
    color = []
    for node in G1.nodes(): 
        color.append(color_map[node])

    #Add the labels to the graph
    #set node text to white
    label_dict = {}
    for i in range(len(labels)):
        label_dict[labels[i]] = labels[i]


    edges = G1.edges()
    weights = [G1[u][v]['weight']/250 for u,v in edges]
    colors = [G1[u][v]['color'] for u,v in edges]

    #Nodes positions settings
    nodePos = nx.circular_layout(G1)
    nodePos['People'] = [ -0.5, 0]
    nodePos['Citizenship'] = [0.5,0]
    nodePos['Geography'] = [0,0.1]
    nodePos['Science'] = [-0.5,0.5]
    nodePos['Everyday_life'] = [-0.75,0.25]
    nodePos['History'] = [0,0.5]
    nodePos['Countries'] = [0.3,0.3]
    nodePos['Design_and_Technology'] = [0,-0.3]
    nodePos['Language_and_literature'] = [-0.3,-0.3]
    nodePos['Religion'] = [0.1,-0.1]
    nodePos['Mathematics'] = [0,-0.4]
    nodePos['Art'] = [-0.5,-0.4]
    nodePos['IT'] = [-0.90,0]
    nodePos['Music'] = [0.5,-0.4]
    nodePos['Business_Studies'] = [0.3,-0.3]

    #Set nodes sizes
    size = [df_topics.loc[t_name].nb_seen_articles*25 for t_name in nx.nodes(G1)]
      
    nx.draw_networkx(G1,node_size = size,pos = nodePos,node_color = color,labels=label_dict, 
                    width= weights, edge_color=colors, arrows=True, arrowstyle='->',arrowsize=20, 
                    font_size=15, font_color='white', font_weight='bold', font_family='sans-serif', 
                    alpha=1.0, bbox=None, ax=None, with_labels=True, edgecolors='black', node_shape='o', 
                    connectionstyle='arc3, rad=0.1', min_source_margin=0.05)
