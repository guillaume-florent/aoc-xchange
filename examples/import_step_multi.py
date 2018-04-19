#!/usr/bin/env python
# coding: utf-8

r"""Importing multiple shapes from STEP"""

from __future__ import print_function

import logging

from OCC.Display.SimpleGui import init_display
# from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_GRAY3

from aocutils.display.topology import solids
from aocutils.display.defaults import backend

from aocxchange.step import StepImporter
from corelib.core.files import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')
backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)

# filename = path_from_file(__file__, "./models_in/step/dm1-id-214.stp")
# filename = path_from_file(__file__,
#                           "./models_in/step/APB_GC.stp")  # big file 50 Mb !
# filename = path_from_file(__file__, "./models_in/step/66m.stp")
filename = path_from_file(__file__, "./models_in/step/ASA.STEP")
# filename = path_from_file(__file__, "./models_in/step/Groupama_VO70.stp")
step_importer = StepImporter(filename)

the_shapes = step_importer.shapes
print("Nb shapes : %i" % len(the_shapes))  # 4
# print("number_of_shapes(): %i" % step_importer.number_of_shapes)  # 0 ??

# display.DisplayColoredShape(the_shapes[0], Quantity_Color(Quantity_NOC_GRAY3))
solids(display, the_shapes[0])
display.FitAll()
display.View_Iso()
start_display()
