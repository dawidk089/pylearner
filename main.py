# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from view.main_view import MainWindow
from view.word_pool import PoolWindow
from view.chooseBase_view import ChooseBase
from view.base_view import BaseWindow
from view.setting_view import SettingWindow
from view.learn_view import Learn
from model.data_storage import DataStorage


class Main(QMainWindow):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        # glowna baza slowek
        self.main_base_word = DataStorage("data/main_base")
        self.main_base_word.open()

        # przechowywanie sesji
        # TODO wprowadzic obsluzenie przywracania sesji
        self.session_word = DataStorage("data/session_word")
        self.session_word.open()

        # wczytanie ustawien z pliku
        self.sets = DataStorage('data/settings')
        self.sets.open()

        # tworzenie stosu widokow
        self.windows_c = QStackedWidget()
        self.setCentralWidget(self.windows_c)

        # przechowywanie instancji klas przechowywujacych widgety poszczegolnych 'widokow'
        self.windows = {
            'Main': MainWindow,
            'Pool': PoolWindow,
            'Choose': ChooseBase,
            'Base': BaseWindow,
            'Setting': SettingWindow,
            'Learn': Learn,
            }

        # ustawienie okna
        self.setWindowIcon(QIcon('image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

    # wsparcie przelaczania 'widokow'
    def switch_window(self, name):
        window = self.windows[name](self)
        while self.windows_c.count() > 0:
            self.windows_c.removeWidget(self.windows_c.currentWidget())
        self.windows_c.addWidget(window)

    # wsparcie wysrodkowania okna
    def center(self):

        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


if __name__ == '__main__':

    app = QApplication([])

    main = Main()
    main.switch_window('Main')
    main.show()

    app.exec_()


