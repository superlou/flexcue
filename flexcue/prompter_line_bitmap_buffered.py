import wx
import wx.lib
from .util import wordwrap, execution_time
from .script_line import ScriptLine
import time


class Prompter(wx.Frame):
    def __init__(self, parent, title, display=None):
        if display:
            x, y, width, height = display.GetGeometry()
            super().__init__(parent, title=title, size=(width, height),
                             pos=(x, y), style=wx.NO_BORDER)
        else:
            super().__init__(parent, title=title, size=(320, 240))

        self.Bind(wx.EVT_PAINT, self.paint)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.erase_background)
        self.Show()
        self._script = ""
        self.script_lines = []

        self.speed = 1
        self.y_scroll = 0

        self.buffer = wx.Bitmap(*self.GetSize())

        self.Bind(wx.EVT_SIZE, self.resize)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_buffer, self.timer)
        self.framerate = 60
        self.timer.Start(1000 / self.framerate)
        self.prompter = None

        self.text_color = wx.Colour(255, 255, 255)
        self.background_color = wx.Colour(0, 0, 0)
        self.background_brush = wx.Brush(self.background_color)

        self.font = wx.Font(100, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD, False, 'Freesans 10 Pitch')

        self.line_bitmaps = []
        self.monitor_update_callback = None

        self.prev_update_time = time.time()

    def resize(self, event):
        self.make_line_bitmaps()
        self.buffer = wx.Bitmap(*self.GetSize())
        self.Refresh()

    def erase_background(self, event):
        pass

    def update_buffer(self, event):
        memDC = wx.MemoryDC()
        memDC.SelectObject(self.buffer)

        # Calculate scroll right before we need it, allowing for timer jitter
        now = time.time()
        time_delta = now - self.prev_update_time
        self.prev_update_time = now
        self.y_scroll -= self.speed * (time_delta * self.framerate)

        draw_y = self.y_scroll
        script_line_index = 0

        while (draw_y < memDC.GetSize()[1]):
            script_line = self.script_line[script_line_index]
            memDC.DrawBitmap(script_line.bitmap, 0, draw_y)
            draw_y += script_line.height
            script_line_index += 1

        memDC.SelectObject(wx.NullBitmap)

        self.Refresh(eraseBackground=False)

        if self.monitor_update_callback:
            self.monitor_update_callback(self.buffer)

    def make_line_bitmaps(self):
        dc = wx.ClientDC(self)
        dc.SetFont(self.font)
        text = wordwrap(self._script, self.GetSize()[0], dc)
        self.script_lines = text.split('\n')

        min_y = 0

        self.script_line = []

        for line in self.script_lines:
            lb = ScriptLine(line, self.font, min_y, self.GetSize()[0])
            min_y += lb.height
            self.script_line.append(lb)

    @property
    def script(self):
        return self._script

    @script.setter
    def script(self, new_script):
        self._script = new_script
        self.make_line_bitmaps()
        self.Refresh(eraseBackground=False)

    def paint(self, event):
        dc = wx.ClientDC(self)
        dc.DrawBitmap(self.buffer, 0, 0)

    def get_bitmap(self):
        return self.buffer
