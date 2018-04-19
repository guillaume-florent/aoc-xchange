#!/usr/bin/env python
# coding: utf-8

r"""checks.py module tests"""

# import pytest

from os.path import isfile

from corelib.core.files import p_
from aocxchange.pymesh.stl import Stl
from aocxchange.pymesh.obj import Obj


def test_happy_path():
    r"""Test opening an ASCII file"""
    mesh = Stl(filename=p_(__file__, "../models_in/2_boxes_ascii.stl"))

    # Save as OBJ
    mesh.save_obj(p_(__file__, "../models_out/2_boxes.obj"),
                  update_normals=True,
                  write_normals=False)

    # reopen obj file
    mesh = Obj(p_(__file__, "../models_out/2_boxes.obj"))

    assert mesh is not None
    assert mesh.data is not None
    # assert mesh.normals == []
    assert len(mesh.vectors) > 10

    # Save as OBJ
    mesh.save_obj(p_(__file__, "../models_out/2_boxes_with_normals.obj"),
                  update_normals=True,
                  write_normals=True)

    assert isfile(p_(__file__, "../models_out/2_boxes_with_normals.obj"))
