__author__ = 'mcmushroom'

from PyQt4 import QtGui

from view.main_view import MainWindow
from view.word_pool import PoolWindow
from view.base_view import BaseWindow
from view.setting_view import SettingWindow
from view.chooseBase_view import ChooseBase
from view.learn_view import LearnWindow
from model.data_storage import DataStorage


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

        print('>rozpoczecie biegu programu')#$

        # glowna baza slowek
        self.main_base_word = DataStorage("../data/main_base")
        self.main_base_word.open()
        # print('main base word -- main: ', self.main_base_word.get())

        # otwarcie sesji
        self.session_word = DataStorage("../data/session_word")
        self.session_word.open()

        print('>zainicjowano bazy slowek i sesji')#$

        # tworzenie stosu widokow
        self.stacked_widgets = QtGui.QStackedWidget()
        self.setCentralWidget(self.stacked_widgets)

        print('>stworzono stos widokow')#$

        # zaladowanie widokow
        self.windows = {
            'main': MainWindow(self, self.stacked_widgets),
            'word_pool': PoolWindow(self, self.stacked_widgets),
            'base': BaseWindow(self, self.stacked_widgets),
            'setting': SettingWindow(self, self.stacked_widgets),
            'choose_base': ChooseBase(self, self.stacked_widgets),
            'learn': LearnWindow(self, self.stacked_widgets),
        }

        print('>zaladowano widoki')#$
        
        # ustawienia okna
        self.setWindowIcon(QtGui.QIcon('../image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()

        print('>ustawiono okno')#$

        self.stacked_widget.addWidget(self.windows['main'])

        print('>dodano widok glowny do stosu widokow')#$

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


