.. -*- coding: utf-8 -*-

aoc-xchange
===========

.. image:: https://api.codacy.com/project/badge/Grade/10428d668bc94d10a96a39a200dfd843
   :target: https://www.codacy.com/app/guillaume-florent/aoc-xchange?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=guillaume-florent/aoc-xchange&amp;utm_campaign=Badge_Grade
.. image:: http://img.shields.io/badge/Status-development-ff3300.svg
   :alt: Development
.. image:: http://img.shields.io/badge/license-GPL_v3-blue.svg
   :target: https://www.gnu.org/copyleft/gpl.html
   :alt: GPL v3
.. image:: http://img.shields.io/badge/Python-2.7_3.*-ff3366.svg
   :target: https://www.python.org/downloads/
   :alt: Python 2.7 3.*

The **aoc-xchange** project provides a Python package named **aocxchange** to read and write
from/to IGES, STEP, BREP, and STL files using `PythonOCC <http://www.pythonocc.org/>`_.

**aocxchange** can also read 2D foil section definition files (.dat files)

PythonOCC is a set of Python wrappers for the OpenCascade Community Edition (an industrial strength 3D CAD modeling kernel)

Warning
-------

**aocxchange** can import IGES, STEP, BREP, and STL files. Beware that the import of a similar looking geometry from different file
types might (and very likely will) lead to a different topology.

For example, the import of 2 distinct solids (closed boxes) will lead to:

- undistinguishable faces from an IGES file

- 2 separate solids from a STEP file

- 2 separate closed shells from a STL file

If working with solids, prefer STEP; you might get away with STL but it will involve extra effort

If working with surfaces, any file type will do. However, remember that STEP and IGES geometry is mathematically defined
while STL basically stores a bunch of triangles approximating the geometry (which is absolutely fine and even
desirable in some cases).

install
-------

.. code-block:: bash

  pip install aocxchange

Dependencies
~~~~~~~~~~~~

*aocxchange* depends on OCC >=0.16 and aocutils. The examples require wx>=2.8 (or another backend (minor code modifications required)).
Please see the table below for instructions on how to satisfy the requirements.

+----------+----------+----------------------------------------------------------------------------+
| package  | version  | Comment                                                                    |
+==========+==========+============================================================================+
| OCC      | >=0.16.  | | See pythonocc.org or github.com.tpaviot/pythonocc-core for instructions  |
|          |          | | or `conda install -c https://conda.anaconda.org/dlr-sc pythonocc-core`   |
+----------+----------+----------------------------------------------------------------------------+
| aocutils | latest   | `pip install aocutils --upgrade`                                           |
+----------+----------+----------------------------------------------------------------------------+
| wx       | >=2.8    | See wxpython.org for instructions                                          |
+----------+----------+----------------------------------------------------------------------------+

Goal
----

The goal of the **aocxchange** package is to simplify the read/write of CAD files using PythonOCC.

Versions
--------

occdataexchange version and target PythonOCC version

+--------------------+-------------------+
| aocxchange version | PythonOCC version |
+====================+===================+
| 0.1.*              | 0.16.2            |
+--------------------+-------------------+

Examples
--------

The examples are in the *examples* folder at the Github repository (https://github.com/floatingpointstack/aoc-xchange).

The wx backend (wxPython) backend is used for the examples that display a UI.
You may easily change this behaviour to use pyqt4 or PySide by changing the backend in the call to init_display().

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-xchange/master/img/submarine.jpg
   :alt: submarine from STL

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-xchange/master/img/step_import_wing_structure_solids.jpg
   :alt: wing structure solids from STEP

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-xchange/master/img/vor70_cockpit.jpg
   :alt: VOR 70 cockpit from STEP

.. image:: https://raw.githubusercontent.com/floatingpointstack/aoc-xchange/master/img/step_import_aube_solids_and_edges.jpg
   :alt: Aube solids and edges from STEP
