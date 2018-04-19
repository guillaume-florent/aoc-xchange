#!/usr/bin/env python
# coding: utf-8

r"""checks.py module tests"""

import pytest

from OCC.Core.TopoDS import TopoDS_Shape, TopoDS_Shell
from OCC.Core.gp import gp_Pnt
from OCC.Core.BRepBuilderAPI import BRepBuilderAPI_MakeEdge

from aocutils.topology import Topo

from aocxchange.checks import check_importer_filename, check_exporter_filename,\
    check_overwrite, check_shape
from aocxchange.exceptions import DirectoryNotFoundException, \
    IncompatibleFileFormatException
from corelib.core.files import path_from_file

# Python 2 and 3 compatibility
try:
    FileNotFoundError
except NameError:
    FileNotFoundError = IOError


def test_check_importer_filename_inexistent_file():
    r"""Inexistent file test for check_importer_filename()"""
    with pytest.raises(FileNotFoundError):
        check_importer_filename(path_from_file(__file__,
                                               "./models_out/dummy.igs"))


def test_check_importer_filename_wrong_extension():
    r"""Wrong extension test for check_importer_filename()"""
    with pytest.raises(IncompatibleFileFormatException):
        check_importer_filename(path_from_file(__file__,
                                               "./models_in/box.igs"),
                                ["step"])


def test_check_importer_filename_happy_path():
    r"""Happy path for check_importer_filename()"""
    check_importer_filename(path_from_file(__file__, "./models_in/box.igs"))


def test_check_exporter_filename_inexistent_directory():
    r"""Inexistent directory test for check_exporter_filename()"""
    with pytest.raises(DirectoryNotFoundException):
        check_exporter_filename(path_from_file(__file__,
                                               "./inexistent-dir/dummy.igs"))


def test_check_exporter_filename_wrong_extension():
    r"""Wrong extension test for check_exporter_filename()"""
    with pytest.raises(IncompatibleFileFormatException):
        check_exporter_filename(path_from_file(__file__,
                                               "./models_out/box.igs"),
                                ["step"])


def test_check_exporter_filename_happy_path():
    r"""Happy path for check_exporter_filename()"""
    check_exporter_filename(path_from_file(__file__, "./models_out/box.igs"))


def test_check_overwrite():
    r"""check_overwrite() tests"""
    # file exists
    assert check_overwrite(path_from_file(__file__, "./models_in/box.igs")) is True

    # file does not exist
    assert check_overwrite(path_from_file(__file__, "./models_in/bo_.igs")) is False


def test_check_shape():
    r"""check_shape() tests"""
    # Null shapes should raise a ValueError
    with pytest.raises(ValueError):
        check_shape(TopoDS_Shape())
    with pytest.raises(ValueError):
        check_shape(TopoDS_Shell())

    builderapi_makeedge = BRepBuilderAPI_MakeEdge(gp_Pnt(), gp_Pnt(10, 10, 10))
    shape = builderapi_makeedge.Shape()

    # a ValueError should be raised is check_shape() is not give
    # a TopoDS_Shape or subclass
    with pytest.raises(ValueError):
        check_shape(gp_Pnt())
    with pytest.raises(ValueError):
        check_shape(builderapi_makeedge)

    # a TopoDS_Shape should pass the check without raising any exception
    check_shape(shape)

    # a subclass of shape should not raise any exception
    check_shape(Topo(shape, return_iter=False).edges[0])
