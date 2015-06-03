# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re


class PoolWindow(QtGui.QWidget):

    def __init__(self):
        super(PoolWindow, self).__init__()

        self.initUI()
        self.amount_word = 0

    def initUI(self):

        self.header = [
            ('stretch',),
            ('widget', QtGui.QLabel('<h1><b>Nauka indywidualna</b></h1>', self)),
            ('stretch',),
        ]

        self.add_butt = [
            ('widget', QtGui.QLabel('Dopisz słówko do puli', self)),
            ('widget', QtGui.QPushButton('+', self)),
        ]

        self.chs_butt = [
            ('widget', QLabel('Wybierz z bazy', self)),
            ('widget', QPushButton('+', self)),
        ]

        self.impt_butt = [
            ('widget', QtGui.QLabel('Importuj z pliku', self)),
            ('widget', QtGui.QPushButton('+', self)),
        ]

        self.w_amount_l = [
            ('widget', QtGui.QLabel('Ilość: ', self)),
            ('widget', QtGui.QLabel(str(0), self)),
            ('stretch',),
        ]

        self.cancel_l = [
            ('stretch',),
            ('widget', QtGui.QPushButton('Anuluj', self)),
        ]

        self.set_butt_size(20)

        self.add_box = self.box('horizontal', self.add_butt)
        self.chs_box = self.box('horizontal', self.chs_butt)
        self.impt_box = self.box('horizontal', self.impt_butt)

        w_amount_box = self.box('horizontal', self.w_amount_l)
        cancel_box = self.box('horizontal', self.cancel_l)

        self.left_l = [
            ('widget', QtGui.QLabel('słówko pytające', self)),
            ('widget', QtGui.QLineEdit(self)),
            ('widget', QtGui.QLabel('słówko odpowiadające', self)),
            ('widget', QtGui.QLineEdit(self)),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QtGui.QLabel('znak rozdzielający', self)),
            ('widget', QtGui.QLineEdit(self)),
            ('stretch',),
        ]

        self.right_l = [
            ('widget', QtGui.QLabel('Wybrane słówka', self)),
            ('widget', self.list_word()),
            ('layout', w_amount_box),
            ('layout', cancel_box),
        ]

        self.set_edit_line(200)

        left_box = self.box('vertical', self.left_l)
        right_box = self.box('vertical', self.right_l)

        top_box = self.box('horizontal', self.header)

        bottom_l = [
            ('layout', left_box),
            ('layout', right_box),
        ]

        bottom_box = self.box('horizontal', bottom_l)

        main_l = [
            ('layout', top_box),
            ('layout', bottom_box),
        ]

        main_box = self.box('vertical', main_l)

        self.slot_conn()
        self.setLayout(main_box)

        self.resize(800, 600)
        self.center()
        self.setWindowTitle('Learner -- You just to learn, and I will do the rest. ')
        self.setWindowIcon(QtGui.QIcon('../image/app_ico.png'))
        self.show()

    def center(self):

        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

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

        return box

    def list_word(self, word_list_in=[]):
        word_list = QListView()
        word_list.setWindowTitle('Example List')
        word_list.setMinimumSize(600, 400)

        self.list_model = QStandardItemModel(word_list)


        for word in word_list_in:
            line = word[0]+" = "+word[1]
            print('line: ', line)
            list_item = QStandardItem(line)
            list_item.setCheckable(True)
            self.list_model.appendRow(list_item)

        word_list.setModel(self.list_model)
        return word_list

    def set_butt_size(self, a):
        self.add_butt[1][1].setMaximumSize(a, a)
        self.chs_butt[1][1].setMaximumSize(a, a)
        self.impt_butt[1][1].setMaximumSize(a, a)

    def set_edit_line(self, a):
        self.left_l[1][1].setMaximumWidth(a)
        self.left_l[3][1].setMaximumWidth(a)

    def slot_conn(self):
        self.impt_butt[1][1].clicked.connect(self.file_dialog)
        self.add_butt[1][1].clicked.connect(self.add_word)

    def add_word(self):
        ask = self.left_l[1][1].text()
        que = self.left_l[3][1].text()
        list_item = QStandardItem(ask+' = '+que)
        list_item.setCheckable(True)
        self.list_model.appendRow(list_item)
        self.amount_word += 1
        self.w_amount_l[1][1].setText(str(self.amount_word))

    def file_dialog(self):
        splitter = self.left_l[8][1].text()
        list = self.right_l[1][1]
        if splitter == '':
            splitter = '='
        fd = QtGui.QFileDialog(self)
        file = open(fd.getOpenFileName()).read()
        n = 0
        for row in file.split('\n'):
            if row != '' and True:
                n += 1
                list_item = QStandardItem(row)
                list_item.setCheckable(True)
                self.list_model.appendRow(list_item)
                list.setModel(self.list_model)

        self.amount_word += n
        self.w_amount_l[1][1].setText(str(self.amount_word))

    def simple(self):
        print("makarena")


def main():

    app = QtGui.QApplication(sys.argv)
    ex = PoolWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()