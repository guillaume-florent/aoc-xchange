# coding: utf-8

r"""STL module of aocxchange"""

from __future__ import print_function

import logging

from OCC.StlAPI import StlAPI_Reader, StlAPI_Writer
from OCC.TopoDS import TopoDS_Shape

from aocutils.mesh import mesh

# import aocxchange.exceptions
from aocxchange.extensions import stl_extensions
# import aocxchange.utils
from aocxchange.checks import check_importer_filename, check_exporter_filename,\
    check_overwrite, check_shape

logger = logging.getLogger(__name__)


class StlImporter(object):
    r"""STL importer

    Parameters
    ----------
    filename : str

    """
    def __init__(self, filename):
        logger.info("StlImporter instantiated with filename : %s" % filename)

        check_importer_filename(filename, stl_extensions)
        self._filename = filename
        self._shape = None

        logger.info("Reading file ....")
        self.read_file()

    def read_file(self):
        r"""Read the STL file and stores the result in a TopoDS_Shape"""
        stl_reader = StlAPI_Reader()
        shape = TopoDS_Shape()
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

        check_exporter_filename(filename, stl_extensions)
        check_overwrite(filename)

        self._shape = None  # only one shape can be exported
        self._ascii_mode = ascii_mode
        self._filename = filename

    def set_shape(self, a_shape, factor=4000., use_min_dim=False):
        """
        only a single shape can be exported...

        Parameters
        ----------
        a_shape
        factor : float
            Meshing factor, the higher the finer the mesh
        use_min_dim: bool
            Use the smallest dimension as a base for shape meshing
            Useful for shapes with high aspect ratios

        """
        # raises an exception if the shape is not valid
        check_shape(a_shape)
        mesh(shape=a_shape, factor=factor, use_min_dim=use_min_dim)
        self._shape = a_shape

    def write_file(self):
        r"""Write file"""
        statuses = {0: "StlAPI_StatusOK",
                    1: "StlAPI_MeshIsEmpty",
                    2: "StlAPI_CannotOpenFile",
                    3: "StlAPI_WriteError"}
        stl_writer = StlAPI_Writer()

        # Cross OCC versions STL writing
        try:
            status = stl_writer.Write(self._shape, self._filename, self._ascii_mode)
        except TypeError:
            stl_writer.SetASCIIMode(self._ascii_mode)
            status = stl_writer.Write(self._shape, self._filename)

        if status != 0:
            msg = "STL write failed with code %i (%s)" % (status,
                                                          statuses[status])
            logger.error(msg)
            raise RuntimeError(msg)

        # stl_writer.Write(self._shape, self._filename)
        logger.info("Wrote STL file")
