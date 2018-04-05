# coding: utf-8

r"""BREP module of aocxchange"""

from __future__ import print_function

import logging

import OCC.BRep
import OCC.BRepTools
import OCC.Message
import OCC.TopoDS

import aocxchange.exceptions
import aocxchange.extensions
import aocxchange.utils
import aocxchange.checks

logger = logging.getLogger(__name__)


class BrepImporter(object):
    r"""Brep importer

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename):
        logger.info("BrepImporter instantiated with filename : %s" % filename)

        aocxchange.checks.check_importer_filename(filename, aocxchange.extensions.brep_extensions)
        self._filename = filename
        self._shape = None

        logger.info("Reading file ....")
        self.read_file()

    def read_file(self):
        r"""Read the BREP file and stores the result in a TopoDS_Shape"""
        shape = OCC.TopoDS.TopoDS_Shape()
        builder = OCC.BRep.BRep_Builder()
        OCC.BRepTools.breptools_Read(shape, self._filename, builder)
        self._shape = shape

    @property
    def shape(self):
        r"""Shape"""
        if self._shape.IsNull():
            raise AssertionError("Error: the shape is NULL")
        else:
            return self._shape


class BrepExporter(object):
    """ A TopoDS_Shape to BREP exporter.

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename=None):
        logger.info("BrepExporter instantiated with filename : %s" % filename)

        aocxchange.checks.check_exporter_filename(filename, aocxchange.extensions.brep_extensions)
        aocxchange.checks.check_overwrite(filename)

        self._shape = None  # only one shape can be exported
        self._filename = filename

    def set_shape(self, a_shape):
        """
        only a single shape can be exported...

        Parameters
        ----------
        a_shape

        """
        aocxchange.checks.check_shape(a_shape)  # raises an exception if the shape is not valid
        self._shape = a_shape

    def write_file(self):
        r"""Write file"""
        logger.info("Writing brep : {cad_file}".format(cad_file=self._filename))
        builder = OCC.Message.Handle_Message_ProgressIndicator()
        OCC.BRepTools.breptools_Write(self._shape, self._filename, builder)
        logger.info("Wrote BREP file")
