import argparse
import sys
import csv
import re
import geopy
import pickle
import shelve
from geopy import distance
import networkx as nx
import matplotlib.pyplot as plt

# Loads a csv road netowrk file, returns networkx digrpah
def create_graph(input_path):
  # Create new graph
  G = nx.DiGraph()
  # To grab points from WKT linestring
  geopoint_re = re.compile("(-?\d+.\d+) (-?\d+.\d+)")
  # Open input csv file
  with open(input_path) as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
      wkt_string = row['WKT']
      bidirectional = (row['DIR_CODE'] == 'B')
      forward = bidirectional or (row['DIR_CODE'] == 'F')
      points = re.findall(geopoint_re, wkt_string)
      # If r.e. found some points in string
      if points:
          line = [geopy.Point(float(point[1]), float(point[0])) for point in points]
      # If its a reverse line, reverse points in line list
      if (not forward):
        line.reverse()
      # Calc dist between line nodes, and add as weights to edges
      for i in range(len(line)-1):
        dist = distance.distance(line[i], line[i+1]).m
        G.add_edge(str(line[i]), str(line[i+1]), weight=dist)
        # IF bidirectional line, add reversed pair
        if bidirectional:
          G.add_edge(str(line[i+1]), str(line[i]), weight=dist)
  return G

# Stores graph on disk at path
def pickle_graph(graph, path):
  nx.write_gpickle(graph, path)

# Load graph from path
def load_pickled_graph(path):
  return nx.read_gpickle(path)

# Draw graph
def draw_graph(G):
# # add pseudo pos for vis. purposes
  fp = geopy.Point(G.nodes()[0])
  scale = 100000
  for n in G:
    p = geopy.Point(G.node[n])
    G.node[n]['pos'] = ((p.longitude - fp.longitude) * scale, (p.latitude - fp.latitude) * scale)
  # Grab newly created pos attr. 
  pos=nx.get_node_attributes(G,'pos')
  # Set up matplotlib plot
  plt.figure(figsize=(16,16))
  nx.draw_networkx_nodes(G, pos, node_size=8, cmap=plt.cm.Reds_r)
  nx.draw_networkx_edges(G, pos, alpha=0.4)
  # Set bounds
  plt.xlim(-1500,1500)
  plt.ylim(-1500,1500)
  # Turn off axes and render
  plt.axis('off')
  plt.show()

# Takes two geopoints, returns path- list of node names (str(geopoint))
# If points aren't in network closest nodes will be used
def get_path(start, end, graph):
  search_points = [get_closest_node(node, graph) for node in [start, end]]
  path = nx.shortest_path(graph, source=search_points[0], target=search_points[1])
  if (path[0] != str(start)):
    path = [str(start)] + path
  if (path[-1] != str(end)):
    path.append(str(end))
  return path

# Prints the path nicely
def print_path(start, end, path):
  start_str = " " + start + " >>> " + end + " "
  line_str = "_"*len(start_str)
  print line_str + '\n\n' + start_str + '\n' + line_str + '\n'
  for i, node in enumerate(path):
    print str(i+1).rjust(3) + ".   " + node
  print line_str + '\n'

# Find closest node in graph, returns node name
# Graph must have geopoints on nodes
def get_closest_node(point, graph):
  if (str(point) in graph):
    return str(point)
  min_dist = float('Inf')
  min_node = graph.nodes()[0]
  for n in graph:
    dist = distance.distance(point, geopy.Point(graph.node[n])).m 
    if (dist < min_dist):
      min_dist = dist
      min_node = n
  return min_node


def main():
  parser = argparse.ArgumentParser(description="Parse CSV into graph, or find path")
  parser.add_argument('-p','--pickle', help='Path to graph pickle, either to be generated or read', required=True)
  parser.add_argument('-c','--csv', help='Path to csv file to parse', required=False)
  args = vars(parser.parse_args())

  csv_path = args['csv']
  pickle_path = args['pickle']
  
  # Make graph and save to disk
  if(csv_path != None):
    G = create_graph(csv_path)
    pickle_graph(G, pickle_path)

  # Load in graph, and print a sample path
  else:
    G = load_pickled_graph(pickle_path)

    a = geopy.Point(-37.816472, 144.964888)
    b = geopy.Point(-37.808551, 144.968525)
    print_path(str(a), str(b), get_path(a, b, G))
    # draw_graph(G)
    
if __name__ == "__main__":
    main()
