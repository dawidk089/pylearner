__author__ = 'mcmushroom'

# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from view.view_template import View


class BaseWindow(View):

    def __init__(self, main, stacked_widgets):
        super().__init__()

        self.main = main
        self.main.stacked_widgets = stacked_widgets

        self.header = QLabel('<h1><b>Główna baza słówek</b></h1>', self)

        self.button = {}

        self.button["add"] = QtGui.QPushButton('Dodaj', self)
        self.button["import"] = QtGui.QPushButton('Importuj', self)
        self.button["change"] = QtGui.QPushButton('Zmień', self)
        self.button["delete"] = QtGui.QPushButton('Usuń', self)
        self.button["cancel"] = QtGui.QPushButton('Anuluj', self)
        self.button["done"] = QtGui.QPushButton('Gotowe', self)

        # definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        self.list_model = QStandardItemModel(self.word_list)
        for row in self.main.base_word_list.get():
            self.list_model.appendRow(QStandardItem(row[0]+" = "+row[1]))
        self.word_list.setModel(self.list_model)
        self.word_list.clicked.connect(self.catch_item)
        self.choosen_item = None

        self.que_editline = QLineEdit(self)
        self.ans_editline = QLineEdit(self)
        self.que_editline.setMaximumWidth(200)
        self.ans_editline.setMaximumWidth(200)

        self.initUI()

    # inicjalizacja widget'ow i layout'u
    def initUI(self):

        # print('word list: ', self.word_list)
        #layout step 1
        add_butt_l = [
            ('stretch',),
            ('widget', self.button['add']),
        ]

        add_que_l = [
            ('widget', QLabel('słówko pytające', self)),
            ('widget', self.que_editline),
        ]

        add_ans_l = [
            ('widget', QLabel('słówko odpowiadające', self)),
            ('widget', self.ans_editline),
        ]

        self.add_butt_box = self.box('vertical', add_butt_l)
        self.add_que_box = self.box('vertical', add_que_l)
        self.add_ans_box = self.box('vertical', add_ans_l)

        #layout step 2
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        add_l = [
            ('layout', self.add_butt_box),
            ('layout', self.add_que_box),
            ('layout', self.add_ans_box),
            ('stretch',),
        ]

        import_l = [
            ('widget', self.button['import']),
            ('stretch',),
        ]

        change_l = [
            ('widget', self.button['change']),
            ('stretch',),
        ]

        delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        done_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', header_l)
        self.add_box = self.box('horizontal', add_l)
        self.import_box = self.box('horizontal', import_l)
        self.change_box = self.box('horizontal', change_l)
        self.delete_box = self.box('horizontal', delete_l)
        self.done_box = self.box('horizontal', done_l)

        # layout step 3
        main_l = [
            ('layout', self.header_box),
            ('layout', self.add_box),
            ('layout', self.import_box),
            ('layout', self.change_box),
            ('layout', self.delete_box),
            ('widget', self.word_list),
            ('layout', self.done_box),
        ]

        self.main_box = self.box('vertical', main_l)

        # podpiecie przyciskow
        slots = {
            'add': self.add,
            'change': self.change,
            'import': self.imprt,
            'delete': self.delete,
            'cancel': self.cancel,
            'done': self.done,
            }

        self.slot_conn(slots)
        self.setLayout(self.main_box)
        self.show()

    # metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):
        self.list_model.appendRow(QStandardItem(item_to_add))

    # definicje funkcji podpinanych do przyciskow
    def add(self):
        self.add_word()

    def change(self):
        # print('change: ', self.choosen_item)
        self.list_model.setItem(self.choosen_item, QStandardItem("makarena"))

    def delete(self):
        # print('delete: ', self.choosen_item)
        self.list_model.removeRow(self.choosen_item)
        self.main.base_word_list.remove(self.choosen_item)

    def done(self):
        self.main.base_word_list.save()
        self.main.stacked_widget.removeWidget(self.main.stacked_widget.currentWidget())

    def cancel(self):
        self.main.base_word_list.reset()
        self.main.stacked_widget.removeWidget(self.main.stacked_widget.currentWidget())

    def imprt(self):
        self.file_dialog()

    def add_word(self):
        que = self.que_editline.text()
        ans = self.ans_editline.text()
        self.que_editline.setText("")
        self.ans_editline.setText("")

        if que != "" and ans != "":
            word = [que, ans]
            if not self.main.base_word_list.search_if_is(word):
                self.main.base_word_list.add(word)
                self.list_model.appendRow(QStandardItem(que+" = "+ans))

    def file_dialog(self):
        splitter = '='
        file = open(QtGui.QFileDialog(self).getOpenFileName()).read()

        for row in file.split('\n'):
            if row != '':
                word = row.split(splitter)
                if len(word) == 2:
                    que = row.split(splitter)[0]
                    ans = row.split(splitter)[1]
                    word = [que, ans]
                    if not self.main.base_word_list.search_if_is(word):

                        item = QStandardItem(que+" = "+ans)
                        self.list_model.appendRow(item)
                        self.main.base_word_list.add(word)

    def catch_item(self):
        items = self.word_list.selectedIndexes()
        for item in items:
            self.choosen_item = item.row()