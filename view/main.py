__author__ = 'mcmushroom'

from PyQt4 import QtCore, QtGui
from view.main_view import MainWindow
from view.word_pool import PoolWindow
from view.base_view import BaseWindow
from model.data_storage import DataStorage


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        #glowna baza slowek
        self.main_base_word = DataStorage("../data/main_base")
        self.main_base_word.open()
        print('main base word -- main: ', self.main_base_word.get())

        #tworzenie stosu widokow
        self.stacked_widget = QtGui.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        #zaladowanie glownego okna
        main_window = MainWindow()
        self.setWindowIcon(QtGui.QIcon('../image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()
        self.stacked_widget.addWidget(main_window)

        #podpiecie przyciskow
        slots = {
            'learn': self.pool,
            'auto': self.auto,
            'base': self.base,
            'sets': self.sets,
            'close': QtCore.QCoreApplication.instance().quit,
            }

        main_window.slot_conn(slots)

    #definicje funkcji podpinanych do przyciskow
    def pool(self):
        pool_window = PoolWindow(self.stacked_widget, self.main_base_word)
        self.stacked_widget.addWidget(pool_window)
        self.stacked_widget.setCurrentWidget(pool_window)

    def auto(self):
        print('auto')

    def sets(self):
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


