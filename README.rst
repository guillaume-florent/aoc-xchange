.. -*- coding: utf-8 -*-

***********
aoc-xchange
***********

.. image:: https://travis-ci.org/guillaume-florent/aoc-xchange.svg?branch=master
    :target: https://travis-ci.org/guillaume-florent/aoc-xchange

.. image:: https://api.codacy.com/project/badge/Grade/10428d668bc94d10a96a39a200dfd843
    :target: https://www.codacy.com/app/guillaume-florent/aoc-xchange?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=guillaume-florent/aoc-xchange&amp;utm_campaign=Badge_Grade

.. image:: https://anaconda.org/gflorent/aocxchange/badges/version.svg
    :target: https://anaconda.org/gflorent/aocxchange

.. image:: https://anaconda.org/gflorent/aocxchange/badges/latest_release_date.svg
    :target: https://anaconda.org/gflorent/aocxchange

.. image:: https://anaconda.org/gflorent/aocxchange/badges/platforms.svg
    :target: https://anaconda.org/gflorent/aocxchange

.. image:: https://anaconda.org/gflorent/aocxchange/badges/downloads.svg
    :target: https://anaconda.org/gflorent/aocxchange

.. image:: http://img.shields.io/badge/Python-2.7_3.*-ff3366.svg
    :target: https://www.python.org/downloads/

The **aoc-xchange** project provides a Python package named **aocxchange** to read and write
from/to IGES, STEP, BREP, and STL files using `PythonOCC <http://www.pythonocc.org/>`_.

**aocxchange** can also read 2D foil section definition files (.dat files)

PythonOCC is a set of Python wrappers for the OpenCascade Community Edition (an industrial strength 3D CAD modeling kernel)

Warning
-------

**aocxchange** can import IGES, STEP, BREP, and STL files. Beware that the import of a similar looking geometry from different file
types might (and very likely will) lead to a different topology.

If working with solids, prefer STEP; you might get away with other formats but it will involve extra effort

If working with surfaces, any file type will do. However, remember that STEP and IGES geometry is mathematically defined
while STL basically stores a bunch of triangles approximating the geometry (which is absolutely fine and even
desirable in some cases).

install
-------

.. code-block:: bash

  conda install -c gflorent aocxchange

Dependencies
~~~~~~~~~~~~

*aocxchange* depends on OCC >=0.16 and aocutils. The examples require wx>=2.8 (or another backend (minor code modifications required)).
Please see how the Dockerfile satisfies these requirements.

Goal
----

The goal of the **aocxchange** package is to simplify the read/write of CAD files using PythonOCC.

Versions
--------

aocxchange version and target PythonOCC version

+--------------------+-------------------+
| aocxchange version | PythonOCC version |
+====================+===================+
| 18.*.*             | >=0.18.2          |
+--------------------+-------------------+

Examples
--------

The examples are in the *examples* folder at the Github repository (https://github.com/guillaume-florent/aoc-xchange).

The wx backend (wxPython) backend is used for the examples that display a UI.
You may easily change this behaviour to use pyqt4 or PySide by changing the backend in the call to init_display().

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-xchange/master/img/submarine.jpg
   :alt: submarine from STL

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-xchange/master/img/step_import_wing_structure_solids.jpg
   :alt: wing structure solids from STEP

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-xchange/master/img/vor70_cockpit.jpg
   :alt: VOR 70 cockpit from STEP

.. image:: https://raw.githubusercontent.com/guillaume-florent/aoc-xchange/master/img/step_import_aube_solids_and_edges.jpg
   :alt: Aube solids and edges from STEP
