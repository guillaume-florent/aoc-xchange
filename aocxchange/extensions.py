# coding: utf-8

r"""CAD file acceptable extensions"""

iges_extensions = ["iges", "igs"]
step_extensions = ["step", "stp"]
stl_extensions = ["stl"]
brep_extensions = ["brep", "brp"]
dat_extensions = ["dat"]

iges_wildcard = "IGES (*.iges,*.igs)|*.iges;*.igs"
step_wildcard = "STEP (*.step,*.stp)|*.step;*.stp"
stl_wildcard = "STL (*.stl)|*.stl"
brep_wildcard = "BREP (*.brep)|*.brep"
all_files_wildcard = "All files (*.*)|*.*"

cad_files_wildcard = "|".join([step_wildcard,
                               iges_wildcard,
                               stl_wildcard,
                               brep_wildcard])
