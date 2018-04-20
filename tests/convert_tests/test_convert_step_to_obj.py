#!/usr/bin/env python
# coding: utf-8

r"""step_to_obj.py module tests"""

# import pytest

from os.path import isfile

from corelib.core.files import p_

from aocxchange.convert.step_to_obj import step_to_obj


def test_happy_path():
    step_to_obj(p_(__file__, "../models_in/aube_pleine.stp"),
                obj_file_path=p_(__file__, "../models_out/aube_pleine.obj"))
    assert isfile(p_(__file__, "../models_out/aube_pleine.obj"))
