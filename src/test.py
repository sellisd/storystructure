#!/usr/bin/env python
from subprocess import call

from storystructure import storystructure
from string import digits, ascii_lowercase
from random import sample

chars = digits + ascii_lowercase
#Run some basic functionality tests
a = storystructure()
threshold = 0.5
paths = {
1:sample(chars, 10),
2:sample(chars, 10),
3:sample(chars, 10),
4:sample(chars, 10)
}
# test for similarity index

a.similarityIndex(paths[1], paths[2]) #0.333
a.similarityIndex(paths[3], paths[4]) #0.4

# merge paths
a.mergePaths(paths[1], paths[2])
# cluster paths
a.clusterPaths(0.35,paths,[])

# interative
a.paths = paths
a.iterativeClusterPaths(0.35)
# end of tests

# load dolmadakia
a.loadStory(edges = "../data/dolmadakia/edgelist.csv", nodes = "../data/dolmadakia/nodeAttributes.csv")

# make graph
a.saveDot("../data/dolmadakia/structure.dot")
f = open("../figs/dolmadakia.png", "w")
call(["dot", "../data/dolmadakia/structure.dot", "-Tpng"], stdout = f)

# make simplified graph
a.simplify()
a.saveDot("../data/dolmadakia/structureSimplified.dot")
f = open("../figs/dolmadakiaSimplified.png", "w")
call(["dot", "../data/dolmadakia/structureSimplified.dot", "-Tpng"], stdout = f)

# make DAG graph
a.makeGraph()
#-print([i.id for i in a.getStart()])
#-a.graph.setRoot(a.graph.nodes[7])
a.savePathStats(7, '../data/dolmadakia/allPaths.dat')
a.pathsToEdgelist()
a.saveDot("../data/dolmadakia/structurePaths.dot")
f = open("../figs/dolmadakiaPaths.png", "w")
call(["dot", "../data/dolmadakia/structurePaths.dot", "-Tpng"], stdout = f)

# cluster paths and make graph
a.iterativeClusterPaths(0.2)
a.pathsToEdgelist()
a.saveDot("../data/dolmadakia/structurePaths.dot")
f = open("../figs/dolmadakiaPathsClustered.png", "w")
call(["dot", "../data/dolmadakia/structurePaths.dot", "-Tpng"], stdout = f)

#
b = storystructure()
b.loadStory(edges = "../data/orientExpress/edgelist.csv")
b.simplify()
b.makeGraph()
#b.getStart()
#b.getStart()[0].id
#b.graph.setRoot(6)
b.savePathStats(7, '../data/orientExpress/allPaths.dat')
b.saveDot("../data/orientExpress/structure.dot")
f = open("../figs/orientExpress.png", "w")
call(["dot", "../data/orientExpress/structure.dot", "-Tpng"], stdout = f)
