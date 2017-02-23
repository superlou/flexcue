#!/usr/bin/python3
import wx
from flexcue.prompter import Prompter
from flexcue.editor import Editor


def main():
    app = wx.App()
    editor = Editor(None, title='Editor')
    prompter = Prompter(None, title='Prompter')
    editor.prompter = prompter
    app.MainLoop()


if __name__ == '__main__':
    main()
