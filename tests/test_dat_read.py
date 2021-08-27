#!/usr/bin/env python
# coding: utf-8

r"""DAT file reading tests"""

from corelib.core.files import path_from_file
from aocxchange.dat import DatImporter, import_dat_file


def test_read_dat_file():
    r"""Test reading a foil section definition dat file"""
    importer = DatImporter(path_from_file(__file__, "./models_in/naca0006.dat"),
                           skip_first_line=True)
    pts = importer.points
    assert len(pts) == 35

    assert pts[0] == (1.0000, 0.00063)
    assert pts[-1] == (1.0000, -0.00063)


def test_import_dat_file():
    r"""Test importing a foil section definition dat file using
    the import_dat_file() function"""
    pts = import_dat_file(path_from_file(__file__, "./models_in/naca0006.dat"),
                          skip_first_line=True)
    assert len(pts) == 35

    assert pts[0] == (1.0000, 0.00063)
    assert pts[-1] == (1.0000, -0.00063)
