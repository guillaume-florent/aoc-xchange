#!/usr/bin/python
# coding: utf-8

r"""Convert a STEP file to OBJ file"""

import logging
import shutil
import tempfile
import uuid

from os.path import join, abspath
from aocxchange.convert.step_to_stl import step_to_stl, ONE_SHAPE_PER_FILE

from aocxchange.pymesh import stl

logger = logging.getLogger(__name__)


def step_to_obj(step_file_path,
                obj_file_path,
                factor=4000.,
                use_min_dim=False,
                remove_intermediate_stl=True):
    r"""Convert a STEP file to a OBJ file
    
    This function uses an intermediate conversion from STEP to STL then from
    STL to OBJ
    
    Parameters
    ----------
    step_file_path
    obj_file_path
    factor : float
        Meshing factor, optional (default is 4000.)
        The higher, the finer the mesh and the bigger the resulting file
    use_min_dim : bool, optional (default is False)
        Use the minimum dimension of the shape as a base for meshing
        This is useful for shapes with a high aspect ratio
    remove_intermediate_stl : bool, optional (default is True)
        Should the intermediate STL(s) be removed

    """
    # Save as STL

    # Create a tmp dir with 700 (read+write) rights
    tmp_dir = tempfile.mkdtemp()

    # Create a temporary STL file with a random name in tmp dir
    stl_temp_file = abspath(join(tmp_dir, "%s.stl" % uuid.uuid4().hex))

    list_of_files, nb_shapes = step_to_stl(step_file_path,
                                           stl_temp_file,
                                           factor,
                                           use_min_dim,
                                           ascii_mode=True,
                                           multi_shape_mode=ONE_SHAPE_PER_FILE)

    for stl_f in list_of_files:
        # Open STL with pymesh
        mesh = stl.Stl(stl_f)

        # Save as OBJ
        mesh.save_obj(obj_file_path, update_normals=True)

    # Delete STL
    if remove_intermediate_stl is True:
        # remove(stl_f)
        shutil.rmtree(tmp_dir)
