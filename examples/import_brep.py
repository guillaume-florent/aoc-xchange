#!/usr/bin/env python
# coding: utf-8

r"""Importing BREP"""

import logging

from OCC.Display.SimpleGui import init_display

from aocutils.display.topology import solids
from aocutils.display.defaults import backend

from aocxchange.brep import BrepImporter
# from corelib.core.files import path_from_file
from corelibpy import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

# open/parse BREP file and get the resulting TopoDS_Shape instance
filename = path_from_file(__file__, "./models_in/brep/carter.brep")
my_brep_importer = BrepImporter(filename)
the_shape = my_brep_importer.shape

# Then display the shape
backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)
# display.DisplayShape(the_shape, color='BLUE', update=True)

# 1 solid to display
solids(display, the_shape)
# faces
# faces(display, the_shape, show_numbers=False)  # super slow !!
display.FitAll()
display.View_Iso()
start_display()
