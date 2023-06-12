import wx
import mp3_converter  # Stelle sicher, dass mp3_converter im gleichen Ordner wie dein GUI-Skript ist

class Mywin(wx.Frame):
    def __init__(self, parent, title):
        super(Mywin, self).__init__(parent, title = title, size = (600, 300))
        self.SetSizeHints(wx.Size(500, 300))  # Minimale Größe setzen

        self.InitUI()

    def InitUI(self):
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.input_dir_txt = wx.TextCtrl(panel)
        self.output_dir_txt = wx.TextCtrl(panel)

        input_dir_btn = wx.Button(panel, label = "Select Input Folder")
        output_dir_btn = wx.Button(panel, label = "Select Output Folder")

        convert_btn = wx.Button(panel, label = "Start Conversion")

        input_dir_btn.Bind(wx.EVT_BUTTON, self.OnInputDir)
        output_dir_btn.Bind(wx.EVT_BUTTON, self.OnOutputDir)
        convert_btn.Bind(wx.EVT_BUTTON, self.OnConvert)

        vbox.Add(wx.StaticText(panel, label = "Input Folder:"), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.input_dir_txt, 0, wx.EXPAND | wx.ALL, 5)  # Größe der Textfelder festlegen
        vbox.Add(input_dir_btn, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(wx.StaticText(panel, label = "Output Folder:"), 0, wx.EXPAND | wx.ALL, 5)
        vbox.Add(self.output_dir_txt, 0, wx.EXPAND | wx.ALL, 5)  # Größe der Textfelder festlegen
        vbox.Add(output_dir_btn, 1, wx.EXPAND | wx.ALL, 5)

        vbox.Add(convert_btn, 1, wx.EXPAND | wx.ALL, 5)

        panel.SetSizer(vbox)

    def OnInputDir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.input_dir_txt.SetValue(dlg.GetPath())
            print('Input directory selected: ' + dlg.GetPath())
        dlg.Destroy()

    def OnOutputDir(self, event):
        dlg = wx.DirDialog(self, "Choose a directory:")
        if dlg.ShowModal() == wx.ID_OK:
            self.output_dir_txt.SetValue(dlg.GetPath())
            print('Output directory selected: ' + dlg.GetPath())
        dlg.Destroy()

    def OnConvert(self, event):
        input_dir = self.input_dir_txt.GetValue()
        output_dir = self.output_dir_txt.GetValue()

        if not input_dir or not output_dir:
            dlg = wx.MessageDialog(self, "Please select both an input and output directory.", "Missing Directory", wx.OK | wx.ICON_ERROR)
            dlg.ShowModal()
            dlg.Destroy()
        else:
            print("Starting conversion...")
            mp3_converter.scan_folders(input_dir, output_dir)
            print("Conversion finished!")

app = wx.App()
frame = Mywin(None, "Folder selector")
frame.Show()
app.MainLoop()
