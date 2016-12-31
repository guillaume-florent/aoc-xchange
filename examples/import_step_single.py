#!/usr/bin/python
# coding: utf-8

r"""Importing single shape from STEP"""

from __future__ import print_function

import logging

import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.backends

import aocxchange.step
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/aube_pleine.stp")
step_importer = aocxchange.step.StepImporter(filename)

# step_importer.read_file() -> automatic read_file !!

print("Nb shapes: %i" % len(step_importer.shapes))
for shape in step_importer.shapes:
    print(shape.ShapeType())  # 2 -> solid
# print("number_of_shapes: %i" % step_importer.number_of_shapes)  # 0 ??
# display.DisplayShape(step_importer.shapes)
aocutils.display.topology.solids(display, step_importer.shapes[0], transparency=0.8)
aocutils.display.topology.edges(display, step_importer.shapes[0])
display.FitAll()
display.View_Iso()
start_display()
