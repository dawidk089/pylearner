__author__ = 'mcmushroom'

from PyQt4 import QtGui

class View(QtGui.QWidget):
    def __init__(self):
        super().__init__()

    def franca(self):
        print("nie drukuje bo franca")

    #pomocnicza metoda do budowania layout'u
    def box(self, el_type, elems):

        if el_type == 'vertical':
            temp_box = QtGui.QVBoxLayout()

        elif el_type == 'horizontal':
            temp_box = QtGui.QHBoxLayout()

        for elem in elems:
            if elem[0] == 'widget':
                temp_box.addWidget(elem[1])
            elif elem[0] == 'layout':
                temp_box.addLayout(elem[1])
            elif elem[0] == 'stretch':
                temp_box.addStretch(1)

        return temp_box

    #definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
