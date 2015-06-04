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
        self.header = [
            ('stretch',),
            ('widget', QLabel('<h1><b>Nauka indywidualna</b></h1>', self)),
            ('stretch',),
        ]

        self.add_butt = [
            ('widget', QLabel('Dopisz słówko do puli', self)),
            ('widget', self.button['add']),
        ]

        self.chs_butt = [
            ('widget', QLabel('Wybierz z bazy', self)),
            ('widget', self.button['choose']),
        ]

        self.impt_butt = [
            ('widget', QLabel('Importuj z pliku', self)),
            ('widget', self.button['import']),
        ]

        self.w_amount_l = [
            ('widget', QLabel('Ilość: ', self)),
            ('widget', self.counter),
            ('stretch',),
        ]

        self.cancel_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
        ]

        self.add_box = self.box('horizontal', self.add_butt)
        self.chs_box = self.box('horizontal', self.chs_butt)
        self.impt_box = self.box('horizontal', self.impt_butt)

        w_amount_box = self.box('horizontal', self.w_amount_l)
        cancel_box = self.box('horizontal', self.cancel_l)

        self.left_l = [
            ('widget', QLabel('słówko pytające', self)),
            ('widget', QLineEdit(self)),
            ('widget', QLabel('słówko odpowiadające', self)),
            ('widget', QLineEdit(self)),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QLabel('znak rozdzielający', self)),
            ('widget', QLineEdit(self)),
            ('stretch',),
        ]

        self.right_l = [
            ('widget', QLabel('Wybrane słówka', self)),
            ('widget', self.word_list),
            ('layout', w_amount_box),
            ('layout', cancel_box),
        ]

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

        #podpiecie przyciskow
        slots = {
            'add': self.add,
            'choose': self.choose,
            'import': self.imprt,
            'cancel': self.cancel,
            }

        self.slot_conn(slots)

        self.set_butt_size(20)
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
        self.add_word()

    def choose(self):
        print('choose')
        mb = QMessageBox()

    def imprt(self):
        self.file_dialog()

    def cancel(self):
        print('cancel')
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def set_butt_size# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re


class PoolWindow(QtGui.QWidget):

    def __init__(self, stacked_widget):
        super(PoolWindow, self).__init__()

        self.stacked_widget = stacked_widget

        self.session_word = []

        self.button = {}

        self.button["add"] = QPushButton('+', self)
        self.button["choose"] = QPushButton('+', self)
        self.button["import"] = QPushButton('+', self)
        self.button["cancel"] = QPushButton('Anuluj', self)

        #definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        #word_list.setWindowTitle('Example List')
        self.list_model = QStandardItemModel(self.word_list)
        self.word_list.setModel(self.list_model)

        self.counter = QLabel(str(0), self)
        self.initUI()
        self.amount_word = 0

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        #layout
        self.header = [
            ('stretch',),
            ('widget', QLabel('<h1><b>Nauka indywidualna</b></h1>', self)),
            ('stretch',),
        ]

        self.add_butt = [
            ('widget', QLabel('Dopisz słówko do puli', self)),
            ('widget', self.button['add']),
        ]

        self.chs_butt = [
            ('widget', QLabel('Wybierz z bazy', self)),
            ('widget', self.button['choose']),
        ]

        self.impt_butt = [
            ('widget', QLabel('Importuj z pliku', self)),
            ('widget', self.button['import']),
        ]

        self.w_amount_l = [
            ('widget', QLabel('Ilość: ', self)),
            ('widget', self.counter),
            ('stretch',),
        ]

        self.cancel_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
        ]

        self.add_box = self.box('horizontal', self.add_butt)
        self.chs_box = self.box('horizontal', self.chs_butt)
        self.impt_box = self.box('horizontal', self.impt_butt)

        w_amount_box = self.box('horizontal', self.w_amount_l)
        cancel_box = self.box('horizontal', self.cancel_l)

        self.left_l = [
            ('widget', QLabel('słówko pytające', self)),
            ('widget', QLineEdit(self)),
            ('widget', QLabel('słówko odpowiadające', self)),
            ('widget', QLineEdit(self)),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QLabel('znak rozdzielający', self)),
            ('widget', QLineEdit(self)),
            ('stretch',),
        ]

        self.right_l = [
            ('widget', QLabel('Wybrane słówka', self)),
            ('widget', self.word_list),
            ('layout', w_amount_box),
            ('layout', cancel_box),
        ]

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

        #podpiecie przyciskow
        slots = {
            'add': self.add,
            'choose': self.choose,
            'import': self.imprt,
            'cancel': self.cancel,
            }

        self.slot_conn(slots)

        self.set_butt_size(20)
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
        self.add_word()

    def choose(self):
        print('choose')
        mb = QMessageBox()

    def imprt(self):
        self.file_dialog()

    def cancel(self):
        print('cancel')
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def set_butt_size(self, a):
        self.add_butt[1][1].setMaximumSize(a, a)
        self.chs_butt[1][1].setMaximumSize(a, a)
        self.impt_butt[1][1].setMaximumSize(a, a)

    def set_edit_line(self, a):
        self.left_l[1][1].setMaximumWidth(a)
        self.left_l[3][1].setMaximumWidth(a)

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
        n = 0
        for row in file.split('\n'):
            if row != '' and True:
                n += 1
                list_item = QStandardItem(row)
                list_item.setCheckable(True)
                self.list_model.appendRow(list_item)
                list.setModel(self.list_model)

        self.amount_word += n
        self.counter.setText(str(self.amount_word))
(self, a):
        self.add_butt[1][1].setMaximumSize(a, a)
        self.chs_butt[1][1].setMaximumSize(a, a)
        self.impt_butt[1][1].setMaximumSize(a, a)

    def set_edit_line(self, a):
        self.left_l[1][1].setMaximumWidth(a)
        self.left_l[3][1].setMaximumWidth(a)

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
        n = 0
        for row in file.split('\n'):
            if row != '' and True:
                n += 1
                list_item = QStandardItem(row)
                list_item.setCheckable(True)
                self.list_model.appendRow(list_item)
                list.setModel(self.list_model)

        self.amount_word += n
        self.counter.setText(str(self.amount_word))
