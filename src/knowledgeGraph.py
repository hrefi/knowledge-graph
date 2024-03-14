import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
   def __init__(self, entities, relationships):
      self.__graph = nx.MultiDiGraph()
      # self.__graph = nx.DiGraph()
      self.__build_knowledge_graph(entities, relationships)

   @property
   def graph(self):
      return self.__graph

   def __build_knowledge_graph(self, entities, relationships):
      for entity in entities:
         self.add_entity(entity)
      # Relationships should be in format (src, tgt, relationship)
      for src, tgt, relationship in relationships:
         self.add_relationship(src, tgt, relationship)
      
      # # Add nodes and edges with relationships as attributes
      # for src, tgt, relationship in relationships:
      #    self.add_entity(src)
      #    self.add_entity(tgt)
      #    self.add_relationship(src, tgt, relationship=relationship)

   def add_entity(self, entity):
      self.__graph.add_node(entity)

   def add_relationship(self, source, target, relationship):
      self.__graph.add_edge(source, target, relationship=relationship)


class KnowledgeGraphVisualizer:
   def __init__(self, knowledgeGraph: KnowledgeGraph):
      self.knowledgeGraph = knowledgeGraph

   def aggregate_edge_labels(self, multigraph):
      """Aggregate multiple edges between two nodes into a single edge with a combined label"""
      simplified_graph = nx.DiGraph()

      # For each unique edge, combine labels if there are multiple edges
      for u, v, data in multigraph.edges(data=True):
         if simplified_graph.has_edge(u, v):
            simplified_graph[u][v]['relationship'] += ',\n' + data['relationship']
         else:
            simplified_graph.add_edge(u, v, relationship=data['relationship'])

      return simplified_graph

   def visualize(self, with_labels=True, node_size=6000, highlight_size=12000, node_color="#9ecae1", highlight_color="#6baed6", edge_color="lightgrey", font_color="#0c1a26", font_size=10, highlight_entities=[]):
      # Aggregate edge labels for multigraph
      simplified_graph = self.aggregate_edge_labels(self.knowledgeGraph.graph)

      # Highlight any nodes/entities (change color and size) if specified
      color_map = [highlight_color if node in highlight_entities else node_color for node in simplified_graph]
      size_map = [highlight_size if node in highlight_entities else node_size for node in simplified_graph]
      
      # Generate positions for all nodes
      pos = nx.spring_layout(simplified_graph) # alternatively: circular_layout
      plt.figure(figsize=(10, 10))
      
      # Draw nodes and edges
      nx.draw(simplified_graph, pos, with_labels=with_labels, node_size=size_map, node_color=color_map, edge_color=edge_color, font_size=font_size, font_weight="bold", width=3, arrowstyle="-|>", arrowsize=20) # arrows = True, alpha = 0.6
      
      # Draw edge labels
      edge_labels = nx.get_edge_attributes(simplified_graph, 'relationship')
      nx.draw_networkx_edge_labels(simplified_graph, pos, edge_labels=edge_labels, font_color=font_color)
      
      # plt.axis('off')
      plt.show()


# If you are going to add a visualization with GraphViz (you need to install the Graphviz software first), 
# define a (abstract) base class for visualization and then implement separate subclasses for NetworkX and Graphviz visualizers


"""Additional Information
draw_networkx_edge_labels does not support drawign graphs with multiple edges/labels between two nodes.

There are 3 options:
   1. Simply use `DiGraph` (or `Graph`), but you lose the ability to have multiple relationships between two entities
   2. Aggregate multiple edges into a single edge with a combined label
   3. Use a different visualization library, e.g. GraphViz

We have adopted the second approach here, but it's worth checing out other visualization libraries
"""

"""Future Improvements
We could add a type to each entity, e.g. "organization", "person", "club", "university", "location", etc.

Additionally, the visualization can be implemented to be dynamic and interactive, e.g. by using D3.js.
This may allow many improvements, particularly if the UX is designed in a way that can interact/communicate with
the AI Agent API to provide and update information on the screen.
The following are suggestions for additional features: 
   - Users can select a relationship to get more elaborate information about it from the Agent, e.g. ...
   - Users can select an entity and ask the LLM to generate all of its most relevant relationships and add tem to the graph
   - Users can seelct which relationships or entities are not relevant and instruct the Agent to remove them from the graph for more clarity
   - Users can move around nodes of the graph for clarity
"""
