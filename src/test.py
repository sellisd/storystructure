#!/usr/bin/env python
from subprocess import call

from storystructure import storystructure
a = storystructure()
a.loadStory(edges = "../data/dolmadakia/edgelist.csv", nodes = "../data/dolmadakia/nodeAttributes.csv")
a.saveDot("../data/dolmadakia/structure.dot")
f = open("../figs/dolmadakia.png", "w")
call(["dot", "../data/dolmadakia/structure.dot", "-Tpng"], stdout = f)

a.simplify()
#a.makeGraph()
a.saveDot("../data/dolmadakia/structureSimplified.dot")
f = open("../figs/dolmadakiaSimplified.png", "w")
call(["dot", "../data/dolmadakia/structureSimplified.dot", "-Tpng"], stdout = f)

a.makeGraph()
print([i.id for i in a.getStart()])
a.graph.setRoot(a.graph.nodes[7])

a.savePathStats(7, '../data/dolmadakia/allPaths.dat')

a.pathsToEdgelist()
a.saveDot("../data/dolmadakia/structurePaths.dot")
f = open("../figs/dolmadakiaPaths.png", "w")
call(["dot", "../data/dolmadakia/structurePaths.dot", "-Tpng"], stdout = f)
