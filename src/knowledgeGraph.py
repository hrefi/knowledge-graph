import networkx as nx
import matplotlib.pyplot as plt

class KnowledgeGraph:
   def __init__(self, relationships):
      """
      Parameters:
         relationships (list of dicts): Each dictionary should contain 'src', 'tgt', and 'relationship' keys.
      """
      # self.__graph = nx.DiGraph()
      self.__graph = nx.MultiDiGraph()
      self.__build_knowledge_graph(relationships)

   @property
   def graph(self):
      return self.__graph

   def __build_knowledge_graph(self, relationships):
      for rel in relationships:
         self.add_entity(rel['src'])
         self.add_entity(rel['tgt'])
         self.add_relationship(rel['src'], rel['tgt'], rel['relationship'])

   def add_entity(self, entity):
      self.__graph.add_node(entity)

   def add_relationship(self, source, target, relationship):
      self.__graph.add_edge(source, target, relationship=relationship)


class KnowledgeGraphVisualizer:
   def __init__(self, knowledge_graph: KnowledgeGraph):
      self.knowledge_graph = knowledge_graph

   def aggregate_edge_labels(self, multigraph):
      """Aggregate multiple edges between two nodes into a single edge with a combined label.
      
      Parameters:
         multigraph (nx.MultiDiGraph): The graph containing potentially multiple edges between nodes.
      """
      simplified_graph = nx.DiGraph()

      # For each unique edge, combine labels if there are multiple edges
      for u, v, data in multigraph.edges(data=True):
         if simplified_graph.has_edge(u, v):
            simplified_graph[u][v]['relationship'] += ',\n' + data['relationship']
         else:
            simplified_graph.add_edge(u, v, relationship=data['relationship'])

      return simplified_graph

   def visualize(self, with_labels=True, node_size=6000, highlight_size=12000, node_color="#9ecae1", highlight_color="#6baed6", edge_color="lightgrey", font_color="#0c1a26", font_size=10, highlight_entities=[], num_nodes=None):
      """
      Visualizes the knowledge graph using matplotlib.

      Parameters:
         with_labels (bool): Whether to draw labels on the nodes.
         node_size (int): The size of the nodes.
         highlight_size (int): The size of highlighted nodes.
         node_color (str): The color of the nodes.
         highlight_color (str): The color for highlighted nodes.
         edge_color (str): The color of the edges.
         font_color (str): The color of the font for node labels.
         font_size (int): The font size for node labels.
         highlight_entities (list of str): Nodes to highlight.
         num_nodes (int or None): If specified, limits the graph to the first num_nodes nodes.
      """
      # Aggregate edge labels for multigraph
      simplified_graph = self.aggregate_edge_labels(self.knowledge_graph.graph)
      # If 'num_nodes' is specified, visualize a subgraph only with the first 'num_nodes' nodes
      if num_nodes is not None:
         num_nodes = int(num_nodes)
         if 1 < num_nodes and num_nodes < simplified_graph.number_of_nodes():
            nodes = list(simplified_graph.nodes())[:num_nodes]
            simplified_graph = simplified_graph.subgraph(nodes)

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

