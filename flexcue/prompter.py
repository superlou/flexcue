import wx


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 300))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()

    def paint(self, event):
        self.draw_line()

    def draw_line(self):
        dc = wx.ClientDC(self)
        dc.DrawLine(50, 60, 190, 60)

    def get_bitmap(self):
        dc = wx.ClientDC(self)
        size = dc.Size
        bmp = wx.Bitmap(size.width, size.height)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dc, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        return bmp
