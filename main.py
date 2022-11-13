
from graph import Graph
import csv

graph  = Graph()


##Part 1 : read the articles category file 
## for each article initialize the article 
## and add it to the graph (with the same function we initialize the categories and topics)
with open("data/categories.tsv") as file:
    tsv_file = csv.reader(file, delimiter="\t")
    for line in tsv_file:
        print(line)

### this will create all categories , articles and topics  and put them in the graph





##Part 2 : read the paths file 
# for each path 
#loop on articles and create edges between Article.category i and Article.category i+1
#using the add_edge function in graph.py




#After this step we should have a complete common sense graph 


####TODO : nzidou topics fel eeja 



###After this step we can do the analysis