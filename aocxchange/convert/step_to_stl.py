# coding: utf-8

r"""Convert a STEP file to STL file"""

import logging

from os.path import join, dirname, abspath, isfile

from aocxchange.step import StepImporter
from aocxchange.stl import StlExporter

from aocutils.mesh import mesh
from aocutils.operations.transform import scale_uniform

from OCC.gp import gp_Pnt

logger = logging.getLogger(__name__)

# Modes for conversion when more than 1 shape is present in the STEP file
ONE_SHAPE_PER_FILE = 0
ALL_SHAPES_IN_ONE_FILE = 1


def step_to_stl(step_file_path,
                stl_file_path,
                scale=1.,
                factor=4000.,
                use_min_dim=False,
                ascii_mode=True,
                multi_shape_mode=ONE_SHAPE_PER_FILE):
    r"""Convert a STEP file to a STL file

    Parameters
    ----------
    step_file_path
    stl_file_path
    factor : float
        Meshing factor, optional (default is 4000.)
        The higher, the finer the mesh and the bigger the resulting file
    use_min_dim : bool, optional (default is False)
        Use the minimum dimension of the shape as a base for meshing
        This is useful for shapes with a high aspect ratio
    ascii_mode : bool, optional (default is True)
        Write STL in ascii mode if True, in binary mode if False
    multi_shape_mode : int, optional (default is 0 (ONE_SHAPE_PER_FILE)
        Mode to use in case there is more than 1 shape in the STEP file
        
    Returns
    -------
    List of STL files creates, total number of shapes
    If there is only 1 file in the liste and more than 1 shape, it is a STL with
    multiple entities
        

    """
    def shape_to_stl(shape_, stl_file_, scale, ascii_mode_, factor_, use_min_dim_):
        r"""Write a single shape to an STL file
        
        Parameters
        ----------
        shape_
        stl_file_
        ascii_mode_
        factor_
        use_min_dim_

        """
        exporter = StlExporter(filename=stl_file_, ascii_mode=ascii_mode_)

        shape_ = scale_uniform(shape_, gp_Pnt(0, 0, 0), scale, False)

        # Must mesh ! Otherwise the exporter does not write anything!
        mesh(shape_, factor=factor_, use_min_dim=use_min_dim_)

        exporter.set_shape(shape_)
        exporter.write_file()

    # Read STEP
    shapes = StepImporter(filename=step_file_path).shapes

    if len(shapes) == 0:
        msg = "The STEP file contains no shape"
        logger.error(msg)
        raise ValueError(msg)

    elif len(shapes) == 1:  # 99.9 % of practical cases
        shape_to_stl(shapes[0], stl_file_path, scale, ascii_mode, factor, use_min_dim)
        assert isfile(stl_file_path)
        return [stl_file_path], 1

    elif len(shapes) > 1:
        if multi_shape_mode == ONE_SHAPE_PER_FILE:
            f, e = os.path.splitext(stl_file_path)
            partial_files = list()
            for i, shape in enumerate(shapes):
                filename = f+"_"+str(i)+e
                shape_to_stl(shape,
                             filename,
                             scale,
                             ascii_mode,
                             factor,
                             use_min_dim)
                partial_files.append(filename)
            return partial_files, len(shapes)

        elif multi_shape_mode == ALL_SHAPES_IN_ONE_FILE:
            partial_files = list
            for i, shape in enumerate(shapes):
                filename = f + "_" + str(i) + e
                shape_to_stl(shape,
                             filename,
                             scale,
                             ascii_mode,
                             factor,
                             use_min_dim)
                partial_files.append(filename)
            with open(stl_file_path, "w") as stl_file:
                for partial_file in partial_files:
                    with open(partial_file) as pf:
                        content = pf.readlines()
                        stl_file.writelines(content)
            for partial_file in partial_files:
                os.remove(partial_file)
            return [stl_file_path], len(shapes)

        else:
            msg = "Unknown mode for multi shape STEP conversion to STL"
            raise ValueError(msg)
