#!/usr/bin/python3
import wx
from flexcue.controller import Controller


def main():
    app = wx.App()
    controller = Controller(None, title='Flexcue')
    controller.create_prompter()
    controller.load_script_from_file('example.txt')
    app.MainLoop()


if __name__ == '__main__':
    main()
