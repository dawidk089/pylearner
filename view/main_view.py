from PyQt4 import QtCore, QtGui


class MainWindow(QtGui.QWidget):

    def __init__(self):
        super().__init__()
        self.init_widget()

    def init_widget(self):
        button = {
            "learn": QtGui.QPushButton('Nauka indywidualna'),
            "auto": QtGui.QPushButton('Nauka automatyczna'),
            "base": QtGui.QPushButton('bazy słówek'),
            "sets": QtGui.QPushButton('Ustawienia'),
            "close": QtGui.QPushButton('Wyjście'),
        }

        #inicjalizacja widget'ow i layout'u

        logo = QtGui.QLabel()
        logo.resize(500, 250)
        logo.setPixmap(QtGui.QPixmap("image/logo_orange-black.jpg").scaled(logo.size(), QtCore.Qt.KeepAspectRatio))

        hbox = QtGui.QHBoxLayout()
        vbox = QtGui.QVBoxLayout()
        hbox_butt = QtGui.QHBoxLayout()
        vbox_butt = QtGui.QVBoxLayout()

        vbox_butt.addWidget(button["learn"])
        vbox_butt.addWidget(button["auto"])
        vbox_butt.addWidget(button["base"])
        vbox_butt.addWidget(button["sets"])
        vbox_butt.addWidget(button["close"])

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

        self.setLayout(hbox)
        #self.show()



    """
    #self.slot_conn()
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
    """

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = MainWindow()
    window.show()
    app.exec_()