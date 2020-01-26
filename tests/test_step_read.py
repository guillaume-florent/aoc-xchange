#!/usr/bin/env python
# coding: utf-8

r"""STEP file reading tests"""

import pytest

from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Compound
from OCC.Core.TopAbs import TopAbs_SOLID, TopAbs_COMPOUND

from aocutils.topology import Topo

from aocxchange.exceptions import IncompatibleFileFormatException,\
    StepFileReadException
from aocxchange.step import StepImporter
# from corelib.core.files import path_from_file
from corelibpy import path_from_file

# Python 2 and 3 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def test_step_importer_wrong_path():
    r"""Wrong filename"""
    with pytest.raises(FileNotFoundError):
        StepImporter("C:/stupid-filename.bad_extension")


def test_step_importer_wrong_extension():
    r"""wrong file format (i.e. trying to read a iges file
    with step importer)"""
    with pytest.raises(IncompatibleFileFormatException):
        filename = path_from_file(__file__, "./models_in/aube_pleine.iges")
        StepImporter(filename)


def test_step_importer_wrong_file_content():
    r"""wrong file content"""
    with pytest.raises(StepFileReadException):
        StepImporter(path_from_file(__file__, "./models_in/empty.stp"))


def test_step_importer_happy_path():
    r"""happy path"""
    importer = StepImporter(path_from_file(__file__,
                                           "./models_in/aube_pleine.stp"))
    assert isinstance(importer.compound, TopoDS_Compound)
    assert isinstance(importer.shapes, list)
    for shape in importer.shapes:
        assert isinstance(shape, TopoDS_Shape)
    assert len(importer.shapes) == 1


def test_step_importer_happy_topology():
    r"""import step file containing a box and test topology"""
    importer = StepImporter(path_from_file(__file__, "./models_in/box_203.stp"))
    assert len(importer.shapes) == 1

    assert isinstance(importer.shapes[0], TopoDS_Shape)
    assert importer.shapes[0].ShapeType() == TopAbs_SOLID

    topo = Topo(importer.shapes[0])
    assert topo.number_of_compounds == 0
    assert topo.number_of_comp_solids == 0
    assert topo.number_of_solids == 1
    assert topo.number_of_shells == 1


def test_step_importer_2_boxes():
    r"""Import an step file containing 2 distinct boxes and test topology"""
    importer = StepImporter(path_from_file(__file__,
                                           "./models_in/2_boxes_203.stp"))
    assert len(importer.shapes) == 1
    assert importer.shapes[0].ShapeType() == TopAbs_COMPOUND

    topo = Topo(importer.shapes[0])
    assert topo.number_of_compounds == 1
    assert topo.number_of_comp_solids == 0
    assert topo.number_of_solids == 2
    assert topo.number_of_shells == 2
