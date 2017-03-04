import wx
from .util import scale_bitmap, execution_time


class PrompterMonitor(wx.Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, -1, **kwargs)
        self.Bind(wx.EVT_PAINT, self.paint)
        self.SetDoubleBuffered(True)    # Prevent flicker on Windows

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(20)
        self.prompter = None

    def update(self, event):
        self.Refresh()

    def paint(self, event):
        if self.prompter:
            bitmap = self.prompter.get_bitmap()
            bitmap = scale_bitmap(bitmap, self.GetSize())
            dc = wx.BufferedPaintDC(self)
            dc.Clear()
            dc.DrawBitmap(bitmap, 0, 0)
