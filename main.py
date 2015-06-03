# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui
from view.main_view import MainWindow


def main():

    app = QtGui.QApplication(sys.argv)

    ex = MainWindow()

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
