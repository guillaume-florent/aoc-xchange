# coding: utf-8

r"""Common checks to all exporters and importers"""

import os.path
import logging
import warnings

from OCC.Core.TopoDS import TopoDS_Shape

from aocxchange.exceptions import FileNotFoundException, \
    DirectoryNotFoundException, IncompatibleFileFormatException
from aocxchange.utils import extract_file_extension

logger = logging.getLogger(__name__)


def check_importer_filename(filename, allowed_extensions="*"):
    r"""Check the filename is ok for importing.

    Checks that:
    - the file exists
    - the file extension is one of the extensions in allowed extensions
      (case insensitive check)

    Parameters
    ----------
    filename : str
        Full / absolute path to the file
    allowed_extensions : list[str]
        List of allowed extensions

    Raises
    ------
    aocxchange.exceptions.FileNotFoundException
        if the file does not exist
    aocxchange.exceptions.IncompatibleFileFormatException
        if the extension is not in allowed extensions

    """
    # Check the file exists
    if not os.path.isfile(filename):
        msg = "Importer error : file %s not found." % filename
        logger.error(msg)
        raise FileNotFoundException(msg)
    else:
        logger.debug("File to import exists")

    # Check the extension
    if allowed_extensions != "*":
        _check_extension(filename, allowed_extensions)

    logger.info("Filename passed checks")


def check_exporter_filename(filename,
                            allowed_extensions="*",
                            create_directory=False):
    r"""Check the filename is ok for exporting

    Checks that:
    - the directory in the filename exists
    - the file extension is one of the extensions in allowed extensions
      (case insensitive check)

    Parameters
    ----------
    filename : str
        Full path to the file
    allowed_extensions : list[str] or "*" (optional)
        List of allowed extensions
        The default is "*" which implies no check on the extension
    create_directory : bool (optional)
        Should the directory be created if it does not exist
        The default is False (no attempt made to create an inexistent directory)

    Raises
    ------
    aocxchange.exceptions.DirectoryNotFoundException
        if the directory from the filename does not exist
    aocxchange.exceptions.IncompatibleFileFormatException
        if the extension is not in allowed extensions
    OSError
        if create directory is True and the inexistent directory
        cannot be created

    """
    # Check the output directory exists
    if not os.path.isdir(os.path.dirname(filename)):
        if create_directory is True:
            os.makedirs(os.path.split(filename)[0])  # may raise OSError
        else:
            msg = "Exporter error : Output directory does not exist"
            logger.error(msg)
            raise DirectoryNotFoundException(msg)
    else:
        logger.debug("Directory to export to exists")

    # check the extension
    if allowed_extensions != "*":
        _check_extension(filename, allowed_extensions)

    logger.info("Filename passed checks")


def _check_extension(filename, allowed_extensions):
    r"""Check that the extension extracted from filename
    is in allowed extensions"""
    if extract_file_extension(filename).lower() not in allowed_extensions:
        msg = "Accepted extensions are %s" % str(allowed_extensions)
        logger.error(msg)
        raise IncompatibleFileFormatException(msg)
    else:
        logger.debug("Extension is ok")


def check_overwrite(filename):
    r"""Determines if writing will overwrite the file denoted by filename

    Parameters
    ----------
    filename : str
        Full path to the file

    Returns
    -------
    bool
        True if would overwrite, False otherwise

    """
    if os.path.isfile(filename):
        msg = "Will be overwriting file: %s" % filename
        warnings.warn(msg)
        logger.warning(msg)
        return True
    else:
        return False


def check_shape(a_shape):
    r"""Check the shape before adding it to an exporter.

    Parameters
    ----------
    a_shape : TopoDS_Shape or subclass

    Returns
    -------
    bool
        True if all tests passed, raises an exception otherwise
    """
    if not isinstance(a_shape, TopoDS_Shape) and not issubclass(a_shape.__class__,
                                                                TopoDS_Shape):
        msg = "Expecting a TopoDS_Shape or subclass, " \
              "got a %s" % a_shape.__class__
        logger.error(msg)
        raise ValueError(msg)

    if a_shape.IsNull():
        msg = "IgesExporter Error: the shape is NULL"
        logger.error(msg)
        raise ValueError(msg)
