# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        # init Widget

        self.button = {
            "learn": QtGui.QPushButton('Nauka indywidualna'),
            "auto": QtGui.QPushButton('Nauka automatyczna'),
            "base": QtGui.QPushButton(u'bazy słówek'),
            "sets": QtGui.QPushButton('Ustawienia'),
            "close": QtGui.QPushButton(u'Wyjście'),
            }
        
        self.logo = QtGui.QLabel(self)
        
        # setting Layout
        
        self.logo.resize(500, 250)
        self.logo.setPixmap(QtGui.QPixmap("image/logo_orange-black.jpg").scaled(self.logo.size(), QtCore.Qt.KeepAspectRatio))

        self.hbox = QtGui.QHBoxLayout()
        self.vbox = QtGui.QVBoxLayout()
        
        self.hbox_butt = QtGui.QHBoxLayout()
        self.vbox_butt = QtGui.QVBoxLayout()

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

    # setting widgets

    def plug_buttons(self):
        self.button['learn'].clicked.connect(self.pool)
        self.button['auto'].clicked.connect(self.auto)
        self.button['base'].clicked.connect(self.base)
        self.button['sets'].clicked.connect(self.sets)
        self.button['close'].clicked.connect(QtCore.QCoreApplication.instance().quit)

    # events
    def pool(self):
        from main import Main
        #window = Main.get().windows['PoolWindow']['id']
        self.hide()
        Main.get().switch_window('PoolWindow')

    def auto(self):
        from main import Main
        print('auto')

    def sets(self):
        from main import Main
        window = Main.get().windows['SettingWindow']['id']
        self.stacked_widget.setCurrentWidget(window)

    def base(self):
        from main import Main
        window = Main.get().windows['BaseWindow']['id']
        self.stacked_widget.setCurrentWidget(window)


