import wx
from wx.richtext import RichTextCtrl
from enum import Enum
from .prompter_line_bitmap_buffered import Prompter
from .prompter_monitor import PrompterMonitor, EVT_SPEED_CHANGED


class Controller(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.prompter = None
        self.script = ""

        self.layout = ControllerLayout.SIDE_BY_SIDE
        self.init_ui()
        self.Show()

    def secondary_display(self):
        for index in range(wx.Display.GetCount()):
            display = wx.Display(index)
            if not display.IsPrimary():
                return display

        return None

    def create_prompter(self):
        display = self.secondary_display()
        self.prompter = Prompter(None, 'Prompter', display)
        self.prompter.monitor_update_callback = self.monitor.update
        self.update_prompter_script()

    def init_ui(self):
        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()

        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)

        self.rtc = RichTextCtrl(self)
        self.rtc.Bind(wx.EVT_KEY_UP, self.key_up)
        self.load_script(self.script)
        self.monitor = PrompterMonitor(self)
        self.monitor.Bind(wx.EVT_LEFT_DCLICK, self.monitor_fullscreen_toggle)
        self.monitor.Bind(EVT_SPEED_CHANGED, self.change_speed)

        self.SetAutoLayout(True)

        if self.layout == ControllerLayout.MONITOR_FULLSCREEN:
            self.layout_monitor_fullscreen()
        else:
            self.layout_side_by_side()

    def change_speed(self, event):
        if event.change == 'increase':
            self.prompter.speed += 1
        elif event.change == 'decrease':
            self.prompter.speed += -1
        elif event.change == 'stop':
            self.prompter.speed = 0

    def layout_side_by_side(self):
        self.layout = ControllerLayout.SIDE_BY_SIDE
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.rtc, 1, wx.EXPAND)
        sizer.Add(self.monitor, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def layout_monitor_fullscreen(self):
        self.layout = ControllerLayout.MONITOR_FULLSCREEN
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(self.monitor, 1, wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def monitor_fullscreen_toggle(self, event):
        if self.layout == ControllerLayout.MONITOR_FULLSCREEN:
            self.layout_side_by_side()
        else:
            self.layout_monitor_fullscreen()

    def key_up(self, event):
        self.script = self.rtc.GetValue()
        self.update_prompter_script()

    def load_script(self, script):
        self.rtc.Clear()
        self.rtc.WriteText(script)
        self.update_prompter_script()

    def load_script_from_file(self, filename):
        with open(filename) as script_file:
            self.script = script_file.read()
            self.load_script(self.script)

    def update_prompter_script(self):
        if self.prompter:
            self.prompter.script = self.script


class ControllerLayout(Enum):
    SIDE_BY_SIDE = 1
    MONITOR_FULLSCREEN = 2
