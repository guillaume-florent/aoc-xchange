#!/usr/bin/env python
# coding: utf-8

r"""Exporting multiple shapes to STEP"""

import logging

from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox, BRepPrimAPI_MakeSphere

from aocxchange.step import StepExporter
from aocxchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')


# First create a simple shape to export
box_shape = BRepPrimAPI_MakeBox(50, 50, 50).Shape()
sphere_shape = BRepPrimAPI_MakeSphere(20).Shape()

# Export to STEP
filename = path_from_file(__file__, "./models_out/result_export_multi.stp")
step_exporter = StepExporter(filename)
step_exporter.add_shape(box_shape)
step_exporter.add_shape(sphere_shape)
step_exporter.write_file()
