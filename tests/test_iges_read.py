#!/usr/bin/python
# coding: utf-8

r"""IGES file reading tests"""

import logging

import pytest
import OCC.TopoDS
import OCC.BRepPrimAPI

import aocutils.topology
import aocutils.pretty_print

import aocxchange.exceptions
import aocxchange.iges
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')


def test_iges_importer_wrong_path():
    r"""Wrong filename"""
    with pytest.raises(aocxchange.exceptions.FileNotFoundException):
        aocxchange.iges.IgesImporter("C:/stupid-filename.bad_extension")


def test_iges_importer_wrong_extension():
    r"""wrong file format (i.e. trying to read a step file with iges importer)"""
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        aocxchange.iges.IgesImporter(aocxchange.utils.path_from_file(__file__, "./models_in/aube_pleine.stp"))


def test_iges_importer_wrong_file_content():
    r"""wrong file content"""
    with pytest.raises(aocxchange.exceptions.IgesFileReadException):
        aocxchange.iges.IgesImporter(aocxchange.utils.path_from_file(__file__, "./models_in/empty.igs"))


def test_iges_importer_happy_path():
    r"""happy path"""
    importer = aocxchange.iges.IgesImporter(aocxchange.utils.path_from_file(__file__, "./models_in/aube_pleine.iges"))
    assert isinstance(importer.compound, OCC.TopoDS.TopoDS_Compound)
    assert isinstance(importer.shapes, list)
    for shape in importer.shapes:
        assert isinstance(shape, OCC.TopoDS.TopoDS_Shape)


def test_iges_importer_happy_topology():
    r"""import iges file containing a box and test topology"""
    importer = aocxchange.iges.IgesImporter(aocxchange.utils.path_from_file(__file__, "./models_in/box.igs"))

    topo = aocutils.topology.Topo(importer.compound, return_iter=False)
    assert topo.number_of_faces == 6
    assert topo.number_of_edges == 24  # 12 edges * 2 possible orientations ?


def test_iges_importer_2_boxes():
    r"""Import an iges file containing 2 distinct boxes and test topology

    Notes
    -----
    This shows the current limitations of the IgesImporter as 2 boxes cannot be distinguished from one another

    """
    importer = aocxchange.iges.IgesImporter(aocxchange.utils.path_from_file(__file__, "./models_in/2_boxes.igs"))
    topo = aocutils.topology.Topo(importer.compound, return_iter=False)
    assert topo.number_of_faces == 6 * 2
    assert topo.number_of_edges == 24 * 2
