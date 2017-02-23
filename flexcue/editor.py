import wx
from wx.richtext import RichTextCtrl
from .prompter import Prompter
from .prompter_monitor import PrompterMonitor


class Editor(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 200))
        self.prompter = None
        self.init_ui()
        self.Show()

    def create_prompter(self):
        self.prompter = Prompter(None, title='Prompter')
        self.monitor.prompter = self.prompter

    def init_ui(self):
        menubar = wx.MenuBar()
        filem = wx.Menu()
        editm = wx.Menu()
        helpm = wx.Menu()

        menubar.Append(filem, '&File')
        menubar.Append(editm, '&Edit')
        menubar.Append(helpm, '&Help')
        self.SetMenuBar(menubar)

        self.text_ctrl = RichTextCtrl(self, size=(250, 100))
        self.monitor = PrompterMonitor(self, size=(100, 100))

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.text_ctrl)
        hbox.Add(self.monitor)
        self.SetAutoLayout(True)
        self.SetSizer(hbox)
