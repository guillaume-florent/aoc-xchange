#!/usr/bin/env python
# coding: utf-8

r"""STL file writing tests"""

import pytest
import os.path
import glob

import OCC.BRepPrimAPI
import OCC.gp
import OCC.TopoDS

import aocutils.topology

import aocxchange.exceptions
import aocxchange.stl
import aocxchange.utils


@pytest.yield_fixture(autouse=True)
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
    return OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(10, 20, 30).Shape()


def test_stl_exporter_wrong_filename(box_shape):
    r"""Trying to write to a non-existent directory"""
    filename = aocxchange.utils.path_from_file(__file__, "./nonexistent/box.stl")
    with pytest.raises(aocxchange.exceptions.DirectoryNotFoundException):
        aocxchange.stl.StlExporter(filename)


def test_stl_exporter_wrong_extension(box_shape):
    r"""Trying to write a step file with the IgesExporter"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.step")
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        aocxchange.stl.StlExporter(filename)


def test_stl_exporter_adding_not_a_shape(box_shape):
    r"""Adding something to the exporter that is not a
    TopoDS_Shape or a subclass"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stl")
    exporter = aocxchange.stl.StlExporter(filename)
    with pytest.raises(ValueError):
        exporter.set_shape(OCC.gp.gp_Pnt(1, 1, 1))


def test_stl_exporter_happy_path(box_shape):
    r"""Happy path"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.sTl")
    exporter = aocxchange.stl.StlExporter(filename)
    exporter.set_shape(box_shape)
    exporter.write_file()
    assert os.path.isfile(filename)
    # tests.utils.clean_output_dir()


def test_stl_exporter_happy_path_shape_subclass(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stl")
    exporter = aocxchange.stl.StlExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    assert isinstance(solid, OCC.TopoDS.TopoDS_Solid)
    exporter.set_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)


def test_stl_exporter_overwrite(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stl")
    exporter = aocxchange.stl.StlExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    assert isinstance(solid, OCC.TopoDS.TopoDS_Solid)
    exporter.set_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)

    # read the written box.stl
    importer = aocxchange.stl.StlImporter(filename)
    topo = aocutils.topology.Topo(importer.shape)
    assert topo.number_of_shells == 1

    # set a sphere and write again with same exporter
    sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(10)
    exporter.set_shape(sphere.Shape())
    exporter.write_file()  # this creates a file with a sphere only, this is STL specific

    # check that the file contains the sphere only
    importer = aocxchange.stl.StlImporter(filename)
    topo = aocutils.topology.Topo(importer.shape)
    assert topo.number_of_shells == 1

    # create a new exporter and overwrite with a box only
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stl")
    exporter = aocxchange.stl.StlExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    exporter.set_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)

    # check the file only contains a box
    importer = aocxchange.stl.StlImporter(filename)
    topo = aocutils.topology.Topo(importer.shape)
    assert topo.number_of_shells == 1
