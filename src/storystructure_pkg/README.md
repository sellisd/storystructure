# storystructure package

A Python package to explore the stucture of branching stories

## Requirements

The module has been developed with python 3.6.6 and the following modules. Other
versions might work also but have not been tested

- pandas 0.24.1
-
## Installation

```
pip install storystructure
```

## Example usage

To use the package two input data files are necessary:

- An *edgelist* file with columns `source` and `target`
- A *node attributes* file with columns `node` and `attribute`. The attribute column must be on of the following values `good`, `bad`, `pause`

```Python
from storystructure.storystructure import storystructure
s = storystructure.storystructure()
```
