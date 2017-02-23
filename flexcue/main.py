#!/usr/bin/python3
import wx
from wx.richtext import RichTextCtrl


def scale_bitmap(bitmap, size):
    width, height = size
    image = bitmap.ConvertToImage()
    image = image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
    result = wx.Bitmap(image)
    return result


class Editor(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 200))
        self.prompter = None
        self.init_ui()
        self.Show()

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

        self.monitor = wx.Panel(self, -1, size=(100, 100))
        self.monitor.Bind(wx.EVT_PAINT, self.paint_panel)
        self.monitor.SetDoubleBuffered(True)    # Prevent flicker on Windows

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.update, self.timer)
        self.timer.Start(20)

        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(self.text_ctrl)
        hbox.Add(self.monitor)
        self.SetAutoLayout(True)
        self.SetSizer(hbox)

    def update(self, event):
        self.monitor.Refresh()

    def paint_panel(self, event):
        if self.prompter:
            bitmap = self.prompter.get_bitmap()
            bitmap = scale_bitmap(bitmap, self.monitor.GetSize())
            dc = wx.BufferedPaintDC(self.monitor)
            dc.Clear()
            dc.DrawBitmap(bitmap, 0, 0)


class Prompter(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300, 300))
        self.Bind(wx.EVT_PAINT, self.paint)
        self.Show()

    def paint(self, event):
        self.draw_line()

    def draw_line(self):
        dc = wx.ClientDC(self)
        dc.DrawLine(50, 60, 190, 60)

    def get_bitmap(self):
        dc = wx.ClientDC(self)
        size = dc.Size
        bmp = wx.Bitmap(size.width, size.height)
        memDC = wx.MemoryDC()
        memDC.SelectObject(bmp)
        memDC.Blit(0, 0, size.width, size.height, dc, 0, 0)
        memDC.SelectObject(wx.NullBitmap)
        return bmp


def main():
    app = wx.App()
    editor = Editor(None, title='Editor')
    prompter = Prompter(None, title='Prompter')
    editor.prompter = prompter
    app.MainLoop()


if __name__ == '__main__':
    main()
