# coding: utf-8

r"""BREP module of aocxchange"""

from __future__ import print_function

import logging

from OCC.Core.BRep import BRep_Builder
from OCC.Core.BRepTools import breptools_Write, breptools_Read
from OCC.Core.Message import Handle_Message_ProgressIndicator
from OCC.Core.TopoDS import TopoDS_Shape

# import aocxchange.exceptions
from aocxchange.extensions import brep_extensions
# import aocxchange.utils
from aocxchange.checks import check_importer_filename, check_exporter_filename,\
    check_overwrite, check_shape

logger = logging.getLogger(__name__)


class BrepImporter(object):
    r"""Brep importer

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename):
        logger.info("BrepImporter instantiated with filename : %s" % filename)

        check_importer_filename(filename, brep_extensions)
        self._filename = filename
        self._shape = None

        logger.info("Reading file ....")
        self.read_file()

    def read_file(self):
        r"""Read the BREP file and stores the result in a TopoDS_Shape"""
        shape = TopoDS_Shape()
        builder = BRep_Builder()
        breptools_Read(shape, self._filename, builder)
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

        check_exporter_filename(filename, brep_extensions)
        check_overwrite(filename)

        self._shape = None  # only one shape can be exported
        self._filename = filename

    def set_shape(self, a_shape):
        """
        only a single shape can be exported...

        Parameters
        ----------
        a_shape

        """
        check_shape(a_shape)  # raises an exception if the shape is not valid
        self._shape = a_shape

    def write_file(self):
        r"""Write file"""
        logger.info("Writing brep : {cad_file}".format(cad_file=self._filename))
        builder = Handle_Message_ProgressIndicator()
        breptools_Write(self._shape, self._filename, builder)
        logger.info("Wrote BREP file")
