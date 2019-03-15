A Python package to explore the structure of branching stories.

Requirements
------------

The module has been developed with python 3.6.6 and the following modules. Other
versions might work also but have not been tested:

* ``pathlib2 v.2.2.0``
* ``pandas v.0.19.2``
* ``numpy v.1.11.3``

Installation
------------

.. code-block::  bash

    pip install storystructure

Example usage
-------------

To use the package two input data files are necessary:

* An *edgelist* file with columns ``source`` and ``target``
* A *node attributes* file with columns ``node`` and ``attribute``. The attribute column must be on of the following values ``good``, ``bad``, ``pause``.

.. code-block:: python

    from storystructure.storystructure import storystructure
    s = storystructure.storystructure()