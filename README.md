# Title: Bacteria at the world cup ! :scream:
(to be confirmed depending on least related topics obtained by the data)
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



**Step 1. Common Sense Graph construction:**
We aim to construct three directed Common Sense Graphs: Articles common sense graph, Categories common sense graph and  Topics common sense graph;

For that purpose,  we extract from the categories.tsv file the list of articles and we assign to each one of them a category and a topic.
We define as a category the last item of the categories list.
We define as a topic the most general category which means appearing first in the list of categories
The aforementioned represent the nodes of each graph.

In addition, we connect every two nodes $a$ and $b$ with a weighted edge $e$ where $weight(e) = number of distinct ways to go from a to b$
the list of edges is extracted from the finished and unfinished paths files (we take into consideration all the games).

**Step 2. Truth Graph:**

This graph has the same number of vertices as the Common Sense Graph but greater number of edges |E|
for E being the set of all possible explorable ways between subjects which are not necessarily logical for humans.

Common Sense Graph  VS  Truth Graph

![alt text](https://github.com/epfl-ada/ada-2022-project-groupe53/blob/main/output.png)

**Step3. Initial Analysis:**

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


We have additionally done some basic statistics to come up with numbers such as number of articles, edges, distribuition of articles among topics. 
This has shown that articles are not uniformly distributed across topics. 
From basic inspections, we have found that Geography is a potential hub that can be further studied in future analysis.
Indeed, the plot clearly indicates strong incoming links from all the topics to Geography.


Once we have done some basic exploratory analysis, we decide to compare the number of explored paths with the total number of possible paths 
by computing the fraction of nodes degrees and edges weights between the  two constructed dataframes.

In the future, we aim to compare the obtained fractions across categories and topics;
How does the percentage of a given topic exploration reflect the hottness of that topic ?
It is also interesting to analyse the effect of backclicks.
How can backclicks give us insights on subject properties (too general, too specific) ?


## Dropped Ideas: :x:
At some point of our discussions, we considered studying the played paths difficulty. However, we have decided that it was not relevant to answer 
the stated research questions. Furthermore, it is hard to avoid having a degree of bias when talking about difficulty given the presented dataset.

## Proposed timeline:   :calendar:                                                                                                                                                                          
**Milestone 2:** <br>
Week 8: Data extraction <br>
Week 9: Initial Analysis and ReadMe <br>
Week 10-11: Hw2 <br>
**Milestone 3:** <br>
Week 12: Complete Analysis <br>
Week 13: Data Story Wesbite creation <br>
 

## Organization within the team: :busts_in_silhouette:

Hichem Hadhri: Architecture, ReadMe <br>
Youssef Mamlouk: ReadMe and plot improvements <br>
Mehdi Mezghani: Architecture improvements, initial analysis <br>
Mehdi Sellami: Graph plots, initial analysis <br>
