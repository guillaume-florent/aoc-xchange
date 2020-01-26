# coding: utf-8

r"""utils module of aocxchange"""

from __future__ import print_function

import logging
import warnings
import os

# import corelib.core.files
import corelibpy

logger = logging.getLogger(__name__)


def path_from_file(file_origin, relative_path):
    r"""Builds an absolute path from a file using a relative path

    file_origin (absolute path) + relative_path (from file_origin) -> returned path

    Parameters
    ----------
    file_origin : str
        Full / absolute path to the file from which the path is to be built
    relative_path : str
        The relative path from file_origin

    Returns
    -------
    str
        Absolute file path

    """
    # # Check file_origin exists
    # if not os.path.isfile(file_origin):
    #     msg = "File %s not found." % file_origin
    #     logger.error(msg)
    #     raise FileNotFoundError(msg)
    #
    # dir_of_file_origin = os.path.dirname(os.path.realpath(file_origin))
    # return os.path.abspath(os.path.join(dir_of_file_origin, relative_path))

    warnings.warn("aocxchange.utils.path_from_file is deprecated, "
                  "use corelibpy.path_from_file or corelibpy.p_ instead")
    return corelibpy.path_from_file(file_origin, relative_path)


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
