#!/usr/bin/env python
# coding: utf-8

r"""Importing BREP"""

import logging

import OCC.Display.SimpleGui

import aocutils.display.topology
import aocutils.display.defaults

import aocxchange.brep
import aocxchange.utils

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# open/parse BREP file and get the resulting TopoDS_Shape instance
filename = aocxchange.utils.path_from_file(__file__, "./models_in/brep/carter.brep")
my_brep_importer = aocxchange.brep.BrepImporter(filename)
the_shape = my_brep_importer.shape

# Then display the shape
backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)
# display.DisplayShape(the_shape, color='BLUE', update=True)

# 1 solid to display
aocutils.display.topology.solids(display, the_shape)
# faces
# aocutils.display.topology.faces(display, the_shape, show_numbers=False)  # super slow !!
display.FitAll()
display.View_Iso()
start_display()
