import networkx as nx
import matplotlib.pyplot as plt
from modulegraph.modulegraph import ModuleGraph

# Create a ModuleGraph instance
graph = ModuleGraph()

# Add your script's path
graph.run_script('main.py')

# Create a networkx graph
nx_graph = nx.DiGraph()
for node in graph.nodes():
    for edge in graph.get_edges(node):
        nx_graph.add_edge(node.identifier, edge.identifier)

# Draw the graph
plt.figure(figsize=(12, 12))
pos = nx.spring_layout(nx_graph)
nx.draw(nx_graph, pos, with_labels=True, node_size=500, font_size=8)
plt.show()
