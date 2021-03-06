===========
Tensorprobe
===========


.. image:: https://img.shields.io/pypi/v/tensorprobe.svg
        :target: https://pypi.python.org/pypi/tensorprobe

.. image:: https://img.shields.io/travis/abhishekkumarsingh/tensorprobe.svg
        :target: https://travis-ci.org/abhishekkumarsingh/tensorprobe

.. image:: https://readthedocs.org/projects/tensorprobe/badge/?version=latest
        :target: https://tensorprobe.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/abhishekkumarsingh/tensorprobe/shield.svg
     :target: https://pyup.io/repos/github/abhishekkumarsingh/tensorprobe/
     :alt: Updates



[Getting Started]() |
[Documentation]() |
[Community]() |
[Contributing]()



Tensorprobe assits in interactively probing your dataset.


* Free software: MIT license
* Documentation: https://tensorprobe.readthedocs.io.


Installation
------------

Tensorprobe supports python 3.5+.

**Direct Installation using pip:**

Execute Python functions in parallel.

.. code-block:: sh

    pip install tensorprobe


**Install from source:**

.. code-block:: sh
    
    git clone https://github.com/tensorsolve-ai/tensorprobe.git
    cd tensorprobe
    git checkout master  # master is pinned to the latest release
    pip install .


Quick Start
-----------

.. code-block:: python

    import tensorprobe as tp
    import seaborn as sns


    # load an example dataframe
    titanic = sns.load_dataset("titanic")

    # investigate dataframe
    tp.probe(titanic)


.. image:: /images/dashboard.png
    :alt: dashboard image

Features
--------

* TODO
