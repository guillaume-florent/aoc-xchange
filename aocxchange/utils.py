# coding: utf-8

r"""utils module of aocxchange"""

import logging
import os

logger = logging.getLogger(__name__)


def path_from_file(file_origin, relative_path):
    r"""Builds an absolute path from a file using a relative path
    Parameters
    ----------
    file_origin : str
        Full / absolute path to he file from which the path is to be built
    relative_path : str
        The relative path from file_origin
    Returns
    -------
    str
        Absolute file path
    """
    # Check the file exists
    # assert os.path.isfile(file_origin)
    if not os.path.isfile(file_origin):
        msg = "The file_origin parameter refers to a path that does not exist"
        raise ValueError(msg)
    dir_of_file_origin = os.path.dirname(os.path.realpath(file_origin))
    return os.path.abspath(os.path.join(dir_of_file_origin, relative_path))


# Make it possible to use a shorter syntax
p_ = path_from_file


def extract_file_extension(filename):
    r"""Extract the extension from the file name

    Parameters
    ----------
    filename : str
        Path to the file

    Returns
    -------
    str
        The file extension

    """
    # if "." not in filename.split("/")[-1]:
    #     return ""
    # else:
    #     return (filename.split("/")[-1]).split(".")[-1]

    # Switching to a more cross-OS version
    return os.path.splitext(filename)[1][1:]
