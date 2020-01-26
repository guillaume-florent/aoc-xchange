#!/usr/bin/env python
# coding: utf-8

r"""Exporting a shape to STL"""

from __future__ import print_function

import logging

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox

from aocxchange.stl import StlExporter
# from corelib.core.files import path_from_file
from corelibpy import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

# First create a simple shape to export
my_box_shape = BRepPrimAPI_MakeBox(50, 50, 50).Shape()

# Export to STL. If ASCIIMode is set to False, then binary format is used.
filename = path_from_file(__file__, "./models_out/result_export.stl")
my_stl_exporter = StlExporter(filename, ascii_mode=True)
my_stl_exporter.set_shape(my_box_shape)
my_stl_exporter.write_file()
