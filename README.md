# Title: Disover your web instincts ! :mag:
(to be confirmed depending on least related topics obtained by the data)


## Data story
to understand your web instincts, Check this out : add_site_here


## Abstract: :page_with_curl:
The Way We Think Everything Is Connected Isn’t the Way Everything Is Connected.
By exploring the Wikispeedia dataset, a human-computation game in which users are asked to navigate from a given source to a given target article, by only clicking Wikipedia links, we aim to derive people common sense when it comes to subject relations. 

## Research questions: :question:
In this project, we will try to answer the following questions:
- What are the subjects people are most comfortable with ?
- How common sense knowledge influence the way people link subjects together?
- What makes a subject a hub or an authority ?
- How can we use this knowledge to improve the way we navigate through the web ?


## Methods: :hammer:


### Data structure and preprocessing: 
 ***Extracting Data:***



**Step 1. Common Sens and truth Graph construction:**
We aim to construct two directed Graphs from the dataset : 
- The Common Sense Graph
- The Truth Graph
  
The graphs will be constructed on three different levels  : 
- Articles
- Categories
- Topics

The latter two are extracted from the categories.tsv file and are constructed for visualization purposes.


  
`The common sense graph`: It represents the links clicked on by the players as edges and the discovered articles (topics, categories) as vertices.
The graph is directed and weighted. The weight of an edge is the number of times it has been clicked on by the players. <br>
`The truth graph`: It represents the links that are logically possible as edges and the discovered articles (topics, categories) as vertices.
This graph is not weighted and is directed.




 We connect every two articles $a$ and $b$ with a weighted edge $e$ where $weight(e) = number of times to go from a to b$
the list of edges is extracted from the finished and unfinished paths files (we take into consideration all the games).


The truth graph has the same number of vertices as the Common Sense Graph but greater number of edges |E|
for E being the set of all possible lniks between articles which are not necessarily logical for humans, as explained in the datastory.

Common Sense Graph  VS  Truth Graph

![alt text](https://github.com/epfl-ada/ada-2022-project-groupe53/blob/main/output.png)

**Step2. Initial Analysis:**

From each graph, we contruct a dataframe with the following columns:

| Column name          | Description                                                                                                                                                                                       |   
|----------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Topic           | The topic of the vertex (Not valid for the Topic df)                                                                                                                                    |
| Category            | The category of the vertex (Not valid for the Topic df nor the the Category Df)                                                                      |
| out-degree          | The number of different articles/topics/catagories to which users went from this article/topic/catagory      |
| in_degree          | The number of different articles/topics/catagories from which users ended up in this article/topic/catagory    |
| degree            | Sum of nb_unique_outgoing_edges and nb_unique_incoming_edges            |
| total_weight_out        | Sum of the weights of the outgoing edges     |
| total_weight_in        | Sum of the weights of the incoming edges      |
| total_weight        | Sum of the weights of the incoming and outgoing edges       |
| average_weight_out        | The average weight of an outgoing edge      |
| average_weight_in       | The average weight of an incoming edge     |
| average_weight       | The average weight of an incoming or outgoing edge      |
| nb_articles       |   The number of articles in the Vertex (Not valid for articles)    |
| nb_categories       | The number of categories contained in the Vertex (Not valid for Articles and Categories df)   |


We have additionally done some basic statistics to come up with numbers such as number of articles, edges.<br>

We have found that the players did not explore all the articles in the dataset (? missed articles). <br>
The unreached articles contain 2% of the total number of links in the truth graph. 

However, we have found that the players only clicked on 48% of the links in the dataset.<br> Adding that to the above finding, we can conclude that the players only explored half of the links thay seen.<br>


## In our datastory, we try to understand why is it the case. <!-- insert emoji --> :thinking: 
Our analysis will be divided into 5 parts :
- Part 1: Introduction to the dataset
- Part 2: Semantics Analysis
  - Comparison of semantic similarities between human and optimal paths
  - Node centrality analysis
- Part 3: Influence of graph architecture on people's behaviour
  - Position of links in article
  - Number of links in article
- Part 4: Case study : Missed mate in one
- Part 5: Conclusion
<br>


## Requirements (external Libraries): :wrench:
- BeautifulSoup
- sentence_transformers
## Dropped Ideas: :x:
At the end of milestone 2, our datastory was originally about exploring the relationship between the topics and categories and how do people link between them and use that skill to play the game.<br>
However, we have decided to move on past that, as we found that the data was not sufficient to answer the questions we had in mind, and we believe we have a clearer and more feasable datastory now.

## Proposed timeline:   :calendar:                                                                                                                                                                          
**Milestone 2:** <br>
Week 8: Data extraction <br>
Week 9: Initial Analysis and ReadMe <br>
Week 10-11: Hw2 <br>
**Milestone 3:** <br>
Week 12: Complete Analysis <br>
Week 13: Grouping Analysis <br>
Week 14: Website creation <br>

## Organization within the team: :busts_in_silhouette:

Hichem Hadhri: Architecture, ReadMe , initial analysis , parts of analysis (2,3) <br>
Youssef Mamlouk: plot improvements , initial analysis , analysis (4), interactive plots <br>
Mehdi Mezghani: Architecture improvements, initial analysis , analysis (3), website design , notebook refactoring <br>
Mehdi Sellami: Graph plots, website creation, script writing, proof check <br>


### With Love, groupe53.
