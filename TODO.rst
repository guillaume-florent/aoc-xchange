conversions
-----------

step_to_obj:
    tests !!
    linux script
    windows script
    install instructions
    dockerization

    Dockerization
    -------------
    Minimal Linux
    Miniconda
    conda install pythonocc
    aocutils (git clone)
    aocxchange (git clone)
    install pymesh (pip install pymesh) -> NO, included in aocxchange
    make a script available system-wide
    how to call from outside?


dialogs
-------

save:
warning message when only one shape can be saved and the list is longer (stl and brep)

open:
optional panel recapitulating what has been loaded and info about topology
how to extract schema/format info from files that are opened

move the example of cad file dialogs to the examples + plug a viewer in the testing frame


tests
-----
include tests with different geometries (open shell, curves etc ...)
step_ocaf
Python 3 tests
doctests?
brep importer and exporter tests
auto folder creation option in checks.py/check_exporter_filename()

Run tests on Linux and MacOS

general
-------
solid reconstruction from iges faces, stl shell
it is a library, easy on logging (debug for almost everything, info if very important)

iges
----
extract iges version when importing
roots and shapes -> have a look at iges file format spec
build the shell and solid from connected faces (pretty complicated / network theory / find groups of interconnected faces)

step_ocaf
---------
complete review + tests
looks weird to only consider compounds and solids while reading file. What about edges etc ...

issues
------
importing iges box -> 24 edges
importing step box -> 12 edges

Later
-----

opennurbs
  -> python bindings (cf. https://github.com/raj12lnm/OpenNurbs-Python) with pybindgen (or swig?)
        cython can be used to wrao existing codebases (and libraries for automation exist)
        https://github.com/cython/cython/wiki/AutoPxd
  -> work from/to 3dm files
  -> cage editing available in opennurbs?