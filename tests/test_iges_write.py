#!/usr/bin/env python
# coding: utf-8

r"""IGES file writing tests"""

import pytest
import os.path
import glob

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere
from OCC.Core.gp import gp_Pnt
from OCC.Core.TopoDS import TopoDS_Solid

from aocutils.topology import Topo, shape_to_topology

from aocxchange.exceptions import DirectoryNotFoundException, \
    IncompatibleFileFormatException, IgesUnknownFormatException
from aocxchange.iges import IgesImporter, IgesExporter
from corelib.core.files import path_from_file


@pytest.fixture(autouse=True)
def cleandir():
    r"""Clean the tests output directory

    autouse=True insure this fixture wraps every test function
    yield represents the function call
    """
    yield  # represents the test function call
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                              "models_out")
    files = glob.glob(output_dir + r"\*")
    print("Cleaning output directory ...")
    for f in files:
        os.remove(f)
    print("Output directory clean")


@pytest.fixture()
def box_shape():
    r"""Box shape for testing"""
    return BRepPrimAPI_MakeBox(10, 20, 30).Shape()


def test_iges_exporter_wrong_filename(box_shape):
    r"""Trying to write to a non-existent directory"""
    filename = path_from_file(__file__, "./nonexistent/box.igs")
    with pytest.raises(DirectoryNotFoundException):
        IgesExporter(filename)


def test_iges_exporter_wrong_extension(box_shape):
    r"""Trying to write a step file with the IgesExporter"""
    filename = path_from_file(__file__, "./models_out/box.step")
    with pytest.raises(IncompatibleFileFormatException):
        IgesExporter(filename)


def test_iges_exporter_wrong_format(box_shape):
    r"""Format is not 5.1 or 5.3"""
    filename = path_from_file(__file__, "./models_out/box.igs")
    with pytest.raises(IgesUnknownFormatException):
        IgesExporter(filename, format_="48.3")


def test_iges_exporter_adding_not_a_shape(box_shape):
    r"""Adding something to the exporter that is not a TopoDS_Shape 
    or a subclass"""
    filename = path_from_file(__file__, "./models_out/box.igs")
    exporter = IgesExporter(filename)
    with pytest.raises(ValueError):
        exporter.add_shape(gp_Pnt(1, 1, 1))


def test_iges_exporter_happy_path(box_shape):
    r"""Happy path"""
    filename = path_from_file(__file__, "./models_out/box.IgS")
    exporter = IgesExporter(filename)
    exporter.add_shape(box_shape)
    exporter.write_file()
    assert os.path.isfile(filename)
    # tests.utils.clean_output_dir()


def test_iges_exporter_happy_path_shape_subclass(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = path_from_file(__file__, "./models_out/box.igs")
    exporter = IgesExporter(filename)
    solid = shape_to_topology(box_shape)
    assert isinstance(solid, TopoDS_Solid)
    exporter.add_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)


def test_iges_exporter_overwrite(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = path_from_file(__file__, "./models_out/box.igs")
    exporter = IgesExporter(filename)
    solid = shape_to_topology(box_shape)
    assert isinstance(solid, TopoDS_Solid)
    exporter.add_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)

    # read the written box.igs
    importer = IgesImporter(filename)
    topo_compound = Topo(importer.compound)
    assert topo_compound.number_of_faces == 6
    assert topo_compound.number_of_edges == 24

    # add a sphere and write again with same exporter
    sphere = BRepPrimAPI_MakeSphere(10)
    exporter.add_shape(sphere.Shape())
    exporter.write_file()  # this creates a file with a box and a sphere

    # check that the file contains the box and the sphere
    importer = IgesImporter(filename)
    topo_compound = Topo(importer.compound)
    assert topo_compound.number_of_faces == 7  # 6 from box + 1 from sphere

    # create a new exporter and overwrite with a box only
    filename = path_from_file(__file__, "./models_out/box.igs")
    exporter = IgesExporter(filename)
    solid = shape_to_topology(box_shape)
    exporter.add_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)

    # check the file only contains a box
    importer = IgesImporter(filename)
    topo_compound = Topo(importer.compound)
    assert topo_compound.number_of_faces == 6  # 6 from box
