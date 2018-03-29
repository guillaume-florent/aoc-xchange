#!/usr/bin/python
# coding: utf-8

r"""CAD file opening and saving in a wx ui"""

import wx
import aocxchange.extensions
import aocxchange.utils
import aocxchange.step
import aocxchange.iges
import aocxchange.stl
import aocxchange.brep


class OpenCadDialog(wx.FileDialog):
    r"""Pre-configured file dialog to open a CAD file

    The dialog is implemented as a context manager

    """
    def __init__(self, parent=None, title="Choose Cad file to open", default_dir="", default_file=""):
        super(OpenCadDialog, self).__init__(parent, title, default_dir, default_file,
                                            style=wx.FD_OPEN | wx.FD_FILE_MUST_EXIST,
                                            wildcard=aocxchange.extensions.cad_files_wildcard)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Destroy()


class SaveAsCadDialog(wx.FileDialog):
    r"""Pre-configured file dialog to save a CAD file as ...

    The dialog is implemented as a context manager

    """
    def __init__(self, parent=None, title="Save CAD file", default_dir="", default_file=""):
        super(SaveAsCadDialog, self).__init__(parent, title, default_dir, default_file,
                                              style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT,
                                              wildcard=aocxchange.extensions.cad_files_wildcard)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Destroy()


class ComboBoxDialog(wx.Dialog):
    r"""A dialog with a configurable title, message and combo box

    Parameters
    ----------
    parent
    title : str
    message : str
    choices : list[str]

    """
    def __init__(self, parent, title, message, choices):
        super(ComboBoxDialog, self).__init__(parent, wx.ID_ANY, title)

        self.selection = wx.ComboBox(self, choices=choices, value=choices[0], style=wx.CB_READONLY)
        ok_button = wx.Button(self, wx.ID_OK)
        main_sizer = wx.BoxSizer(wx.VERTICAL)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(wx.StaticText(self, wx.ID_ANY, message), 0, wx.TOP | wx.CENTER, 5)
        sizer.Add(self.selection, 0, wx.ALL | wx.CENTER, 5)
        sizer.Add(ok_button, 0, wx.ALL | wx.CENTER, 30)
        main_sizer.AddSizer(sizer, 0, wx.ALL | wx.CENTER, 50)
        self.SetSizer(main_sizer)
        self.Fit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.Destroy()


class IgesFormatDialog(ComboBoxDialog):
    r"""Specialized ComboBoxDialog for IGES formats"""
    def __init__(self):
        super(IgesFormatDialog, self).__init__(parent=None, title="IGES format", message="Choose IGES format",
                                               choices=["5.1", "5.3"])


class StepSchemaDialog(ComboBoxDialog):
    r"""Specialized ComboBoxDialog for STEP schemas"""
    def __init__(self):
        super(StepSchemaDialog, self).__init__(parent=None, title="STEP schema", message="Choose STEP schema",
                                               choices=["AP203", "AP214CD"])


class StlFormatDialog(ComboBoxDialog):
    r"""Specialized ComboBoxDialog for STL formats"""
    def __init__(self):
        super(StlFormatDialog, self).__init__(parent=None, title="STL format", message="Choose STL format",
                                              choices=["Binary", "ASCII"])


def handle_cad_file_open():
    r"""Handle the logic of cad file opening

    Returns
    -------
    path : str
    type_ : str
        iges, step, stl brep
    shapes: list[OCC.TopoDS.TopoDS_Shape]

    """
    with OpenCadDialog() as open_cad_file_dialog:
        if open_cad_file_dialog.ShowModal() == wx.ID_OK:

            # cast the path from the FileDialog to st to avoid
            # TypeError: in method 'XSControl_Reader_ReadFile',
            #                                  argument 2 of type 'char const *'
            path = str(open_cad_file_dialog.GetPath())
            extension = aocxchange.utils.extract_file_extension(path)

            if extension.lower() in aocxchange.extensions.step_extensions:
                type_ = "step"
                shapes = aocxchange.step.StepImporter(path).shapes
            elif extension.lower() in aocxchange.extensions.iges_extensions:
                type_ = "iges"
                shapes = aocxchange.iges.IgesImporter(path).shapes
            elif extension.lower() in aocxchange.extensions.stl_extensions:
                type_ = "stl"
                shapes = list()
                shapes.append(aocxchange.stl.StlImporter(path).shape)
            elif extension.lower() in aocxchange.extensions.brep_extensions:
                type_ = "brep"
                shapes = list()
                shapes.append(aocxchange.brep.BrepImporter(path).shape)
            else:
                raise ValueError("File extension indicates a file type that "
                                 "is not supported")
            # return filepath + type (iges ...) + list of shapes
            return path, type_, shapes
        else:  # cancel button
            return None, None, None


def handle_cad_file_save_as(shapes):
    r"""Handle the logic of cad file save as

    Parameters
    ----------
    shapes : iterable of OCC.TopoDS.TopoDS_Shape

    Returns
    -------
    tuple
        path, type (step, iges ...), extra_info(format, schema or None)

    """

    # assert len(shapes) > 0
    if len(shapes) == 0:
        msg = "shapes list does not contain any shape"
        raise ValueError(msg)

    with SaveAsCadDialog() as save_as_cad_dialog:
        if save_as_cad_dialog.ShowModal() == wx.ID_OK:
            path = str(save_as_cad_dialog.GetPath())
            extension = aocxchange.utils.extract_file_extension(path)

            if extension.lower() in aocxchange.extensions.step_extensions:
                type_ = "step"
                with StepSchemaDialog() as step_schema_dialog:
                    if step_schema_dialog.ShowModal() == wx.ID_OK:
                        extra_info = schema = str(step_schema_dialog.selection.GetValue())
                        exporter = aocxchange.step.StepExporter(path,
                                                                schema=schema)
                        for shape in shapes:
                            exporter.add_shape(shape)
                        exporter.write_file()
            elif extension.lower() in aocxchange.extensions.iges_extensions:
                type_ = "iges"
                with IgesFormatDialog() as iges_format_dialog:
                    if iges_format_dialog.ShowModal() == wx.ID_OK:
                        extra_info = format_ = str(iges_format_dialog.selection.GetValue())
                        exporter = aocxchange.iges.IgesExporter(path,
                                                                format_=format_)
                        for shape in shapes:
                            exporter.add_shape(shape)
                        exporter.write_file()
            elif extension.lower() in aocxchange.extensions.stl_extensions:
                type_ = "stl"
                with StlFormatDialog() as stl_format_dialog:
                    if stl_format_dialog.ShowModal() == wx.ID_OK:
                        extra_info = ascii_mode = True if stl_format_dialog.selection.GetValue() == "ASCII" else False
                        exporter = aocxchange.stl.StlExporter(path,
                                                              ascii_mode=ascii_mode)
                        # TODO : warning message if len(shapes) > 1
                        exporter.set_shape(shapes[0])
                        exporter.write_file()
            elif extension.lower() in aocxchange.extensions.brep_extensions:
                type_ = "brep"
                extra_info = None
                exporter = aocxchange.brep.BrepExporter(path)
                # TODO : warning message if len(shapes) > 1
                exporter.set_shape(shapes[0])
                exporter.write_file()

            else:
                msg = "File extension indicates a file type " \
                      "that is not supported"
                raise ValueError(msg)

            return path, type_, extra_info
        else:
            return None, None, None
    # return filepath + type + format/schema


if __name__ == "__main__":

    class Example(wx.Frame):
        r"""Example wx frame"""
        def __init__(self, *args, **kw):
            super(Example, self).__init__(*args, **kw)
            self.init_ui()

        def init_ui(self):
            r"""Setup ui components"""
            ID_OPEN_CAD = wx.NewId()
            ID_SAVE_CAD = wx.NewId()

            tb = self.CreateToolBar()
            tb.AddLabelTool(id=ID_OPEN_CAD,
                            label='',
                            bitmap=wx.Bitmap('../icons/open.png'))
            tb.AddLabelTool(id=ID_SAVE_CAD,
                            label='',
                            bitmap=wx.Bitmap('../icons/save-as.png'))
            tb.Realize()

            self.Bind(wx.EVT_TOOL, self.on_open_cad, id=ID_OPEN_CAD)
            self.Bind(wx.EVT_TOOL, self.on_save_as_cad, id=ID_SAVE_CAD)

            self.SetSize((200, 200))
            self.SetTitle('CAD file dialogs testing frame')
            self.Centre()
            self.Show(True)

        def on_open_cad(self, event):
            print(handle_cad_file_open())

        def on_save_as_cad(self, event):
            import aocutils.primitives
            box = aocutils.primitives.box(10, 10, 10)
            cylinder = aocutils.primitives.cylinder(10, 30)
            shapes = [box, cylinder]
            print(handle_cad_file_save_as(shapes))

    ex = wx.App()
    Example(None)
    ex.MainLoop()
