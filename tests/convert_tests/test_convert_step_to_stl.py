#!/usr/bin/env python
# coding: utf-8

r"""step_to_stl.py module tests"""

# import pytest

from os.path import isfile

# from corelib.core.files import p_
from corelibpy import p_

from aocxchange.convert.step_to_stl import step_to_stl


def test_happy_path():
    step_to_stl(p_(__file__, "../models_in/aube_pleine.stp"),
                stl_file_path=p_(__file__, "../models_out/aube_pleine.stl"))
    assert isfile(p_(__file__, "../models_out/aube_pleine.stl"))
