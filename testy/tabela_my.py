__author__ = 'mcmushroom'

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *


class MyWindow(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        tv = QTableView()
        tv.setMinimumSize(400, 300)


        self.tabledata = [[1,2,3,4,5],
                          [6,7,8,9,10],
                          [11,12,13,14,15],
                          [16,17,18,19,20]]
        header = ['col_0', 'col_1', 'col_2', 'col_3', 'col_4']
        tablemodel = MyTableModel(self.tabledata, header, self)
        tv.setModel(tablemodel)

class MyTableModel(QAbstractTableModel):
    def __init__(self, datain, headerdata, parent=None):

        QAbstractTableModel.__init__(self, parent)
        self.arraydata = datain
        self.headerdata = headerdata


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())