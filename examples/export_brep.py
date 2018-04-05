#!/usr/bin/env python
# coding: utf-8

r"""Exporting a single shape to BREP"""

import logging

import OCC.BRepPrimAPI

import aocxchange.brep
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# First create a simple shape to export
box_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()

# Export to BREP
filename = aocxchange.utils.path_from_file(__file__, "./models_out/box.brep")
step_exporter = aocxchange.brep.BrepExporter(filename)
step_exporter.set_shape(box_shape)
step_exporter.write_file()
