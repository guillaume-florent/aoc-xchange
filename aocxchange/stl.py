#!/usr/bin/python
# coding: utf-8

r"""STL module of aocxchange"""

from __future__ import print_function

import logging

import OCC.StlAPI
import OCC.TopoDS

import aocxchange.exceptions
import aocxchange.extensions
import aocxchange.utils
import aocxchange.checks

logger = logging.getLogger(__name__)


class StlImporter(object):
    r"""STL importer

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename):
        logger.info("StlImporter instantiated with filename : %s" % filename)

        aocxchange.checks.check_importer_filename(filename, aocxchange.extensions.stl_extensions)
        self._filename = filename
        self._shape = None

        logger.info("Reading file ....")
        self.read_file()

    def read_file(self):
        r"""Read the STL file and stores the result in a TopoDS_Shape"""
        stl_reader = OCC.StlAPI.StlAPI_Reader()
        shape = OCC.TopoDS.TopoDS_Shape()
        print(self._filename)
        stl_reader.Read(shape, self._filename)
        self._shape = shape

    @property
    def shape(self):
        r"""Shape"""
        if self._shape.IsNull():
            raise AssertionError("Error: the shape is NULL")
        else:
            return self._shape


class StlExporter(object):
    """ A TopoDS_Shape to STL exporter. Default mode is ASCII

    Parameters
    ----------
    filename : str
    ascii_mode : bool
        (default is False)
    """
    def __init__(self, filename=None, ascii_mode=False):
        logger.info("StlExporter instantiated with filename : %s" % filename)
        logger.info("StlExporter ascii : %s" % str(ascii_mode))

        aocxchange.checks.check_exporter_filename(filename,
                                                  aocxchange.extensions.stl_extensions)
        aocxchange.checks.check_overwrite(filename)

        self._shape = None  # only one shape can be exported
        self._ascii_mode = ascii_mode
        self._filename = filename

    def set_shape(self, a_shape):
        """
        only a single shape can be exported...

        Parameters
        ----------
        a_shape

        """
        # raises an exception if the shape is not valid
        aocxchange.checks.check_shape(a_shape)

        self._shape = a_shape

    def write_file(self):
        r"""Write file"""
        stl_writer = OCC.StlAPI.StlAPI_Writer()

        # Cross OCC versions STL writing
        try:
            stl_writer.Write(self._shape, self._filename, self._ascii_mode)
        except TypeError:
            stl_writer.SetASCIIMode(self._ascii_mode)
            stl_writer.Write(self._shape, self._filename)

        # stl_writer.Write(self._shape, self._filename)
        logger.info("Wrote STL file")
