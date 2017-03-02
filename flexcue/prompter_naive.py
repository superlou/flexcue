import wx
import wx.lib
from .util import wordwrap, execution_time


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(320, 240))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()
        self._script = ""

        self.speed = 5
        self.y_scroll = 0

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
        self.timer.Start(17)
        self.prompter = None

        self.text_color = wx.Colour(255, 255, 255)
        self.background_color = wx.Colour(0, 0, 0)
        self.background_brush = wx.Brush(self.background_color)

        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD, False, 'Freesans 10 Pitch')

    def update_animation(self, event):
        self.y_scroll -= self.speed
        self.Refresh()

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, new_script):
        self._script = new_script
        self.Refresh()

    def paint(self, event):
        dc = wx.ClientDC(self)
        dc.SetBackground(self.background_brush)
        dc.Clear()
        dc.SetTextForeground(self.text_color)
        dc.SetFont(self.font)
        text = wordwrap(self.script, self.GetSize()[0], dc)
        dc.DrawText(text, 0, self.y_scroll)

    def get_bitmap(self):
        dc = wx.ClientDC(self)
        size = dc.Size
        bmp = wx.Bitmap(size.width, size.height)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dc, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        return bmp
