from abc import ABC

class Vertex(ABC): 
    """Vertex class
    title : String, the title of the vertex
    neighbors_out : Dictionnar of neighbors, key is the title of the neighbor from which the link comes, 
                                            value is the number of times the link was encountred
    neighbors_in : Dictionnar of neighbors, key is the title of the neighbor to which the link goes,
                                             value is the number of times the link was encountred
    """
    def __init__(self,title):
        self.title = title
        self.neighbors_out = {}
        self.neighbors_in = {}

    """"
    Returns:
    The number of different outgoing neighbors
    """
    def get_nb_different_out_neighbours(self):
        return len(self.neighbors_out)
    
    """"
    Returns:
    The number of different incomming neighbors
    """
    def get_nb_different_in_neighbours(self):
        return len(self.neighbors_in)
    
    """"
    Returns:
    The sum of the weights of the outgoing neighbors
    """
    def get_total_out_weight(self):
        return sum(self.neighbors_out.values())
    
    """"
    Returns:
    The number of different incomming neighbors
    """
    def get_total_in_weight(self):
        return sum(self.neighbors_in.values())
    
    """
    Args:
    vertex : String, the vertex to add as a neighbor
    out : Boolean, True if the link is an outgoing one , False if it is an incoming one"""
    def update_neighbors(self,vertex,out=True):
        if out:
            # Update the number of outgoing links 
            if vertex not in self.neighbors_out :
                # If the category is not in the neighbors_out dict, add it
                self.neighbors_out[vertex] = 1
            else:
                # If the category is already in the neighbors_out dict, update the number of time the link was encountred 
                self.neighbors_out[vertex] += 1
        else:
            # Update the number of incoming links
            if vertex not in self.neighbors_in :
                # If the category is not in the neighbors_in dict, add it
                self.neighbors_in[vertex] = 1
            else:
                # If the category is already in the neighbors_in dict, update the number of times the link was encountred 
                self.neighbors_in[vertex] += 1



