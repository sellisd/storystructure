#!/usr/bin/env python
import pandas as pd

class node(object):
  """Bare bones node class
  """
  def __init__(self, id, parent):
    self.id = id
    self.children = []
    self.parent = parent

class digraph(object):
    """Directed graph class
    """
    def __init__(self, id):
      self.id = id
      self.nodes = {}
      self.root = None
      self.roots = []

    def addEdge(self, sourceId, targetId):
      if sourceId not in self.nodes:
        self.nodes[sourceId] = node(sourceId, None)
      if targetId not in self.nodes:
        self.nodes[targetId] = node(targetId, self.nodes[sourceId])
      self.nodes[targetId].parent = self.nodes[sourceId]
      self.nodes[sourceId].children.append(self.nodes[targetId])

    def findRoots(self):
      """Find the root node(s) of the digraph.
      """
      for nodeId in self.nodes:
        if self.nodes[nodeId].parent is None:
          self.roots.append(self.nodes[nodeId])
        else:
          continue

    def setRoot(self, root):
        """Set the root node of the digraph
        Args
          root (node) arbitrary node to be used as root
        """
        self.root = root

class storystructure(object):
  """python tools for analysing story structures
  """
  __version__ = "0.0.2"
  def __init__(self, title = "my story"):
    self.edgelist = pd.DataFrame()
    self.nodeAttributes = pd.DataFrame()
    self.colors = {
      'goodColor'  : "#7aa457", # green
      'pauseColor' : "#9e6ebd", # violet
      'badColor'   : "#cb6751" # red
    }
    self.graph = digraph(title)

  def getStart(self):
    """Get beginning storylet (root of digraph)
    """
    return(self.graph.roots)

  def loadEdgelist(self, filePath):
    """Load edgelist file
       Args:
        filePath (string):
    """
    self.edgelist = pd.read_csv(filePath)

  def loadNodeAttributes(self, filePath):
    """Load file with node attributes
       Args:
         filePath (string):
    """
    self.nodeAttributes = pd.read_csv(filePath)

  def loadStory(self, edges, nodes):
    """Load story files and create data structure
       Args:
         edges (string) Path and filename of edgelist file (csv)
         nodes (string) Path and filename of node attributes file (csv)
    """
    self.loadEdgelist(edges)
    self.loadNodeAttributes(nodes)
    self.edgelist.drop_duplicates(); # Multigraph to simple graph (peinasmeni nistiki arkouda)
    for edge in self.edgelist.itertuples():
      if edge.source != edge.target: #skipp self-loops
        self.graph.addEdge(edge.source, edge.target)
    self.graph.findRoots() # set the root

  def saveDot(self, fileName, graphName = "myGraph"):
    """Save edgelist in dot format
       Args:
         filePath (string):
         dot ../data/file.dot -Tpng > ../figs/file.png
    """
    with open(fileName, 'w') as f:
      f.write("digraph " + graphName +" {\n")
      for line in self.nodeAttributes.itertuples():
        if line.attribute == "pause":
          color = self.colors['pauseColor']
        elif line.attribute == "good":
          color = self.colors['goodColor']
        elif line.attribute == "bad":
          color = self.colors['badColor']
        else:
          print("Unknown attribute " + line.attribute)
        f.write('{} [style=filled, fillcolor = "{}"];\n'.format(line.node, color))
      for edge in self.edgelist.itertuples():
        f.write(str(edge.source) + ' -> ' + str(edge.target) + ';\n')
      f.write('}\n')

  def depth_first(self, root, path):
    path.append(root.id)
    if root.children:            #this is not a leaf
      for child in root.children:
        if child.id not in path:
          self.depth_first(child, path)
          path.pop()
        else:
          print("Skipped descending into {} to avoid cycles".format(child.id))
    else:
      self.pathStatistics(path)

  def pathStatistics(self, path):
    badEndings = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="bad","node"]
    goodEndings = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="good","node"]
    pause = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="pause","node"]
    pathId = path.pop()
    pathLength = len(path)
    endNode = path[-1]
    if endNode in goodEndings:
      endType = "good"
    elif endNode in badEndings:
      endType = "bad"
    else:
      print("Error: Nodelist and edgelist do not match!")
    numberOfPause = 0
    stepsToFirstPause = None
    for i, node in enumerate(path):
      if node in pause:
        if stepsToFirstPause is None:
          stepsToFirstPause = i
          numberOfPause += 1
    print("\t".join(pathId, pathLength, endType, numberOfPause, stepsToFirstPause))
