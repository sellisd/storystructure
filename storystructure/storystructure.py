"""
.. module:: storystructure
   :synopsis: A python3 module to analyze the story structure of branching books.
"""

import json
from itertools import combinations
from pathlib import Path
import random
from shutil import copyfile
from subprocess import call
import sys
import tempfile

import numpy as np
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
        """Set the root node of the digraph.
        Args:
          root (node): Arbitrary node to be used as root.
        """
        self.root = root

class storystructure(object):
    """Python tools for analysing story structures
    """
    __version__ = "0.0.3"
    def __init__(self, title = "my story"):
        self.edgelist = pd.DataFrame(columns = ['source','target'])
        self.nodeAttributes = pd.DataFrame(columns=['node','attribute'])
        self.colors = {
          'goodColor'  : "#7aa457", # green
          'pauseColor' : "#9e6ebd", # violet
          'badColor'   : "#cb6751" # red
        }
        self.graph = digraph(title)
        self.paths = {}
        self.pathCounter = 0

    def getStart(self):
        """Get beginning storylet (root of digraph).
        """
        return(self.graph.roots)

    def loadEdgelist(self, filePath):
        """Load edgelist file.
           Args:
            filePath (string): Path and file name.
        """
        self.edgelist = pd.read_csv(filePath)

    def loadNodeAttributes(self, filePath):
        """Load file with node attributes.
           Args:
             filePath (string): File and path name.
        """
        self.nodeAttributes = pd.read_csv(filePath)

    def loadStory(self, edges = None, nodes = None):
        """Load story files and create data structure.
           Args:
             edges (string): Path and filename of edgelist file (csv).
             nodes (string): Path and filename of node attributes file (csv).
        """
        if edges is not None:
            self.loadEdgelist(edges)
        if nodes is not None:
            self.loadNodeAttributes(nodes)

    def simplify(self):
        """Simplify graph.

        Simplify graph by:
           * Removing self loops
           * Removing double edges (multigraph to simple graph)
        """
        self.edgelist = self.edgelist.drop_duplicates() # Multigraph to simple graph (peinasmeni nistiki arkouda)
        self.edgelist = self.edgelist[self.edgelist['source'] != self.edgelist['target']]

    def getDuplicates(self):
        """Get double edges from a multigraph.

        Returns: Dataframe of duplicate edges.
        """
        return(self.edgelist[self.edgelist.duplicated()])

    def getSelfloops(self):
        """Get self loops.
        """
        self.edgelist[self.edgelist['source'] == self.edgelist['target']]

    def makeGraph(self):
        """From edgelist and node attributes create graph object.
        """
        for edge in self.edgelist.itertuples():
            self.graph.addEdge(edge.source, edge.target)
        self.graph.findRoots() # set the root
        # guess the correct root, should be the one with the smallest value
        self.graph.root = min([i.id for i in self.graph.roots])

    def saveDot(self, fileName, graphName = "myGraph", noSingle = False):
        """Save edgelist in dot format.

        Args:
           filePath (string): Path and file name of dot file.
           noSingle (bool):   If true remove any unconected single nodes and keep a single connected component
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
                    print("Unknown attribute " + line.attribute, file=sys.stderr)
                f.write('{} [style=filled, fillcolor = "{}"];\n'.format(line.node, color))
            for edge in self.edgelist.itertuples():
                f.write(str(edge.source) + ' -> ' + str(edge.target) + ';\n')
            f.write('}\n')
            f.close()
        if noSingle == True:
            TemporaryFile = tempfile.NamedTemporaryFile()
            call('gvpr -c "N[$.degree==0]{delete(root, $)}" -o '+ str(TemporaryFile.name) + " '"+str(fileName)+"'", shell= True)
            copyfile(TemporaryFile.name, str(fileName))

    def saveFig(self, filePath, noSingle = False):
        """Create a figure of the graph structure.

        Args:
          filePath (string): Path and filename.
          noSingle (bool):   If true remove any unconected single nodes and keep a single connected component
        """
        file_path = Path(filePath) #from string to path object
        self.saveDot(file_path.with_suffix('.dot'), noSingle = noSingle)
        f = open(file_path, 'w')
        call(["dot", file_path.with_suffix('.dot'), '-T'+file_path.suffix[1:]], stdout=f)
        f.close()

    def savePathStats(self, filePath, root = None):
        if root is None:
            root = self.graph.root
        with open(filePath, 'w') as f:
            f.write("\t".join(['pathLength', 'endType', 'numberOfPause', 'stepsToFirstPause', 'pathString\n']))
            self.pathStream = f
            self.depth_first(self.graph.nodes[root],[])

    def depth_first(self, node, path):
        path.append(node.id)
        if node.children:            #this is not a leaf
            for child in node.children:
                if child.id not in path:
                    self.depth_first(child, path)
                    path.pop()
                else:
                    print("Skipped descending into {} to avoid cycles".format(child.id), file=sys.stderr)
        else:
            self.calculatePathStatistics(path)
            self.paths[self.pathCounter] = path[:] #path.copy
            self.pathCounter += 1

    def calculatePathStatistics(self, path):
        badEndings = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="bad","node"]
        goodEndings = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="good","node"]
        pause = self.nodeAttributes.loc[self.nodeAttributes['attribute']=="pause","node"]
        pathLength = len(path)
        endNode = path[-1]
        endType = None
        if endNode in goodEndings.values:
            endType = "good"
        elif endNode in badEndings.values:
            endType = "bad"
        else:
            print("Error: Nodelist and edgelist do not match!", file=sys.stderr)
        numberOfPause = 0
        stepsToFirstPause = None
        pathString = str(path)
        for i, node in enumerate(path):
            if node in pause:
                if stepsToFirstPause is None:
                    stepsToFirstPause = i
                numberOfPause += 1
        self.pathStream.write("\t".join([str(entry) for entry in [pathLength, endType, numberOfPause, stepsToFirstPause, pathString]]) + '\n')

    def pathsToEdgelist(self):
        """Transform a set of paths to an edgelist and update the storystructure's
           edgelist.
        """
        max_rows = 100000
        self.edgelist = pd.DataFrame(index = np.arange(max_rows), columns = ["source","target"])
        rowCount = 0
        for path in self.paths.values():
            for source, target in zip(path[0:-1],path[1:]):
                self.edgelist.iloc[rowCount,] = [source, target]
                rowCount += 1
        assert rowCount <= max_rows,"More paths than max_rows."
        self.edgelist.dropna(inplace = True)
        self.edgelist = self.edgelist.drop_duplicates();
        #nodes are not updated!

    def clusterPaths(self, threshold, paths, pathsToDelete):
        """Cluster paths by similarity.
        Args:
            threshold     (float): Similarity ration for two paths to be merged.
            paths         (map):   Map of paths to be iteratively clustered.
            pathsToDelete (list):  List of path keys that should be deleted.
        """
        tempPaths = paths.copy()
        pathsToDelete = set()
        #for all path pairs calculate similarity index (common nodes/(sum of total))
        for i, j in combinations(tempPaths, 2):
            index = self.similarityIndex(tempPaths[i], tempPaths[j])
            if index <= threshold:
                newPath = self.mergePaths(tempPaths[i], tempPaths[j])
                tempPaths[i] = newPath
                pathsToDelete.add(j) #mark for deletion
        return(pathsToDelete)

    def iterativeClusterPaths(self, threshold):
        """Iteratively cluster paths untill equilibration.
        Args:
            threshold (float): Similarity ratio for two paths to be merged.
        """
        tempPaths = self.paths.copy()
        pathsToDelete = {None}
        while pathsToDelete:
            pathsToDelete = self.clusterPaths(threshold, tempPaths, [])
            for path in pathsToDelete:
                tempPaths.pop(path)
        self.paths = tempPaths.copy()

    def similarityIndex(self, setA, setB):
        """Calculate similarity index between two sets (or lists).
        """
        shared = set(setA).intersection(set(setB))
        union = set(setA).union(set(setB))
        return(1 - len(shared)/(len(union)))

    def mergePaths(self, pathA, pathB):
        """Merge two paths, chose one of the two randomly.
        """
        return(random.choice([pathA,pathB]))
