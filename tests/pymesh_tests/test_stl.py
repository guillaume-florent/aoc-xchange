#!/usr/bin/env python
# coding: utf-8

r"""checks.py module tests"""

# import pytest

# from corelib.core.files import p_
from corelibpy import p_
from aocxchange.pymesh.stl import Stl


def test_happy_path_ascii():
    r"""Test opening an ASCII file"""
    s = Stl(filename=p_(__file__, "../models_in/2_boxes_ascii.stl"))
    assert s is not None
    assert s.name == "solid"
    assert s.mode == Stl.MODE_ASCII


def test_happy_path_binary():
    r"""Test opening a binary file"""
    s = Stl(filename=p_(__file__, "../models_in/2_boxes_binary.stl"))
    assert s is not None
    assert s.name == ""
    assert s.mode == Stl.MODE_BINARY