__author__ = 'mcmushroom'

from PyQt4 import QtCore, QtGui
from view.main_view import MainWindow
from view.word_pool import PoolWindow
from view.chooseBase_view import ChooseBase
from view.base_view import BaseWindow
from view.setting_view import SettingWindow
from model.data_storage import DataStorage


class Main(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # glowna baza slowek
        self.main_base_word = DataStorage("data/main_base")
        self.main_base_word.open()

        # tworzenie stosu widokow
        self.windows_c = QtGui.QStackedWidget()
        self.setCentralWidget(self.windows_c)

        self.windows = {}

        for i, val in enumerate([MainWindow(self), PoolWindow(self)]):
            self.windows[val.__class__.__name__] = {'instance': val, 'id': i}

        print('length of windows list:', len(self.windows))#$

        #self.windows_c.setCurrentIndex(0)
        self.switch_window('MainWindow')
        #self.windows['MainWindow']['instance'].plug_buttons()


        self.setWindowIcon(QtGui.QIcon('image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

    def switch_window(self, name):
        print('przelaczanie na widok: ', name, self.windows[name])
        next = self.windows[name]
        current = self.windows_c.currentWidget()
        self.windows_c.removeWidget(current)
        self.windows_c.addWidget(next['instance'])
        self.windows_c.setCurrentIndex(next['id'])
        next['instance'].show()

        print('id now:', self.windows_c.currentIndex())


    # app center support
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QtGui.QApplication([])
    main_w_l = Main()
    main_w_l.show()
    app.exec_()


