#!/usr/bin/env python
# coding: utf-8

r"""Importing single shape from STEP"""

from __future__ import print_function

import logging

from OCC.Display.SimpleGui import init_display

from aocutils.display.topology import solids, edges
from aocutils.display.defaults import backend

from aocxchange.step import StepImporter
from aocxchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)

filename = path_from_file(__file__, "./models_in/step/aube_pleine.stp")
step_importer = StepImporter(filename)

# step_importer.read_file() -> automatic read_file !!

print("Nb shapes: %i" % len(step_importer.shapes))
for shape in step_importer.shapes:
    print(shape.ShapeType())  # 2 -> solid
# print("number_of_shapes: %i" % step_importer.number_of_shapes)  # 0 ??
# display.DisplayShape(step_importer.shapes)
solids(display, step_importer.shapes[0], transparency=0.8)
edges(display, step_importer.shapes[0])
display.FitAll()
display.View_Iso()
start_display()
