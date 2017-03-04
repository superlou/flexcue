import wx
from .util import scale_bitmap, execution_time


class PrompterMonitor(wx.Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, -1, **kwargs)
        self.Bind(wx.EVT_PAINT, self.paint)
        self.SetDoubleBuffered(True)    # Prevent flicker on Windows

        self.prompter = None

    def update(self, bitmap):
        dc = wx.ClientDC(self)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bitmap)
        dc.StretchBlit(0, 0, *self.GetSize(), memDC, 0, 0, *memDC.GetSize())
        memDC.SelectObject(wx.NullBitmap)

    def paint(self, event):
        if self.prompter:
            dc = wx.ClientDC(self)
            memDC = wx.MemoryDC()
            memDC.SelectObject(self.prompter.get_bitmap())
            dc.StretchBlit(0, 0, *self.GetSize(), memDC, 0, 0, *memDC.GetSize())
            memDC.SelectObject(wx.NullBitmap)
