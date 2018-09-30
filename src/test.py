#!/usr/bin/env python
from subprocess import call

from storystructure import storystructure
a = storystructure()
a.loadEdgelist(filePath = "../data/dolmadakia/edgelist.csv")
a.loadNodeAttributes(filePath = "../data/dolmadakia/nodeAttributes.csv")
a.saveDot("../data/dolmadakia/structure.dot")
# dot ../data/88_ntolmadakia.dot -Tpng > ../figs/88_ntolmadakia.png
f = open("../figs/dolmadakia.png", "w")
call(["dot", "../data/dolmadakia/structure.dot", "-Tpng"], stdout = f)
