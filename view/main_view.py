# -*- coding: utf-8 -*-
from PyQt4 import QtCore
from PyQt4.QtGui import *


class MainWindow(QWidget):

    def __init__(self, main):
        super(MainWindow, self).__init__()
        self.main = main

        # deklaracja widget'ow
        self.button = {
            "learn": QPushButton('Nauka indywidualna'),
            "auto": QPushButton('Nauka automatyczna'),
            "base": QPushButton(u'Bazy słówek'),
            "sets": QPushButton('Ustawienia'),
            "close": QPushButton(u'Wyjście'),
            }

        self.logo = QLabel(self)

        # ustawianie widget'ow
        self.logo.resize(500, 250)
        self.logo.setPixmap(QPixmap("image/logo_orange-black.jpg").scaled(self.logo.size(), QtCore.Qt.KeepAspectRatio))
        self.button['auto'].hide()  # TODO dodac funkcjonalnosc automatycznego generowania slowek do nauki i powtarzania

        # ustawianie layout'ow
        self.hbox = QHBoxLayout()
        self.vbox = QVBoxLayout()

        self.hbox_butt = QHBoxLayout()
        self.vbox_butt = QVBoxLayout()

        self.vbox_butt.addWidget(self.button["learn"])
        self.vbox_butt.addWidget(self.button["auto"])
        self.vbox_butt.addWidget(self.button["base"])
        self.vbox_butt.addWidget(self.button["sets"])
        self.vbox_butt.addWidget(self.button["close"])

        self.hbox_butt.addStretch(1)
        self.hbox_butt.addLayout(self.vbox_butt)
        self.hbox_butt.addStretch(1)

        self.vbox.addStretch(1)
        self.vbox.addWidget(self.logo)
        self.vbox.addStretch(1)
        self.vbox.addLayout(self.hbox_butt)
        self.vbox.addStretch(1)

        self.hbox.addStretch(1)
        self.hbox.addLayout(self.vbox)
        self.hbox.addStretch(1)

        self.setLayout(self.hbox)

        # podlaczenie zdarzen
        self.button['learn'].clicked.connect(self.pool)
        self.button['auto'].clicked.connect(self.auto)
        self.button['base'].clicked.connect(self.base)
        self.button['sets'].clicked.connect(self.sets)
        self.button['close'].clicked.connect(QtCore.QCoreApplication.instance().quit)

    # definicja zdarzen
    def pool(self):
        self.main.switch_window('PoolWindow')

    def auto(self):
        print('auto')

    def sets(self):
        self.main.switch_window('SettingWindow')

    def base(self):
        self.main.switch_window('BaseWindow')


