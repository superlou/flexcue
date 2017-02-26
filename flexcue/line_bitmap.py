import wx


class LineBitmap(wx.Bitmap):
    def __init__(self, text, font, screen_width):
        self.text = text
        self.font = font
        self.height = self.determine_size()[1]
        self.width = screen_width

    def determine_size(self):
        dc = wx.DC()
        dc.SetFont(self.font)
        return dc.GetTextExtent(self.text)
