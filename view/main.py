__author__ = 'mcmushroom'

from PyQt4 import QtGui
from PyQt4.QtGui import QStackedWidget

from view.main_view import MainWindow
"""
from view.word_pool import PoolWindow
from view.base_view import BaseWindow
from view.setting_view import SettingWindow
from view.chooseBase_view import ChooseBase
from view.learn_view import LearnWindow
"""
from model.data_storage import DataStorage


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent)

        print('>rozpoczecie biegu programu')#$

        # glowna baza slowek
        self.main_base_word = DataStorage("../data/main_base")
        self.main_base_word.open()

        # otwarcie sesji
        self.session_word = DataStorage("../data/session_word")
        self.session_word.open()

        print('>zainicjowano bazy slowek i sesji')#$

        # deklaracja listy kontenerow widget'ow dla widokow
        self.windows_c = QStackedWidget()
        self.setCentralWidget(self.windows_c)

        self.windows = {}
        for i, val in enumerate([MainWindow(), ]):
            self.windows[val.__class__.__name__] = {'instance': val, 'id': i}

        #...

        #'word_pool': PoolWindow(self),
        #'base': BaseWindow(self),
        #'setting': SettingWindow(self),
        #'choose_base': ChooseBase(self),
        #'learn': LearnWindow(self),

        self.switch_window('MainWindow')

        print('>stworzono stos widokow')#$

        """
        # zaladowanie widokow


        print('>zaladowano widoki')#$

        self.stacked_widgets.addWidget(self.windows['main'])

        print('>dodano widok glowny do stosu widokow')#$
        
        # ustawienia okna
        self.setWindowIcon(QtGui.QIcon('../image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

        print('>ustawiono okno')#$

        self.stacked_widgets.setCurrentWidget(self.stacked_widgets.currentWidget())
        """

    def switch_window(self, name):
        self.windows_c.setCurrentWidget(self.windows_c.widget(self.windows[name]['id']))

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


