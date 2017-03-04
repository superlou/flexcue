import wx
from wx.richtext import RichTextCtrl
from .prompter_line_bitmap_buffered import Prompter
from .prompter_monitor import PrompterMonitor


class Controller(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.prompter = None
        self.script = ""

        self.init_ui()
        self.Show()

    def create_prompter(self):
        self.prompter = Prompter(None, title='Prompter')
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

        self.rtc = RichTextCtrl(self, size=(250, 240))
        self.rtc.Bind(wx.EVT_KEY_UP, self.key_up)
        self.load_script(self.script)
        self.monitor = PrompterMonitor(self, size=(320, 240))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.rtc)
        hbox.Add(self.monitor)
        self.SetAutoLayout(True)
        self.SetSizer(hbox)

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
