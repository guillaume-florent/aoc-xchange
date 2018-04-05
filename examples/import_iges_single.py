#!/usr/bin/env python
# coding: utf-8

r"""Importing single shape from IGES"""

from __future__ import print_function

import logging

from OCC.Display.SimpleGui import init_display

from aocutils.display.topology import faces
from aocutils.display.defaults import backend

from aocxchange.iges import IgesImporter
from aocxchange.utils import path_from_file

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: '
                           '%(lineno)3d :: %(message)s')

backend = backend
display, start_display, add_menu, add_function_to_menu = init_display(backend)

filename = path_from_file(__file__, "./models_in/iges/aube_pleine.iges")
iges_importer = IgesImporter(filename)

print(iges_importer.nb_shapes)  # 13
print(len(iges_importer.shapes))  # 13


the_compound = iges_importer.compound
# display.DisplayShape(the_compound)

# there are no shells or solids in the compound (IGES specific)
faces(display, iges_importer.compound)


display.FitAll()
display.View_Iso()
start_display()
