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
        # singleton protection
        if Main.private:
            raise RuntimeError("Próba odwołania się do kontruktora singletonu klasy "+self.__class__.__name__)

        super(Main, self).__init__(parent)

        # glowna baza slowek
        self.main_base_word = DataStorage("data/main_base")
        self.main_base_word.open()

        # tworzenie stosu widokow
        self.windows_c = QtGui.QStackedWidget()
        self.setCentralWidget(self.windows_c)

        self.windows = {}

        for i, val in enumerate([MainWindow(), PoolWindow()]):
            self.windows[val.__class__.__name__] = {'instance': val, 'id': i}
            import time
            time.sleep(0.1)
            self.windows[val.__class__.__name__]['instance'].hide()
            time.sleep(0.1)

        print('length of windows list:', len(self.windows))#$

        for key in self.windows:
            self.windows_c.addWidget(self.windows[key]['instance'])

        self.setWindowIcon(QtGui.QIcon('image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

        self.switch_window('MainWindow')
        self.windows['MainWindow']['instance'].show()
        self.windows['MainWindow']['instance'].plug_buttons()

    def switch_window(self, name):
        print('przelaczanie na widok: ', name, self.windows[name])
        self.windows_c.setCurrentWidget(self.windows_c.widget(self.windows[name]['id']))
        self.windows[name]['instance'].show()
        print('id now:', self.windows_c.currentIndex())
        print('-'*100)

    # app center support
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    # singleton
    instance = None
    private = True

    @staticmethod
    def get():
        Main.private = False
        if not Main.instance:
            print('zaraz wywolam konstruktor')
            Main.instance = Main()
            print('skonczylem wywolywac konstruktor')
        Main.private = True
        return Main.instance



if __name__ == '__main__':

    app = QtGui.QApplication([])
    window = Main.get()
    window.show()
    app.exec_()


