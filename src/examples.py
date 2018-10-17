#!/usr/bin/env python

# exploratory scenarios
# 1. Visualize story structure with annotations
# 2. Find problems or interesting features in structure
# 3. Enumerate all possible stories
# 4. Find the number of sub-stories


# create a new object
s = storystructure()
# load an edgelist and node attributes
s.loadStory(edges = "../data/dolmadakia/edgelist.csv", nodes = "../data/dolmadakia/nodeAttributes.csv")
# save in dot format
s.saveDot("../data/dolmadakia/structure.dot")
# save as png
f = open("../figs/dolmadakia.png", "w")
call(["dot", "../data/dolmadakia/structure.dot", "-Tpng"], stdout = f)

# get a table of duplicated edges if they exist
print(s.getDuplicates())

# get a table of self loops if they exist
print(s.getSelfloops())

# get the starting page or all roots if multiple
print(s.getStart())

# find all possible paths and calculate some descriptive statistics
s.makeGraph()
s.savePathStats(7, '../data/dolmadakia/allPaths.dat')

# cluster paths that are more than 20% similar to each other
s.iterativeClusterPaths(0.2)
s.pathsToEdgelist()
s.saveDot("../data/dolmadakia/structurePaths.dot")
f = open("../figs/dolmadakiaPathsClustered.png", "w")
call(["dot", "../data/dolmadakia/structurePaths.dot", "-Tpng"], stdout = f)
