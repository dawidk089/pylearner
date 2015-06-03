# -*- coding: utf-8 -*-
__author__ = 'mcmushroom'

import sys
from PyQt4 import QtGui, QtCore, Qt


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()

    def initUI(self):

        logo = QtGui.QLabel(self)
        logo.resize(500, 250)
        logo.setPixmap(QtGui.QPixmap("image/logo_orange-black.jpg").scaled(logo.size(), QtCore.Qt.KeepAspectRatio))

        self.button = {}

        self.button["learn"] = QtGui.QPushButton('Nauka indywidualna', self)
        self.button["auto"] = QtGui.QPushButton('Nauka automatyczna', self)
        self.button["base"] = QtGui.QPushButton(u'bazy słówek', self)
        self.button["sets"] = QtGui.QPushButton('Ustawienia', self)
        self.button["close"] = QtGui.QPushButton(u'Wyjście', self)

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

        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.setWindowIcon(QtGui.QIcon('image/app_ico.png'))
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def slot_conn(self):
        self.button["close"].clicked.connect(QtCore.QCoreApplication.instance().quit)
        self.button["learn"].clicked.connect(self.learn)
        print(">checkpoint 1")
        #self.impt_butt[1][1].clicked.connect(self.file_dialog)
        #self.add_butt[1][1].clicked.connect(self.add_word)

    def learn(self):
        print(">checkpoint 2")
        del self