__author__ = 'mcmushroom'

# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re


class BaseWindow(QtGui.QWidget):

    def __init__(self, stacked_widget):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.session_word = []

        self.header = QLabel('<h1><b>Nauka indywidualna</b></h1>', self)

        self.button = {}

        self.button["add"] = QtGui.QPushButton('Dodaj', self)
        self.button["import"] = QtGui.QPushButton('Importuj', self)
        self.button["change"] = QtGui.QPushButton('Zmień', self)
        self.button["delete"] = QtGui.QPushButton('Usuń', self)
        self.button["done"] = QtGui.QPushButton('Gotowe', self)

        #definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        #word_list.setWindowTitle('Example List')
        self.list_model = QStandardItemModel(self.word_list)
        self.word_list.setModel(self.list_model)

        self.ask = QLineEdit(self)
        self.que = QLineEdit(self)

        self.initUI()

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        #layout
        self.header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.add_l = [
            ('widget', self.button['add']),
            ('widget', self.ask),
            ('widget', self.que),
            ('stretch',),
        ]

        self.import_l = [
            ('widget', self.button['import']),
            ('stretch',),
        ]

        self.change_l = [
            ('widget', self.button['change']),
            ('stretch',),
        ]

        self.delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        self.done_l = [
            ('stretch',),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', self.header_l)
        self.add_box = self.box('horizontal', self.add_l)
        self.import_box = self.box('horizontal', self.import_l)
        self.change_box = self.box('horizontal', self.change_l)
        self.delete_box = self.box('horizontal', self.delete_l)
        self.done_box = self.box('horizontal', self.done_l)

        main_l = [
            ('layout', self.header_box),
            ('layout', self.add_box),
            ('layout', self.import_box),
            ('layout', self.change_box),
            ('layout', self.delete_box),
            ('widget', self.word_list),
            ('layout', self.done_box),
        ]

        main_box = self.box('vertical', main_l)

        #podpiecie przyciskow
        slots = {
            'add': self.add,
            'change': self.change,
            'import': self.imprt,
            'delete': self.delete,
            'done': self.done,
            }

        self.slot_conn(slots)

        self.set_edit_line(200)
        self.slot_conn()
        self.setLayout(main_box)
        self.show()

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

        return box

    #metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):

        item = QStandardItem(item_to_add)
        item.setCheckable(True)
        self.list_model.appendRow(item)

    #definicje funkcji podpinanych do przyciskow
    def add(self):
        print('add')

    def change(self):
        print('change')

    def delete(self):
        print('delete')

    def done(self):
        print('done')

    def imprt(self):
        print('import')

    def set_edit_line(self, a):
        self.ask.setMaximumWidth(a)
        self.que.setMaximumWidth(a)

#   definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
            print(">checkpoint: slots plugging for key: ", key, 'in class: ', self.__class__.__name__)

    def add_word(self):
        ask = self.left_l[1][1].text()
        que = self.left_l[3][1].text()
        self.session_word.append((ask, que))
        print('session word: ', self.session_word)
        list_item = QStandardItem(ask+' = '+que)
        list_item.setCheckable(True)
        self.list_model.appendRow(list_item)
        self.amount_word += 1
        self.counter.setText(str(self.amount_word))

    def file_dialog(self):
        splitter = self.left_l[8][1].text()
        list = self.right_l[1][1]
        if splitter == '':
            splitter = '='
        fd = QtGui.QFileDialog(self)
        file = open(fd.getOpenFileName()).read()

        for row in file.split('\n'):
            if row != '' and True:
                list_item = QStandardItem(row)
                list_item.setCheckable(True)
                self.list_model.appendRow(list_item)
                list.setModel(self.list_model)

if __name__ == '__main__':
    app = QtGui.QApplication([])
    window = BaseWindow(None)
    window.show()
    app.exec_()