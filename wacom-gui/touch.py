#!/usr/bin/python

from PyQt4 import QtCore, QtGui
import sys, os, re

class touch(QtGui.QWidget):
    def __init__(self, tabletName, parent=None):
        QtGui.QWidget.__init__(self, parent)
        devices = os.popen("xsetwacom --list devices").readlines()
        self.tabletName = None
        for device in devices:
            attr = device.strip().split('\t')
            if attr[2] == 'type: TOUCH':
                self.tabletName = attr[0][:-6]
                self.enable = None
        self.initUI()

    def initUI(self):
        self.devices = []
        # check if it is even necessary
        if os.popen("xsetwacom --list devices | grep touch").readlines().__len__() == 0:
            return None
        # layout code
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setAlignment(QtCore.Qt.AlignLeft)
        self.buttons = QtGui.QCheckBox("Enable Touch")
        self.getEnableStatus()
        self.buttons.stateChanged.connect(self.buttonChange)
        # layout code
        self.mainLayout.addWidget(self.buttons)
        self.mainLayout.setAlignment(QtCore.Qt.AlignCenter)
        self.setLayout(self.mainLayout)

    def buttonChange(self):
        if self.tabletName:
            if self.buttons.isChecked():
                status = os.popen("xsetwacom --set \"" + self.tabletName + " touch\" touch on")
                self.enable = "xsetwacom --set \""+self.tabletName+" touch\" Touch on"
            else:
                status = os.popen("xsetwacom --set \"" + self.tabletName + " touch\" touch off")
                self.enable = "xsetwacom --set \"" + self.tabletName + " touch\" Touch off"

    def getEnableStatus(self):
        if self.tabletName:
            getCommand = os.popen("xsetwacom --get \"" + self.tabletName + " touch\" Touch").readlines()
            # check correct button for orientation
            if getCommand[0] == "on\n":
                self.enable = "xsetwacom --set \"" + self.tabletName + " touch\" Touch on"
                self.buttons.setChecked(1)
            else:
                self.enable = "xsetwacom --set \"" + self.tabletName + " touch\" Touch off"
                # self.buttons.(1)


    def getTouchEnable(self):
        if self.tabletName:
            return self.enable
        else:
            return ''


    def resetDefaults(self):
        if self.tabletName:
            self.enable = "xsetwacom --set \"" + self.tabletName + " touch\" Touch on"
            os.popen(self.enable)
            self.buttons.setChecked(True)
