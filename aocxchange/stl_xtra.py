# coding: utf-8

r"""STL related functions and procedures, useful for OpenFOAM"""

import logging
from os.path import basename

logger = logging.getLogger(__name__)


def nb_regions(stl_filepath):
    r"""Number of regions in the STL file

    Parameters
    ----------
    stl_filepath : str
        Path to the STL file

    Returns
    -------
    int : Number of regions

    """
    counter = 0
    patch_names = []
    with open(stl_filepath) as sf:
        for line in sf:
            if "solid" in line and "endsolid" not in line:
                # print(line)
                counter += 1
                items = line.split()
                # assert len(items) == 2
                if len(items) != 2:
                    msg = "line expected to contain 2 items, found %i" % len(items)
                    logger.error(msg)
                    raise AssertionError(msg)
                # print(items[1])
                patch_names.append(items[1])

    return counter, patch_names


def merge_stls(stls_paths, target_stl_file):
    r"""Merge n STL files into a single STL file

    Parameters
    ----------
    stls_paths : list[str]
        List of paths to STL files to merge
    target_stl_file : str
        Path to the target STL file

    """
    with open(target_stl_file, "w") as tf:
        for stl_path in stls_paths:
            with open(stl_path) as sp:
                for line in sp:
                    tf.write(line)


# def stl_bounding_box(stl_filepath):
#     see aocutils.analyze.bounds.py


def scale_stl(stl_in, factor, stl_out):
    r"""Scale an STL file by a given factor

    The strategy of this function is to scale every string that can be
    converted to float that is found in the file.

    Parameters
    ----------
    stl_in : str
        Path to the input STL file
    factor : float
        The scaling factor
    stl_out : str
        The path to the output/scaled STL file

    """
    logger.info("Scaling %s by factor %f. New STL: %s" % (basename(stl_in),
                                                          factor,
                                                          basename(stl_out)))
    new_lines = []

    with open(stl_in) as stl_input:
        for line in stl_input:
            items = line.rstrip().split(' ')
            new_items = []
            for item in items:
                try:
                    # Will raise a ValueError if item cannot be converted
                    # to float
                    new_items.append(str(float(item) * factor))
                except ValueError:
                    new_items.append(item)
            new_lines.append(' '.join(new_items))

    with open(stl_out, 'w') as stl_output:
        stl_output.write('\n'.join(new_lines))
