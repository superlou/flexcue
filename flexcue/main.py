#!/usr/bin/python3
import wx
from flexcue.editor import Editor


def main():
    app = wx.App()
    editor = Editor(None, title='Editor')
    editor.create_prompter()
    editor.load_script_from_file('example.txt')
    app.MainLoop()


if __name__ == '__main__':
    main()
