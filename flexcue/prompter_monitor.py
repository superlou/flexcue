import wx
import wx.lib.newevent
from .util import scale_bitmap, execution_time


class PrompterMonitor(wx.Panel):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, -1, **kwargs)
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_MOUSEWHEEL, self.on_mousewheel)
        self.Bind(wx.EVT_KEY_DOWN, self.on_key_down)
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

    def on_key_down(self, event):
        if event.GetKeyCode() == 32:
            # Stop on spacebar
            event = SpeedChangedEvent(change='stop')
            wx.PostEvent(self, event)

    def on_mousewheel(self, event):
        rotation = event.GetWheelRotation()

        if rotation > 0:
            direction = 'decrease'
        else:
            direction = 'increase'

        event = SpeedChangedEvent(change=direction)
        wx.PostEvent(self, event)


SpeedChangedEvent, EVT_SPEED_CHANGED = wx.lib.newevent.NewEvent()
