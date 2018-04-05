#!/usr/bin/env python
# coding: utf-8

r"""Importing STL"""

import logging

from OCC.Display.SimpleGui import init_display

from aocutils.display.topology import shells
from aocutils.display.defaults import backend

from aocxchange.stl import StlImporter
from aocxchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

# open/parse STL file and get the resulting TopoDS_Shape instance
# filename = path_from_file(__file__, "./models_in/sample.stl")
# filename = path_from_file(__file__, "./models_in/USS_Albacore.STL")
filename = path_from_file(__file__, "./models_in/stl/USS_Albacore.STL")
my_stl_importer = StlImporter(filename)
the_shape = my_stl_importer.shape

# Then display the shape
backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)
# display.DisplayShape(the_shape, color='BLUE', update=True)

# 1 shell to display
shells(display, the_shape)
# faces
# faces(display, the_shape, show_numbers=False)  # super slow !!
display.FitAll()
display.View_Iso()
start_display()
