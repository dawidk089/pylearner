# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
from model.data_storage import DataStorage
from view.chooseBase_view import ChooseBase


class PoolWindow(QtGui.QWidget):

    def __init__(self, stacked_widget, main_base_word):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.main_base_word = main_base_word

        self.session_word = DataStorage("../data/session_word")
        self.session_word.open()

        self.counter = QLabel(str(0), self)
        self.que_editline = QLineEdit(self)
        self.ans_editline = QLineEdit(self)
        self.que_editline.setMaximumWidth(200)
        self.ans_editline.setMaximumWidth(200)

        self.button = {}

        self.button["add"] = QPushButton('+', self)
        self.button["choose"] = QPushButton('+', self)
        self.button["import"] = QPushButton('+', self)
        self.button["cancel"] = QPushButton('Anuluj', self)
        self.button["delete"] = QPushButton('Usuń', self)
        self.button["add"].setMaximumSize(20, 20)
        self.button["choose"].setMaximumSize(20, 20)
        self.button["import"].setMaximumSize(20, 20)

        #definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        #word_list.setWindowTitle('Example List')
        self.list_model = QStandardItemModel(self.word_list)
        self.word_list.setModel(self.list_model)
        self.word_list.clicked.connect(self.catch_item)

        self.split_line = QLineEdit(self)
        self.split_line.setText(' = ')

        self.choosen_item = None

        self.initUI()
        self.amount_word = 0

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        #layout
        header = [
            ('stretch',),
            ('widget', QLabel('<h1><b>Nauka indywidualna</b></h1>', self)),
            ('stretch',),
        ]

        add_butt = [
            ('widget', QLabel('Dopisz słówko do puli', self)),
            ('widget', self.button['add']),
        ]

        chs_butt = [
            ('widget', QLabel('Wybierz z bazy', self)),
            ('widget', self.button['choose']),
        ]

        impt_butt = [
            ('widget', QLabel('Importuj z pliku', self)),
            ('widget', self.button['import']),
        ]

        w_amount_l = [
            ('widget', QLabel('Ilość: ', self)),
            ('widget', self.counter),
            ('stretch',),
        ]

        cancel_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
        ]

        delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        self.add_box = self.box('horizontal', add_butt)
        self.chs_box = self.box('horizontal', chs_butt)
        self.impt_box = self.box('horizontal', impt_butt)

        self.w_amount_box = self.box('horizontal', w_amount_l)
        self.cancel_box = self.box('horizontal', cancel_l)
        self.delete_box = self.box('horizontal', delete_l)

        left_l = [
            ('widget', QLabel('słówko pytające', self)),
            ('widget', self.que_editline),
            ('widget', QLabel('słówko odpowiadające', self)),
            ('widget', self.ans_editline),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QLabel('znak rozdzielający', self)),
            ('widget', self.split_line),
            ('layout', self.delete_box),
            ('stretch',),
        ]

        right_l = [
            ('widget', QLabel('Wybrane słówka', self)),
            ('widget', self.word_list),
            ('layout', self.w_amount_box),
            ('layout', self.cancel_box),
        ]

        self.left_box = self.box('vertical', left_l)
        self.right_box = self.box('vertical', right_l)

        self.top_box = self.box('horizontal', header)

        bottom_l = [
            ('layout', self.left_box),# ?! to fix
            ('layout', self.right_box),
        ]

        self.bottom_box = self.box('horizontal', bottom_l)

        main_l = [
            ('layout', self.top_box),
            ('layout', self.bottom_box),
        ]

        self.main_box = self.box('vertical', main_l)

        #podpiecie przyciskow
        slots = {
            'add': self.add,
            'choose': self.choose,
            'import': self.imprt,
            'cancel': self.cancel,
            'delete': self.delete,
            }

        self.slot_conn(slots)
        self.setLayout(self.main_box)
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

        self.list_model.appendRow(QStandardItem(item_to_add))

    #definicje funkcji podpinanych do przyciskow
    def add(self):
        self.add_word()
        print('session word', self.session_word.get())

    def choose(self):
        chooseBase_window = ChooseBase(self.stacked_widget, self)
        self.stacked_widget.addWidget(chooseBase_window)
        self.stacked_widget.setCurrentWidget(chooseBase_window)
        print('chooseBase window has been closed')


    def imprt(self):
        self.file_dialog()
        print('session word', self.session_word.get())

    def cancel(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def delete(self):
        if self.choosen_item is not None:
            self.list_model.removeRow(self.choosen_item)
            self.session_word.remove(self.choosen_item)
            self.choosen_item = None
            self.amount_word -= 1
            self.counter.setText(str(self.amount_word))

#   definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
            print(">checkpoint: slots plugging for key: ", key, 'in class: ', self.__class__.__name__)

    def add_word(self):
        que = self.que_editline.text()
        ans = self.ans_editline.text()
        self.que_editline.setText("")
        self.ans_editline.setText("")
        if que != "" and ans != "":
            word = [que, ans]
            if not self.session_word.search_if_is(word):
                self.session_word.add(word)
                self.list_model.appendRow(QStandardItem(que+' = '+ans))
                self.amount_word += 1
                self.counter.setText(str(self.amount_word))

    def file_dialog(self):
        splitter = self.split_line.text()
        if splitter != '':
            file = open(QtGui.QFileDialog(self).getOpenFileName()).read()
            n = 0
            for row in file.split('\n'):
                if row != '':
                    word = row.split(splitter)
                    if len(word) == 2:
                        que = row.split(splitter)[0]
                        ans = row.split(splitter)[1]
                        word = [que, ans]
                        if not self.session_word.search_if_is(word):
                            n += 1
                            item = QStandardItem(que+" = "+ans)
                            self.list_model.appendRow(item)
                            self.session_word.add(word)

            self.amount_word += n
            self.counter.setText(str(self.amount_word))

    def catch_item(self):
        items = self.word_list.selectedIndexes()
        for item in items:
            self.choosen_item = item.row()
