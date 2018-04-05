#!/usr/bin/env python
# coding: utf-8

r"""Test the utils.py module of aocxchange"""

import pytest
import logging

import aocxchange.utils
import aocxchange.exceptions

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s :: %(levelname)6s :: %(module)20s :: %(lineno)3d :: %(message)s')


def test_path_from_file_inexistent_file():
    r"""Test that trying to build the path from an inexistent file fails"""
    with pytest.raises(aocxchange.exceptions.FileNotFoundException):
        aocxchange.utils.path_from_file("C:/file-does-not-exist.txt", "./test/test.txt")


def test_path_from_file_too_far_back():
    r"""Test trying to build the path with a relative path that uses .. too many times and reaches root"""
    relpath = "../" * 40
    assert aocxchange.utils.path_from_file(__file__, relpath + "test.txt") == "C:\\test.txt"


def test_path_from_file_happy_path():
    r"""Create the absolute path from a file that is guaranteed to exists"""
    aocxchange.utils.path_from_file(__file__, "./test.txt")


def test_extract_file_extension():
    r"""extract_file_extension() tests"""
    assert aocxchange.utils.extract_file_extension("name.txt.dat") == "dat"
    assert aocxchange.utils.extract_file_extension("name") == ""
    assert aocxchange.utils.extract_file_extension("/home/username/name") == ""
    assert aocxchange.utils.extract_file_extension("C:/users/username/name.") == ""
    assert aocxchange.utils.extract_file_extension("C:/users/username/name.dat") == "dat"
    assert aocxchange.utils.extract_file_extension("C:/users/user.name/name.dat") == "dat"
    assert aocxchange.utils.extract_file_extension("C:/users/user.name/name") == ""
