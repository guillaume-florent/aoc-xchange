#!/usr/bin/python
# coding: utf-8

r"""checks.py module tests"""

import pytest

import OCC.TopoDS
import OCC.gp
import OCC.BRepBuilderAPI

import aocutils.topology

import aocxchange.checks
import aocxchange.exceptions
import aocxchange.utils


def test_check_importer_filename_inexistent_file():
    r"""Inexistent file test for check_importer_filename()"""
    with pytest.raises(aocxchange.exceptions.FileNotFoundException):
        aocxchange.checks.check_importer_filename(aocxchange.utils.path_from_file(__file__, "./models_out/dummy.igs"))


def test_check_importer_filename_wrong_extension():
    r"""Wrong extension test for check_importer_filename()"""
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        aocxchange.checks.check_importer_filename(aocxchange.utils.path_from_file(__file__, "./models_in/box.igs"),
                                                  ["step"])


def test_check_importer_filename_happy_path():
    r"""Happy path for check_importer_filename()"""
    aocxchange.checks.check_importer_filename(aocxchange.utils.path_from_file(__file__, "./models_in/box.igs"))


def test_check_exporter_filename_inexistent_directory():
    r"""Inexistent directory test for check_exporter_filename()"""
    with pytest.raises(aocxchange.exceptions.DirectoryNotFoundException):
        aocxchange.checks.check_exporter_filename(aocxchange.utils.path_from_file(__file__,
                                                                                  "./inexistent-dir/dummy.igs"))


def test_check_exporter_filename_wrong_extension():
    r"""Wrong extension test for check_exporter_filename()"""
    with pytest.raises(aocxchange.exceptions.IncompatibleFileFormatException):
        aocxchange.checks.check_exporter_filename(aocxchange.utils.path_from_file(__file__, "./models_out/box.igs"),
                                                  ["step"])


def test_check_exporter_filename_happy_path():
    r"""Happy path for check_exporter_filename()"""
    aocxchange.checks.check_exporter_filename(aocxchange.utils.path_from_file(__file__, "./models_out/box.igs"))


def test_check_overwrite():
    r"""check_overwrite() tests"""
    # file exists
    assert aocxchange.checks.check_overwrite(aocxchange.utils.path_from_file(__file__, "./models_in/box.igs")) is True

    # file does not exist
    assert aocxchange.checks.check_overwrite(aocxchange.utils.path_from_file(__file__, "./models_in/bo_.igs")) is False


def test_check_shape():
    r"""check_shape() tests"""
    # Null shapes should raise a ValueError
    with pytest.raises(ValueError):
        aocxchange.checks.check_shape(OCC.TopoDS.TopoDS_Shape())
    with pytest.raises(ValueError):
        aocxchange.checks.check_shape(OCC.TopoDS.TopoDS_Shell())

    builderapi_makeedge = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeEdge(OCC.gp.gp_Pnt(), OCC.gp.gp_Pnt(10, 10, 10))
    shape = builderapi_makeedge.Shape()

    # a ValueError should be raised is check_shape() is not give a TopoDS_Shape or subclass
    with pytest.raises(ValueError):
        aocxchange.checks.check_shape(OCC.gp.gp_Pnt())
    with pytest.raises(ValueError):
        aocxchange.checks.check_shape(builderapi_makeedge)

    # a TopoDS_Shape should pass the check without raising any exception
    aocxchange.checks.check_shape(shape)

    # a subclass of shape should not raise any exception
    aocxchange.checks.check_shape(aocutils.topology.Topo(shape, return_iter=False).edges[0])
