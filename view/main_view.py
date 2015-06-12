# -*- coding: utf-8 -*-
__author__ = 'mcmushroom'

import sys
from PyQt4 import QtGui, QtCore, Qt
from view.word_pool import *


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.button = {}

        self.button["learn"] = QtGui.QPushButton('Nauka indywidualna', self)
        self.button["auto"] = QtGui.QPushButton('Nauka automatyczna', self)
        self.button["base"] = QtGui.QPushButton(u'bazy słówek', self)
        self.button["sets"] = QtGui.QPushButton('Ustawienia', self)
        self.button["close"] = QtGui.QPushButton(u'Wyjście', self)

        self.initUI()

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        logo = QtGui.QLabel(self)
        logo.resize(500, 250)
        logo.setPixmap(QtGui.QPixmap("../image/logo_orange-black.jpg").scaled(logo.size(), QtCore.Qt.KeepAspectRatio))

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        hbox_butt = QtGui.QHBoxLayout()
        vbox_butt = QtGui.QVBoxLayout()

        vbox_butt.addWidget(self.button["learn"])
        vbox_butt.addWidget(self.button["auto"])
        vbox_butt.addWidget(self.button["base"])
        vbox_butt.addWidget(self.button["sets"])
        vbox_butt.addWidget(self.button["close"])

        hbox_butt.addStretch(1)
        hbox_butt.addLayout(vbox_butt)
        hbox_butt.addStretch(1)

        vbox.addStretch(1)
        vbox.addWidget(logo)
        vbox.addStretch(1)
        vbox.addLayout(hbox_butt)
        vbox.addStretch(1)

        hbox.addStretch(1)
        hbox.addLayout(vbox)
        hbox.addStretch(1)

        self.slot_conn()
        self.setLayout(hbox)

        self.show()

    #definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
            # print(">checkpoint: slots plugging for key: ", key, 'in class: ', self.__class__.__name__)


