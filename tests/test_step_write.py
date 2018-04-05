#!/usr/bin/env python
# coding: utf-8

r"""STEP file writing tests"""

import pytest
import os.path
import glob

import OCC.BRepPrimAPI
import OCC.gp
import OCC.TopoDS

import aocutils.topology

import aocxchange.exceptions
import aocxchange.step
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


def test_step_exporter_wrong_filename(box_shape):
    r"""Trying to write to a non-existent directory"""
    filename = aocxchange.utils.path_from_file(__file__, "./nonexistent/box.stp")
    with pytest.raises(aocxchange.exceptions.DirectoryNotFoundException):
        aocxchange.step.StepExporter(filename)


def test_step_exporter_wrong_extension(box_shape):
    r"""Trying to write a step file with the IgesExporter"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.igs")
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        aocxchange.step.StepExporter(filename)


def test_step_exporter_wrong_schema(box_shape):
    r"""Schema is not AP203 or AP214CD"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stp")
    with pytest.raises(aocxchange.exceptions.StepUnknownSchemaException):
        aocxchange.step.StepExporter(filename, schema="48.3")


def test_step_exporter_adding_not_a_shape(box_shape):
    r"""Adding something to the exporter that is not a TopoDS_Shape or a subclass"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stp")
    exporter = aocxchange.step.StepExporter(filename)
    with pytest.raises(ValueError):
        exporter.add_shape(OCC.gp.gp_Pnt(1, 1, 1))


def test_step_exporter_happy_path(box_shape):
    r"""Happy path"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.StP")
    exporter = aocxchange.step.StepExporter(filename)
    exporter.add_shape(box_shape)
    exporter.write_file()
    assert os.path.isfile(filename)
    # tests.utils.clean_output_dir()


def test_step_exporter_happy_path_shape_subclass(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stp")
    exporter = aocxchange.step.StepExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    assert isinstance(solid, OCC.TopoDS.TopoDS_Solid)
    exporter.add_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)


def test_step_exporter_overwrite(box_shape):
    r"""Happy path with a subclass of TopoDS_Shape"""
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stp")
    exporter = aocxchange.step.StepExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    assert isinstance(solid, OCC.TopoDS.TopoDS_Solid)
    exporter.add_shape(solid)
    exporter.write_file()
    initial_timestamp = os.path.getmtime(filename)
    assert os.path.isfile(filename)

    # read the written box.stp
    importer = aocxchange.step.StepImporter(filename)
    topo_compound = aocutils.topology.Topo(importer.compound, return_iter=False)
    assert topo_compound.number_of_faces == 6
    assert len(topo_compound.faces) == 6
    assert topo_compound.number_of_edges == 12

    # add a sphere and write again with same exporter
    sphere = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(10)
    exporter.add_shape(sphere.Shape())
    exporter.write_file()  # this creates a file with a box and a sphere
    intermediate_timestamp = os.path.getmtime(filename)
    assert intermediate_timestamp > initial_timestamp

    # check that the file contains the box and the sphere
    importer = aocxchange.step.StepImporter(filename)
    assert len(aocutils.topology.Topo(importer.compound, return_iter=False).faces) == 7  # 6 from box + 1 from sphere
    assert len(aocutils.topology.Topo(importer.compound, return_iter=False).solids) == 2

    # create a new exporter and overwrite with a box only
    filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.stp")
    exporter = aocxchange.step.StepExporter(filename)
    solid = aocutils.topology.shape_to_topology(box_shape)
    exporter.add_shape(solid)
    exporter.write_file()
    assert os.path.isfile(filename)
    last_timestamp = os.path.getmtime(filename)
    assert last_timestamp > intermediate_timestamp

    # check the file only contains a box
    importer = aocxchange.step.StepImporter(filename)
    assert len(aocutils.topology.Topo(importer.compound, return_iter=False).faces) == 6  # 6 from box
    assert len(aocutils.topology.Topo(importer.compound, return_iter=False).solids) == 1
