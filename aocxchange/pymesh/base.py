# coding: utf-8

r"""Base mesh"""

from __future__ import absolute_import, print_function

import logging

import datetime
import math
import os
import struct

import numpy

# used in header of written STL or OBJ files
from aocxchange import __name__, __version__, __url__


logger = logging.getLogger(__name__)


MODE_STL_AUTO = 0
MODE_STL_ASCII = 1
MODE_STL_BINARY = 2


class BaseMesh(object):
    r"""Base mesh class"""

    stl_dtype = numpy.dtype([
        ('normals', numpy.float32, (3, )),
        ('vectors', numpy.float32, (3, 3)),
        ('attr', numpy.uint16, (1, )),
    ])

    def __init__(self):
        self.data = None
        self.normals = []
        self.vectors = []
        self.attr = []
        self.mode = MODE_STL_BINARY

    def set_initial_values(self):
        """Set initial values form existing self.data value"""
        self.normals = self.data['normals']
        self.vectors = numpy.ones((
            self.data['vectors'].shape[0],
            self.data['vectors'].shape[1],
            self.data['vectors'].shape[2] + 1
        ))
        self.vectors[:, :, :-1] = self.data['vectors']
        self.attr = self.data['attr']
        return

    def rotate_x(self, deg):
        """Rotate mesh around x-axis

        Parameters
        ----------
        deg : float
            Rotation angle (degree)

        """
        rad = math.radians(deg)
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, math.cos(rad), math.sin(rad), 0],
            [0, -math.sin(rad), math.cos(rad), 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def rotate_y(self, deg):
        """Rotate mesh around y-axis

        Parameters
        ----------
        deg : float
            Rotation angle (degree)

        """
        rad = math.radians(deg)
        mat = numpy.array([
            [math.cos(rad), 0, -math.sin(rad), 0],
            [0, 1, 0, 0],
            [math.sin(rad), 0, math.cos(rad), 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def rotate_z(self, deg):
        """Rotate mesh around z-axis

        Parameters
        ----------
        deg : float
            Rotation angle (degree)

        """
        rad = math.radians(deg)
        mat = numpy.array([
            [math.cos(rad), math.sin(rad), 0, 0],
            [-math.sin(rad), math.cos(rad), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def translate_x(self, d):
        """Translate mesh for x-direction

        Parameters
        ----------
        d : float
            Distance to translate

        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [d, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def translate_y(self, d):
        """Translate mesh for y-direction

        Parameters
        ----------
        d : float
            Distance to translate

        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, d, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def translate_z(self, d):
        """Translate mesh for z-direction

        Parameters
        ----------
        d : float
            Distance to translate

        """
        mat = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, d, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def scale(self, sx, sy, sz):
        """Scale mesh

        Parameters
        ----------
        sx: float
            Scaling factor for x-direction
        sy: float
            Scaling factor for y-direction
        sz: float
            Scaling factor for z-direction

        """
        mat = numpy.array([
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ])
        self.vectors = self.vectors.dot(mat)
        return self

    def join(self, another):
        """Join mesh with another mesh

        another : BaseMesh
            The mesh to join

        """
        if another is None:
            raise AttributeError("another BaseMesh instance is required")

        if not isinstance(another, BaseMesh):
            raise TypeError("anther must be an instance of BaseMesh")

        self.data = numpy.append(self.data, another.data)
        self.normals = numpy.append(self.normals, another.normals, axis=0)
        self.vectors = numpy.append(self.vectors, another.vectors, axis=0)
        self.attr = numpy.append(self.attr, another.attr, axis=0)
        return self

    def update_normals(self):
        r"""Update mesh normals"""
        v0 = self.vectors[:, 0, :3]
        v1 = self.vectors[:, 1, :3]
        v2 = self.vectors[:, 2, :3]
        _normals = numpy.cross(v1 - v0, v2 - v0)

        for i, _normal in enumerate(_normals):
            norm = numpy.linalg.norm(_normal)
            if norm != 0:
                _normals[i] /= numpy.linalg.norm(_normal)

        self.normals[:] = _normals
        return self

    #
    # Analyze functions
    #
    def get_volume(self):
        r"""Volume of the mesh

        Returns
        -------
        float : the volume

        """
        total_volume = 0
        for triangle in self.vectors:
            total_volume += BaseMesh.__calc_signed_volume(triangle)
        return total_volume

    @staticmethod
    def __calc_signed_volume(triangle):
        """ Calculate signed volume of given triangle

        Parameters
        ----------
        triangle : list[list]

        Returns
        -------
        float

        """
        v321 = triangle[2][0] * triangle[1][1] * triangle[0][2]
        v231 = triangle[1][0] * triangle[2][1] * triangle[0][2]
        v312 = triangle[2][0] * triangle[0][1] * triangle[1][2]
        v132 = triangle[0][0] * triangle[2][1] * triangle[1][2]
        v213 = triangle[1][0] * triangle[0][1] * triangle[2][2]
        v123 = triangle[0][0] * triangle[1][1] * triangle[2][2]

        signed_volume = (-v321 + v231 + v312 - v132 - v213 + v123) / 6.0
        return signed_volume

    #
    # Save functions
    #

    # STL
    def save_stl(self, filename, mode=MODE_STL_AUTO, update_normals=True):
        """Save data in stl format
        
        Parameters
        ----------
        filename : str
            The stl file name
        mode : int
            0 : MODE_STL_AUTO
            1 : MODE_STL_ASCII
            2 : MODE_STL_BINARY
        update_normals: bool

        """
        if update_normals:
            self.update_normals()

        name = os.path.split(filename)[-1]

        if mode is MODE_STL_AUTO:
            if self.mode == MODE_STL_BINARY:
                save_func = self.__save_stl_binary

            elif self.mode == MODE_STL_ASCII:
                save_func = self.__save_stl_ascii

            else:
                raise ValueError("Mode %r is invalid" % mode)

        elif mode is MODE_STL_BINARY:
            save_func = self.__save_stl_binary

        else:
            raise ValueError("Mode %r is invalid" % mode)

        with open(name, 'wb') as fh:
            save_func(fh, filename)

    def __save_stl_binary(self, fh, name):
        fh.write(("%s (%s) %s %s" % (
            "{}".format(__name__),
            "{}".format(__version__),
            datetime.datetime.now(),
            name
        ))[:80].ljust(80, ' '))

        bin_data = numpy.zeros(self.data.size, BaseMesh.stl_dtype)
        bin_data['normals'] = self.normals[:]
        bin_data['vectors'] = self.vectors[:, :, :3]
        bin_data['attr'] = self.attr
        fh.write(struct.pack('i', bin_data.size))
        bin_data.tofile(fh)

    def __save_stl_ascii(self, fh, name):
        print("solid {}".format(name), file=fh)
        for i, vector in enumerate(self.vectors):
            print("facet normal %f %f %f" % tuple(self.normals[i][:3]),
                  file=fh)
            print("  outer loop", file=fh)
            print("    vertex %f %f %f" % tuple(vector[0][:3]),
                  file=fh)
            print("    vertex %f %f %f" % tuple(vector[1][:3]),
                  file=fh)
            print("    vertex %f %f %f" % tuple(vector[2][:3]),
                  file=fh)
            print("  endloop", file=fh)
            print("endfacet", file=fh)
        print("endsolid {}".format(name), file=fh)

    # OBJ
    def save_obj(self,
                 filename,
                 update_normals=True,
                 write_normals=False,
                 group=True):
        """Save data in OBJ format
        
        Parameters
        ----------
        filename : str
            The obj file name
        update_normals : bool
        write_normals : bool
        group : bool
            Add a g entry before the f entries

        """
        if update_normals:
            self.update_normals()

        # Create triangle_list
        vectors_key_list = []
        vectors_list = []
        normals_key_list = []
        normals_list = []
        triangle_list = []
        for i, vector in enumerate(self.vectors):
            one_triangle = []
            for j in range(3):
                v_key = ",".join(map(str, vector[j][:3]))
                if v_key in vectors_key_list:
                    v_index = vectors_key_list.index(v_key)
                else:
                    v_index = len(vectors_key_list)
                    vectors_key_list.append(v_key)
                    vectors_list.append(vector[j][:3])
                one_triangle.append(v_index + 1)

            n_key = ",".join(map(str, self.normals[i][:3]))
            if n_key in normals_key_list:
                n_index = normals_key_list.index(n_key)
            else:
                n_index = len(normals_key_list)
                normals_key_list.append(n_key)
                normals_list.append(self.normals[i][:3])

            # print(normals_list)
            triangle_list.append((one_triangle, n_index + 1))

        # with open(filename, "wb") as fh:
        with open(filename, "w") as fh:
            print("# {} {}".format(__name__, __version__), file=fh)
            print("# {}".format(datetime.datetime.now()), file=fh)
            print("# {}".format(__url__), file=fh)
            # print("", file=fh)
            for v in vectors_list:
                print("v {} {} {}".format(v[0], v[1], v[2]), file=fh)
            if write_normals is True:
                for vn in normals_list:
                    print("vn {} {} {}".format(vn[0], vn[1], vn[2]), file=fh)
            if group is True:
                print("g patch0", file=fh)
            for t in triangle_list:
                faces = t[0]
                normal = t[1]
                if write_normals is True:
                    print("f {}//{} {}//{} {}//{}".format(
                        faces[0], normal,
                        faces[1], normal,
                        faces[2], normal,
                    ), file=fh)
                else:
                    print("f {} {} {}".format(
                        faces[0],
                        faces[1],
                        faces[2]
                    ), file=fh)

        logger.info("Wrote %s" % filename)
