#!/usr/bin/env python
# coding: utf-8

r"""Importing multiple shapes from STEP"""

from __future__ import print_function

import logging

import OCC.Display.SimpleGui
import OCC.Quantity

import aocutils.display.topology
import aocutils.display.defaults

import aocxchange.step
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')
backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

# filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/dm1-id-214.stp")
# filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/APB_GC.stp")  # big file 50 Mb !
# filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/66m.stp")
filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/ASA.STEP")
# filename = aocxchange.utils.path_from_file(__file__, "./models_in/step/Groupama_VO70.stp")
step_importer = aocxchange.step.StepImporter(filename)

the_shapes = step_importer.shapes
print("Nb shapes : %i" % len(the_shapes))  # 4
# print("number_of_shapes(): %i" % step_importer.number_of_shapes)  # 0 ??

# display.DisplayColoredShape(the_shapes[0], OCC.Quantity.Quantity_Color(OCC.Quantity.Quantity_NOC_GRAY3))
aocutils.display.topology.solids(display, the_shapes[0])
display.FitAll()
display.View_Iso()
start_display()
