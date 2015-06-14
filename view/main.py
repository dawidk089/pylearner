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

        # glowna baza slowek
        self.main_base_word = DataStorage("../data/main_base")
        self.main_base_word.open()
        # print('main base word -- main: ', self.main_base_word.get())

        # otwarcie sesji
        self.session_word = DataStorage("../data/session_word")
        self.session_word.open()

        # tworzenie stosu widokow
        self.stacked_widgets = QtGui.QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # zaladowanie widokow
        self.windows = {
            'main': MainWindow(self.windows, self.stacked_widgets),
            'word_pool': PoolWindow(self.windows, self.stacked_widgets),
            'base': BaseWindow(self.windows, self.stacked_widgets),
            'setting': SettingWindow(self.windows, self.stacked_widgets),
            'choose_base': ChooseBase(self.windows, self.stacked_widgets),
            'learn': LearnWindow(self.windows, self.stacked_widgets),
        }
        
        # ustawienia okna
        self.setWindowIcon(QtGui.QIcon('../image/app_ico.png'))
        self.setWindowTitle('Learner -- You just to learn_butt, and I will do the rest. ')
        self.resize(800, 600)
        self.center()
        self.stacked_widget.addWidget(self.windows['learn'])


    #definicja wysrodkowania okna
    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())


class View(QtGui.QWidget):
    def __init__(self):
        super().__init__()

    #pomocnicza metoda do budowania layout'u
    def box(self, el_type, elems):

        if el_type == 'vertical':
            box = QtGui.QVBoxLayout()

        elif el_type == 'horizontal':
            box = QtGui.QHBoxLayout()

        for elem in elems:
            if elem[0] == 'widget':
                box.addWidget(elem[1])
            elif elem[0] == 'layout':
                box.addLayout(elem[1])
            elif elem[0] == 'stretch':
                box.addStretch(1)

    #definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])


if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = Main()
    window.show()
    app.exec_()


