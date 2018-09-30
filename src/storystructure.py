#!/usr/bin/env python
import pandas as pd

class node(object):
  """Bare bones node class
  """
  def __init__(self, id):
    self.id = id
    self.children = []

class digraph(object):
    """Directed graph class
    """
    def __init__(self, id):
      self.id = id
      self.nodes = {}
    def addEdge(self, sourceId, targetId):
      if sourceId not in self.nodes:
        self.nodes[sourceId] = node(sourceId)
      if targetId not in self.nodes:
        self.nodes[targetId] = node(targetId)
      self.nodes[sourceId].children.append(self.nodes[targetId])

class storystructure(object):
  """python tools for analysing story structures
  """
  __version__ = "0.0.2"
  def __init__(self):
    self.edgelist = pd.DataFrame()
    self.nodeAttributes = pd.DataFrame()
    self.colors = {
      'goodColor'  : "#7aa457", # green
      'pauseColor' : "#9e6ebd", # violet
      'badColor'   : "#cb6751" # red
    }

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

  def saveDot(self, fileName, graphName = "myGraph"):
    """Save edgelist in dot format
       Args:
         filePath (string):
         dot ../data/file.dot -Tpng > ../figs/file.png
    """
    with open(fileName, 'w') as f:
      f.write("digraph " + graphName +" {")
      for line in self.nodeAttributes.itertuples():
        if line.attribute == "pause":
          color = self.colors['pauseColor']
        elif line.attribute == "good":
          color = self.colors['goodColor']
        elif line.attribute == "bad":
          color = self.colors['badColor']
        else:
          print("Unknown attribute " + line.attribute)
        f.write('{} [style=filled, fillcolor = "{}"];'.format(line.node, color))
      for edge in self.edgelist.itertuples():
        f.write(str(edge.source) + ' -> ' + str(edge.target) + ';')
      f.write('}')
