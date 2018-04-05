#!/usr/bin/env python
# coding: utf-8

r"""Exporting a shape to STL"""

from __future__ import print_function

import logging

import OCC.BRepPrimAPI

import aocxchange.stl
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# First create a simple shape to export
my_box_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()

# Export to STL. If ASCIIMode is set to False, then binary format is used.
filename = aocxchange.utils.path_from_file(__file__, "./models_out/result_export.stl")
my_stl_exporter = aocxchange.stl.StlExporter(filename, ascii_mode=True)
my_stl_exporter.set_shape(my_box_shape)
my_stl_exporter.write_file()
