#!/usr/bin/python
# coding: utf-8

r"""Example of converting a STEP file to OBJ"""

import logging

from os.path import abspath, join, dirname

from aocxchange.convert.step_to_obj import step_to_obj

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s :: %(levelname)6s :: %(module)20s '
                               ':: %(lineno)3d :: %(message)s')
    step_ = abspath(join(dirname(__file__), "./models_in/step/aube_pleine.stp"))
    obj_ = abspath(join(dirname(__file__), "./models_out/aube_pleine.obj"))
    step_to_obj(step_, obj_)
