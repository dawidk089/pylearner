__author__ = 'mcmushroom'

from PyQt4 import QtCore, QtGui
from view.main_view import MainWindow
from view.word_pool import PoolWindow


class Main(QtGui.QMainWindow):

    def __init__(self, parent=None):
        super(Main, self).__init__(parent)

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
        slots = [ self.pool, ]
        main_window.button["learn"].clicked.connect(self.pool)
        main_window.slot_conn()


    def pool(self):
        pool_window = PoolWindow()
        self.stacked_widget.addWidget(pool_window)
        self.stacked_widget.setCurrentWidget(pool_window)

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())



class LoginWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoginWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.button = QtGui.QPushButton('Login')
        layout.addWidget(self.button)
        self.setLayout(layout)
        # you might want to do self.button.click.connect(self.parent().login) here


class LoggedWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(LoggedWidget, self).__init__(parent)
        layout = QtGui.QHBoxLayout()
        self.label = QtGui.QLabel('logged in!')
        layout.addWidget(self.label)
        self.setLayout(layout)



if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = Main()
    window.show()
    app.exec_()


