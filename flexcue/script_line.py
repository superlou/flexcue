import wx


class ScriptLine():
    def __init__(self, text, font, min_y, screen_width):
        self.text = text
        self.font = font
        self.height = self.determine_size()[1]
        self.width = screen_width
        self.min_y = min_y
        self.max_y = min_y + self.height

        self.bitmap = wx.Bitmap(self.width, self.height)

        self.text_color = wx.Colour(255, 255, 255)
        self.background_color = wx.Colour(0, 0, 0)
        self.background_brush = wx.Brush(self.background_color)

        self.paint()

    def determine_size(self):
        dc = wx.MemoryDC()
        dc.SetFont(self.font)
        if self.text == '':
            self.text = ' '
        return dc.GetTextExtent(self.text)

    def paint(self):
        if self.height == 0:
            return

        dc = wx.MemoryDC()
        dc.SelectObject(self.bitmap)
        dc.SetBackground(self.background_brush)
        dc.Clear()
        dc.SetTextForeground(self.text_color)
        dc.SetFont(self.font)
        dc.DrawText(self.text, 0, 0)
        dc.SelectObject(wx.NullBitmap)
