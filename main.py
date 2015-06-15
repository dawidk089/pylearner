__author__ = 'mcmushroom'

from PyQt4 import QtCore, QtGui
from view.main_view import MainWindow
from view.word_pool import PoolWindow
from view.base_view import BaseWindow
from view.setting_view import Setting
from model.data_storage import DataStorage


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        #glowna baza slowek
        self.main_base_word = DataStorage("data/main_base")
        self.main_base_word.open()

        #tworzenie stosu widokow
        self.windows_c = QtGui.QStackedWidget()
        self.setCentralWidget(self.windows_c)
        self.windows = {}

        for i, val in enumerate([MainWindow()]):
            self.windows[val.__class__.__name__] = {'instance': val, 'id': i}

        print('length of windows list:', len(self.windows))#$

        for key in self.windows:
            self.windows_c.addWidget(self.windows[key]['instance'])

        self.setWindowIcon(QtGui.QIcon('image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

        #podpiecie przyciskow
        slots = {
            'learn': self.pool,
            'auto': self.auto,
            'base': self.base,
            'sets': self.sets,
            'close': QtCore.QCoreApplication.instance().quit,
            }

        main_window.slot_conn(slots)

    # definicje funkcji podpinanych do przyciskow
    def pool(self):
        pool_window = PoolWindow(self.stacked_widget, self.main_base_word)
        self.stacked_widget.addWidget(pool_window)
        self.stacked_widget.setCurrentWidget(pool_window)

    def auto(self):
        print('auto')

    def sets(self):
        settins_window = Setting(self.stacked_widget)
        self.stacked_widget.addWidget(settins_window)
        self.stacked_widget.setCurrentWidget(settins_window)
        print('sets')

    def base(self):
        base_window = BaseWindow(self.stacked_widget, self.main_base_word)
        self.stacked_widget.addWidget(base_window)
        self.stacked_widget.setCurrentWidget(base_window)

    #definicja wysrodkowania okna
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

if __name__ == '__main__':

    app = QtGui.QApplication([])
    window = Main()
    window.show()
    app.exec_()


