import wx
import wx.lib
from wx.lib.colourchooser.canvas import BitmapBuffer
from .util import wordwrap


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(320, 240))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()
        self._script = ""

        self.frame_rate = 50

        self.speed = 50 / self.frame_rate
        self.y_scroll = 0

        self.bitmap = wx.Bitmap(800, 800 * 9 / 16)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
        self.timer.Start(1000 / self.frame_rate)
        self.prompter = None

        self.text_color = wx.Colour(255, 255, 255)
        self.background_color = wx.Colour(0, 0, 0)
        self.background_brush = wx.Brush(self.background_color)

        self.font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD, False, 'Freesans 10 Pitch')

    def update_animation(self, event):
        self.y_scroll -= self.speed
        memDC = wx.MemoryDC()
        memDC.SelectObject(self.bitmap)
        memDC.SetBackground(self.background_brush)
        memDC.Clear()
        memDC.SetTextForeground(self.text_color)
        memDC.SetFont(self.font)
        text = wordwrap(self.script, self.bitmap.GetSize()[0], memDC)
        memDC.DrawText(text, 0, self.y_scroll)
        memDC.SelectObject(wx.NullBitmap)
        self.Refresh()

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, new_script):
        self._script = new_script
        self.Refresh()

    def paint(self, event):
        # dc = wx.BufferedPaintDC(self)
        # dc.SetBackground(self.background_brush)
        # dc.Clear()
        # dc.SetTextForeground(self.text_color)
        # dc.SetFont(self.font)
        # text = wordwrap(self.script, self.GetSize()[0], dc)
        # dc.DrawText(text, 0, self.y_scroll)

        dc = wx.ClientDC(self)
        size = dc.Size
        scaledImage = self.bitmap.ConvertToImage().Scale(*size)
        dc.DrawBitmap(wx.Bitmap(scaledImage), 0, 0)


    def get_bitmap(self):
        # dc = wx.ClientDC(self)
        # size = dc.Size
        # bmp = wx.Bitmap(size.width, size.height)
        # memDC = wx.MemoryDC()
        # memDC.SelectObject(self.bitmap)
        # memDC.Blit(0, 0, size.width, size.height, dc, 0, 0)
        # memDC.SelectObject(wx.NullBitmap)
        return self.bitmap
