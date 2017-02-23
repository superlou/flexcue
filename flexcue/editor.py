import wx
from wx.richtext import RichTextCtrl
from .prompter import Prompter
from .prompter_monitor import PrompterMonitor


class Editor(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)
        self.prompter = None
        self.script = """[SHAMAN]
You’re lucky to be alive. Many
strong men have fallen to the
gatekeepers.

[SHAMAN]
Here, take a sip."""

        self.init_ui()
        self.Show()

    def create_prompter(self):
        self.prompter = Prompter(None, title='Prompter')
        self.monitor.prompter = self.prompter
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
        self.load_script(self.rtc, self.script)
        self.monitor = PrompterMonitor(self, size=(320, 240))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.rtc)
        hbox.Add(self.monitor)
        self.SetAutoLayout(True)
        self.SetSizer(hbox)

    def key_up(self, event):
        self.script = self.rtc.GetValue()
        self.update_prompter_script()

    def load_script(self, rtc, script):
        rtc.WriteText(script)

    def update_prompter_script(self):
        if self.prompter:
            self.prompter.script = self.script
