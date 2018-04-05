# coding: utf-8

r"""Exceptions for aocxchange"""


class AocXChangeException(Exception):
    r"""Generic Aoc Data Exchange Exception

    Inherit this exception to define more specific exceptions

    """
    pass


class BRepBuildingException(AocXChangeException):
    r"""Something went wrong while building a BRep"""
    pass


# IO Specific / All file types generic


class FileNotFoundException(AocXChangeException):
    r"""The file could not be found"""
    pass


class DirectoryNotFoundException(AocXChangeException):
    r"""The directory could not be found"""
    pass


class IncompatibleFileFormatException(AocXChangeException):
    r"""The file format is not what is expected"""
    pass


class FileReadException(AocXChangeException):
    r"""Something went wrong while reading a file"""
    pass


class FileWriteException(AocXChangeException):
    r"""Something went wrong while writing a file"""
    pass


# IGES Specific


class IgesFileReadException(FileReadException):
    r"""Something wrent wrong while reading an IGES file"""
    pass


class IgesUnknownFormatException(AocXChangeException):
    r"""The IGES format s not 5.1 or 5.3"""
    pass


class IgesFileWriteException(FileWriteException):
    r"""An error occurred while writing a IGES file"""
    pass


# STEP Specific


class StepFileReadException(FileReadException):
    r"""Something went wrong while reading a STEP file"""
    pass


class StepUnknownSchemaException(AocXChangeException):
    r"""The STEP schema is not AP203 or AP214CD"""
    pass


class StepFileWriteException(FileWriteException):
    r"""An error occurred while writing a STEP file"""
    pass


class StepShapeTransferException(FileWriteException):
    r"""A shape could not be transfered to the STEP writer"""
    pass
