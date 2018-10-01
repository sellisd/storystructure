#!/usr/bin/env python
from subprocess import call

from storystructure import storystructure
a = storystructure()
a.loadStory(edges = "../data/dolmadakia/edgelist.csv", nodes = "../data/dolmadakia/nodeAttributes.csv")
a.graph.setRoot(a.graph.nodes[7])
print(a.getRoots())
a.saveDot("../data/dolmadakia/structure.dot")
# dot ../data/88_ntolmadakia.dot -Tpng > ../figs/88_ntolmadakia.png
f = open("../figs/dolmadakia.png", "w")
call(["dot", "../data/dolmadakia/structure.dot", "-Tpng"], stdout = f)
