import threading

import wx
import mp3_converter  # Stellen Sie sicher, dass mp3_converter im gleichen Verzeichnis wie Ihr GUI-Skript ist
import metadata_converter
import cover_importer
import cover_extractor


class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title=title, size=(600, 300))
        self.SetSizeHints(wx.Size(500, 300))  # Set minimum size
        self.InitUI()
        self.running = False
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        self.thread = threading.Thread(target=lambda: None)

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        input_dir_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Input Folder")
        self.input_dir_lbl = wx.StaticText(panel, label="")
        input_dir_box.Add(self.input_dir_lbl, 0, wx.EXPAND | wx.ALL, 5)

        output_dir_box = wx.StaticBoxSizer(wx.VERTICAL, panel, "Output Folder")
        self.output_dir_lbl = wx.StaticText(panel, label="")
        output_dir_box.Add(self.output_dir_lbl, 0, wx.EXPAND | wx.ALL, 5)

        input_dir_btn = wx.Button(panel, label="Select Input Folder")
        output_dir_btn = wx.Button(panel, label="Select Output Folder")

        self.convert_btn = wx.Button(panel, label="Start Conversion")
        self.convert_btn.SetBackgroundColour(wx.RED)

        # Erstellen Sie die Fortschrittsanzeige
        self.progress = wx.Gauge(panel, range=100)

        input_dir_btn.Bind(wx.EVT_BUTTON, self.OnInputDir)
        output_dir_btn.Bind(wx.EVT_BUTTON, self.OnOutputDir)
        self.convert_btn.Bind(wx.EVT_BUTTON, self.OnConvert)

        vbox.Add(input_dir_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(input_dir_btn, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(output_dir_box, 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(output_dir_btn, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(self.convert_btn, 1, wx.EXPAND | wx.ALL, 5)

        # Fügen Sie die Fortschrittsanzeige hinzu
        vbox.Add(self.progress, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)

    def check_dirs(self):
        input_dir = self.input_dir_lbl.GetLabel()
        output_dir = self.output_dir_lbl.GetLabel()

        if input_dir and output_dir:
            self.convert_btn.SetBackgroundColour(wx.GREEN)
        else:
            self.convert_btn.SetBackgroundColour(wx.RED)

    def OnInputDir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.input_dir_lbl.SetLabel(dlg.GetPath())
            print('Input directory selected: ' + dlg.GetPath())
            self.check_dirs()
        dlg.Destroy()

    def OnOutputDir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_lbl.SetLabel(dlg.GetPath())
            print('Output directory selected: ' + dlg.GetPath())
            self.check_dirs()
        dlg.Destroy()

    def OnConvert(self, event):
        self.thread = threading.Thread(target=self.start_conversion, args=(event,))
        self.thread.start()

    def start_conversion(self, event):
        input_dir = self.input_dir_lbl.GetLabel()
        output_dir = self.output_dir_lbl.GetLabel()

        if not input_dir or not output_dir:
            dlg = wx.MessageDialog(self, "Please select both an input and output directory.", "Missing Directory",
                                   wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            print("Starting conversion...")
            wx.CallAfter(self.convert_btn.Disable)
            wx.CallAfter(self.convert_btn.SetBackgroundColour, wx.RED)
            wx.CallAfter(self.progress.SetValue, 0)
            self.running = True
            for progress in mp3_converter.scan_folders(input_dir, output_dir):
                if not self.running:  # Check the flag here
                    break
                wx.CallAfter(self.progress.SetValue, round(progress))

            if self.running:
                metadata_converter.copy_metadata_in_folder(input_dir, output_dir)
                cover_extractor.extract_cover(input_dir, output_dir)
                cover_importer.import_cover(output_dir, output_dir)
                cover_importer.delete_png_files(output_dir)
                print("Conversion finished!")
                wx.CallAfter(self.convert_btn.Enable)
                self.check_dirs()

    def OnClose(self, event):
        self.running = False
        if self.thread.is_alive():  # Check if thread has been started
            self.thread.join()  # Wait for the conversion thread to finish
        event.Skip()  # Continue the close event


app = wx.App()
frame = Mywin(None, "MP3 Converter")
frame.Show()
app.MainLoop()
