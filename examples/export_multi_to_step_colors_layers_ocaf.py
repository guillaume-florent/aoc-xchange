#!/usr/bin/env python
# coding: utf-8

r"""Exporting multiple shapes to STEP with colors and layers"""

import logging

import OCC.BRepPrimAPI
import OCC.Display.SimpleGui

import aocutils.display.defaults

import aocxchange.step_ocaf

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')

# First create a simple shape to export
my_box_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(50, 50, 50).Shape()
my_sphere_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeSphere(20).Shape()

# Export to STEP
my_step_exporter = aocxchange.step_ocaf.StepOcafExporter("./models_out/result_export_multi_ocaf.stp")
my_step_exporter.set_color(r=1, g=0, b=0)  # red
my_step_exporter.set_layer('red')
my_step_exporter.add_shape(my_box_shape)
my_step_exporter.set_color(r=0, g=1, b=0)  # green
my_step_exporter.set_layer('green')
my_step_exporter.add_shape(my_sphere_shape)
my_step_exporter.write_file()

# Read the exported STEP file back
my_step_importer = aocxchange.step_ocaf.StepOcafImporter("./models_out/result_export_multi_ocaf.stp")
# my_step_importer = aocxchange.step_ocaf.StepOcafImport("./models_in/66m.stp")
# my_step_importer.read_file()
the_shapes = my_step_importer.shapes
the_colors = my_step_importer.colors
the_layers = my_step_importer.layers
the_layers_str = my_step_importer.layers_str

print("Number of shapes : %i " % len(the_shapes))

backend = aocutils.display.defaults.backend
display, start_display, add_menu, add_function_to_menu = OCC.Display.SimpleGui.init_display(backend)

for i, shape in enumerate(the_shapes):
    display.DisplayShape(shape, color=the_colors[i])
    print(the_layers_str[i])

display.View_Iso()
display.FitAll()
start_display()
