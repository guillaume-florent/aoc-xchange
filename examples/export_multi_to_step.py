#!/usr/bin/env python
# coding: utf-8

r"""Exporting multiple shapes to STEP"""

import logging

import OCC.BRepPrimAPI

import aocxchange.step
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')


# First create a simple shape to export
box_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()
sphere_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(20).Shape()

# Export to STEP
filename = aocxchange.utils.path_from_file(__file__, "./models_out/result_export_multi.stp")
step_exporter = aocxchange.step.StepExporter(filename)
step_exporter.add_shape(box_shape)
step_exporter.add_shape(sphere_shape)
step_exporter.write_file()
