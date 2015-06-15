# -*- coding: utf-8 -*-
__author__ = 'mcmushroom'

import sys
#from view.word_pool import *
from view.view_template import View
from PyQt4 import QtCore, QtGui


class MainWindow(View):

    def __init__(self, main):
        super().__init__()

        self.main = main

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

    # podpiecie przyciskow
        slots = {
            'learn': self.pool,
            'auto': self.auto,
            'base': self.base,
            'sets': self.sets,
            'close': QtCore.QCoreApplication.instance().quit,
            }

        self.slot_conn(slots)

    # definicje funkcji podpinanych do przyciskow
    def pool(self):
        print('click on individual learn button')
        #TODO PoolWindow potrzebuje main_base_word
        self.main.stacked_widget.addWidget(self.main.windows['word_pool'])
        self.main.stacked_widget.setCurrentWidget(self.main.windows['word_pool'])

    def auto(self):
        print('click on auto learn button')

    def sets(self):
        print('click on setting button')
        self.main.stacked_widget.addWidget(self.main.windows['settings'])
        self.main.stacked_widget.setCurrentWidget(self.main.windows['settings'])

    def base(self):
        print('click on main base button')
        self.main.stacked_widget.addWidget(self.main.windows['base'])
        self.main.stacked_widget.setCurrentWidget(self.main.windows['base'])


