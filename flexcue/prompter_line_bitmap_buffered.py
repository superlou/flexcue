import wx
import wx.lib
from .util import wordwrap, execution_time
from .script_line import ScriptLine


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(320, 240))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()
        self._script = ""
        self.script_lines = []

        self.speed = 5
        self.y_scroll = 0

        self.buffer = wx.Bitmap(*self.GetSize())

        self.Bind(wx.EVT_SIZE, self.resize)

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update_animation, self.timer)
        self.timer.Start(20)
        self.prompter = None

        self.text_color = wx.Colour(255, 255, 255)
        self.background_color = wx.Colour(0, 0, 0)
        self.background_brush = wx.Brush(self.background_color)

        self.font = wx.Font(50, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL,
            wx.FONTWEIGHT_BOLD, False, 'Freesans 10 Pitch')

        self.line_bitmaps = []

    def resize(self, event):
        self.make_line_bitmaps()
        self.buffer = wx.Bitmap(*self.GetSize())
        self.Refresh()

    def update_animation(self, event):
        self.y_scroll -= self.speed
        self.Refresh()

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
        self.Refresh()

    def paint(self, event):
        memDC = wx.MemoryDC()
        memDC.SelectObject(self.buffer)

        lb = self.script_line[0]

        draw_y = self.y_scroll
        script_line_index = 0

        while (draw_y < memDC.GetSize()[1]):
            script_line = self.script_line[script_line_index]
            memDC.DrawBitmap(script_line.bitmap, 0, draw_y)
            draw_y += script_line.height
            script_line_index += 1

        dc = wx.ClientDC(self)
        size = dc.Size
        dc.Blit(0, 0, size.width, size.height, memDC, 0, 0)
        memDC.SelectObject(wx.NullBitmap)

    def get_bitmap(self):
        return self.buffer
