#!/usr/bin/env python
# coding: utf-8

r"""Test the utils.py module of aocxchange"""

import pytest
import platform


from aocxchange.utils import path_from_file, extract_file_extension
from aocxchange.exceptions import FileNotFoundException


def test_path_from_file_inexistent_file():
    r"""Test that trying to build the path from an inexistent file fails"""
    with pytest.raises(FileNotFoundException):
        path_from_file("C:/file-does-not-exist.txt", "./test/test.txt")


def test_path_from_file_too_far_back():
    r"""Test trying to build the path with a relative path that uses .. too 
    many times and reaches root"""
    relpath = "../" * 40
    if platform.system() == "Windows":
        assert path_from_file(__file__, relpath + "test.txt") == "C:\\test.txt"
    elif platform.system() == "Linux":
        assert path_from_file(__file__, relpath + "test.txt") == "/test.txt"
    else:
        assert False  # Not implemented


def test_path_from_file_happy_path():
    r"""Create the absolute path from a file that is guaranteed to exists"""
    path_from_file(__file__, "./test.txt")


def test_extract_file_extension():
    r"""extract_file_extension() tests"""
    assert extract_file_extension("name.txt.dat") == "dat"
    assert extract_file_extension("name") == ""
    assert extract_file_extension("/home/username/name") == ""
    assert extract_file_extension("C:/users/username/name.") == ""
    assert extract_file_extension("C:/users/username/name.dat") == "dat"
    assert extract_file_extension("C:/users/user.name/name.dat") == "dat"
    assert extract_file_extension("C:/users/user.name/name") == ""
