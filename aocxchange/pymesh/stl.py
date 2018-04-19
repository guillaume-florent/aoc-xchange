# coding: utf-8

r"""STL format mesh"""

from __future__ import absolute_import, print_function

import logging
import numpy
import os
import struct

from corelib.core.python_ import py3
from corelib.core.files import is_binary

from .base import BaseMesh


logger = logging.getLogger(__name__)


class Stl(BaseMesh):
    r"""STL mesh class"""

    MODE_AUTO = 0
    MODE_ASCII = 1
    MODE_BINARY = 2

    HEADER_SIZE = 80
    COUNT_SIZE = 4
    MAX_COUNT = 1e6
    BUFFER_SIZE = 4096

    stl_dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, )),
    ])

    def __init__(self, filename=None, mode_policy=MODE_AUTO):
        """Create a instance of Stl.

        Parameters
        ----------
        filename : str
            The filename to open
        mode_policy: int
            The mode to open, default is MODE_AUTO.
            0 : MODE_AUTO
            1 : MODE_ASCII
            2 : MODE_BINARY

        """
        super(Stl, self).__init__()

        if filename is None:
            # Create EMPTY data
            self.name = "empty"
            self.data = numpy.zeros(0, dtype=Stl.stl_dtype)
            self.mode = Stl.MODE_BINARY

        else:
            # Create data from file
            if py3() is True:
                if is_binary(filename):
                    mode = "rb"
                else:
                    mode = "r"
            else:
                mode = "rb"
            with open(filename, mode) as fh:
                name, data, mode = Stl.__load(fh, mode=mode_policy)
            self.name = name
            self.data = data
            self.mode = mode

        super(Stl, self).set_initial_values()
        return

    @staticmethod
    def __load(fh, mode=MODE_AUTO):
        """Load Mesh from STL file

        Parameters
        ----------
        fh : FileIO
            The file handle to open
        mode : int
            The mode to open, default is MODE_AUTO.
            0 : MODE_AUTO
            1 : MODE_ASCII
            2 : MODE_BINARY

        """
        header = fh.read(Stl.HEADER_SIZE).lower()
        name = ""
        data = None
        if not header.strip():
            return

        if fh.mode == "r":
            try:
                name = header.split('\n', 1)[0][:5].strip()
                data = Stl.__load_ascii(fh, header)
                mode = Stl.MODE_ASCII
            except:
                # NO pass after except (GF 27 OCT 2017)
                msg = "Error in header splitting or ascii loading"
                logger.warning(msg)
                # pass
        elif fh.mode == "rb":
            data = Stl.__load_binary(fh)
            mode = Stl.MODE_BINARY

        # if mode in (Stl.MODE_AUTO, Stl.MODE_ASCII) and \
        #         header.startswith('solid'):
        #     try:
        #         name = header.split('\n', 1)[0][:5].strip()
        #         data = Stl.__load_ascii(fh, header)
        #         mode = Stl.MODE_ASCII
        #     except:
        #         # NO pass after except (GF 27 OCT 2017)
        #         msg = "Error in header splitting or ascii loading"
        #         logger.warning(msg)
        #         # pass
        #
        # else:
        #     data = Stl.__load_binary(fh)
        #     mode = Stl.MODE_BINARY

        return name, data, mode

    @staticmethod
    def __load_binary(fh):
        # Read the triangle count
        count, = struct.unpack("i", fh.read(Stl.COUNT_SIZE))
        # assert count < Stl.MAX_COUNT, \
        #     'File too large, got {} triangles ' \
        #     'which exceeds the maximum of {}' .format(count, Stl.MAX_COUNT)
        if count >= Stl.MAX_COUNT:
            msg = 'File too large, got {} triangles which exceeds ' \
                  'the maximum of {}' .format(count, Stl.MAX_COUNT)
            logger.error(msg)
            raise RuntimeError(msg)
        return numpy.fromfile(fh, Stl.stl_dtype, count=count)

    @staticmethod
    def __load_ascii(fh, header):
        return numpy.fromiter(Stl.__ascii_reader(fh, header),
                              dtype=Stl.stl_dtype)

    @staticmethod
    def __ascii_reader(fh, header):
        """
        
        Parameters
        ----------
        fh
        header
        
        """

        lines = header.split('\n')
        recoverable = [True]

        def get(prefix=''):
            r"""
            
            Parameters
            ----------
            prefix : str

            Returns
            -------
            list[float] if prefix evaluates to True
            str if prefix evaluates to False

            """
            if lines:
                line = lines.pop(0)
            else:
                raise RuntimeError(recoverable[0], 'Unable to find more lines')

            if not lines:
                recoverable[0] = False

                # Read more lines and make sure we prepend any old data
                lines[:] = fh.read(Stl.BUFFER_SIZE).split('\n')
                line += lines.pop(0)
            line = line.lower().strip()

            if prefix:
                if line.startswith(prefix):
                    values = line.replace(prefix, '', 1).strip().split()
                elif line.startswith('endsolid'):
                    raise StopIteration()
                else:
                    raise RuntimeError(recoverable[0],
                                       '%r should start with %r' % (line,
                                                                    prefix))

                if len(values) == 3:
                    vertex = [float(v) for v in values]
                    return vertex
                else:  # pragma: no cover
                    raise RuntimeError(recoverable[0],
                                       'Incorrect value %r' % line)
            else:
                return line

        line = get()
        if not line.startswith('solid ') and line.startswith('solid'):
            msg = "Missing space after solid"
            logger.warning(msg)
            # print("Error")

        if not lines:
            raise RuntimeError(recoverable[0],
                               'No lines found, impossible to read')

        while True:
            # Read from the header lines first, until that point we can recover
            # and go to the binary option. After that we cannot due to
            # unseekable files such as sys.stdin
            #
            # Numpy doesn't support any non-file types so wrapping with a
            # buffer and/or StringIO does not work.
            try:
                normals = get('facet normal')
                # assert get() == 'outer loop'
                if get() != 'outer loop':
                    msg = "get() is different from 'outer_loop'"
                    logger.error(msg)
                    raise AssertionError(msg)
                v0 = get('vertex')
                v1 = get('vertex')
                v2 = get('vertex')
                # assert get() == 'endloop'
                if get() != 'endloop':
                    msg = "get() is different from 'endloop'"
                    logger.error(msg)
                    raise AssertionError(msg)
                # assert get() == 'endfacet'
                if get() != 'endfacet':
                    msg = "get() is different from 'endfacet'"
                    logger.error(msg)
                    raise AssertionError(msg)
                attrs = 0
                yield (normals, (v0, v1, v2), attrs)
            except AssertionError as e:
                raise RuntimeError(recoverable[0], e)
            except StopIteration:
                if any(lines):
                    # Seek back to where the next solid should begin
                    fh.seek(-len('\n'.join(lines)), os.SEEK_CUR)
                raise
