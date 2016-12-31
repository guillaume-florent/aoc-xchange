#!/usr/bin/python
# coding: utf-8

r"""dat module of aocxchange

Summary
-------

Deals with .dat files, mostly used to define 2D foil sections

"""

import logging

import aocxchange.checks
import aocxchange.extensions

logger = logging.getLogger(__name__)


class DatImporter(object):
    r"""dat importer

    Parameters
    ----------
    filename : str
        Absolute filepath
    as_3d : bool
        If True, each point has 3 elements (x, y, z=0.), if False, each point has 2 elements (x, y)
    skip_first_line : bool
        If True, the first line of the .dat file is skipped

    """
    def __init__(self, filename, as_3d=False, skip_first_line=False):

        aocxchange.checks.check_importer_filename(filename, aocxchange.extensions.dat_extensions)
        self._filename = filename
        self._as_3d = as_3d
        self._skip_first_line = skip_first_line

        self._points = list()

        logger.info("Reading file ....")
        self.read_file()

    def read_file(self):
        r"""Read the .dat file"""

        points = list()
        with open(self._filename) as f:
            lines = f.readlines()

        if self._skip_first_line:
            lines = lines[1:]

        for line in lines:
            line = line.lstrip().rstrip().replace('    ', ' ').replace('   ', ' ').replace('  ', ' ')
            data = line.split(' ')  # data[0] = x coord.    data[1] = y coord.
            # 3 - create an array of points
            if len(data) == 2:  # two coordinates for each point
                if self._as_3d:
                    points.append((float(data[0]), float(data[1]), 0.0))
                else:
                    points.append((float(data[0]), float(data[1])))
        logger.info("%i points in .dat file" % len(points))
        self._points = points

    @property
    def points(self):
        r"""

        Returns
        -------
        list[tuple]

        """
        return self._points
