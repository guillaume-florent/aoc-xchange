#!/usr/bin/python
# coding: utf-8

r"""STEP file reading tests"""

import logging

import pytest
import OCC.TopoDS
import OCC.BRepPrimAPI
import OCC.TopAbs

import aocutils.topology
import aocutils.pretty_print

import aocxchange.exceptions
import aocxchange.step
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')


def test_step_importer_wrong_path():
    r"""Wrong filename"""
    with pytest.raises(aocxchange.exceptions.FileNotFoundException):
        aocxchange.step.StepImporter("C:/stupid-filename.bad_extension")


def test_step_importer_wrong_extension():
    r"""wrong file format (i.e. trying to read a iges file with step importer)"""
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        filename = aocxchange.utils.path_from_file(__file__, "./models_in/aube_pleine.iges")
        aocxchange.step.StepImporter(filename)


def test_step_importer_wrong_file_content():
    r"""wrong file content"""
    with pytest.raises(aocxchange.exceptions.StepFileReadException):
        aocxchange.step.StepImporter(aocxchange.utils.path_from_file(__file__, "./models_in/empty.stp"))


def test_step_importer_happy_path():
    r"""happy path"""
    importer = aocxchange.step.StepImporter(aocxchange.utils.path_from_file(__file__, "./models_in/aube_pleine.stp"))
    assert isinstance(importer.compound, OCC.TopoDS.TopoDS_Compound)
    assert isinstance(importer.shapes, list)
    for shape in importer.shapes:
        assert isinstance(shape, OCC.TopoDS.TopoDS_Shape)
    assert len(importer.shapes) == 1


def test_step_importer_happy_topology():
    r"""import step file containing a box and test topology"""
    importer = aocxchange.step.StepImporter(aocxchange.utils.path_from_file(__file__, "./models_in/box_203.stp"))
    assert len(importer.shapes) == 1

    assert isinstance(importer.shapes[0], OCC.TopoDS.TopoDS_Shape)
    assert importer.shapes[0].ShapeType() == OCC.TopAbs.TopAbs_SOLID

    topo = aocutils.topology.Topo(importer.shapes[0])
    assert topo.number_of_compounds == 0
    assert topo.number_of_comp_solids == 0
    assert topo.number_of_solids == 1
    assert topo.number_of_shells == 1


def test_step_importer_2_boxes():
    r"""Import an step file containing 2 distinct boxes and test topology"""
    importer = aocxchange.step.StepImporter(aocxchange.utils.path_from_file(__file__, "./models_in/2_boxes_203.stp"))
    assert len(importer.shapes) == 1
    assert importer.shapes[0].ShapeType() == OCC.TopAbs.TopAbs_COMPOUND

    topo = aocutils.topology.Topo(importer.shapes[0])
    assert topo.number_of_compounds == 1
    assert topo.number_of_comp_solids == 0
    assert topo.number_of_solids == 2
    assert topo.number_of_shells == 2
