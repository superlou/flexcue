import wx


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(320, 240))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()
        self._script = ""
        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD, False, 'Freesans 10 Pitch')

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, new_script):
        self._script = new_script
        self.Refresh()

    def paint(self, event):
        dc = wx.ClientDC(self)
        dc.SetFont(self.font)
        dc.DrawText(self.script, 0, 0)

    def get_bitmap(self):
        dc = wx.ClientDC(self)
        size = dc.Size
        bmp = wx.Bitmap(size.width, size.height)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dc, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        return bmp
