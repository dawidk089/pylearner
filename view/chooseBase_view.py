# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re

class ChooseBase(QtGui.QWidget):

    def __init__(self, stacked_widget, word_pool):
        super(ChooseBase, self).__init__()

        self.word_pool = word_pool
        self.stacked_widget = stacked_widget
        self.adding_words_list = self.word_pool.session_word
        self.base_word_list = self.word_pool.main_base_word
        self.n = 0
        self.n_word_pool = self.word_pool.amount_word
        self.counter = self.word_pool.counter

        # print('base_word_list: ', self.adding_words_list)

        self.header = QLabel(u"<h1><b>Główna baza słówek</b></h1>", self)
        self.list_caption = QLabel(u'Wybierz słówka z bazy', self)
        self.amount_word = QLabel(str(self.n), self)

        self.button = {}

        self.button["cancel"] = QtGui.QPushButton('Anuluj', self)
        self.button["done"] = QtGui.QPushButton('Gotowe', self)

        # definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        self.list_model = QStandardItemModel(self.word_list)
        for row in self.base_word_list.get():
            item = QStandardItem(row[0]+" = "+row[1])
            item.setCheckable(True)
            self.list_model.appendRow(item)
        self.word_list.setModel(self.list_model)

        self.changed_item = None
        self.list_model.itemChanged.connect(self.item_change)
        #self.list_model.itemChanged()

        self.initUI()

    # inicjalizacja widget'ow i layout'u
    def initUI(self):

        # print('word list: ', self.word_list)

        #layout step 1
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        amount_l = [
            ('widget', QLabel(u'Wybrano słówek:', self)),
            ('widget', self.amount_word),
            ('stretch',),
        ]

        done_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', header_l)
        self.amount_box = self.box('horizontal', amount_l)
        self.done_box = self.box('horizontal', done_l)

        # layout step 3
        main_l = [
            ('layout', self.header_box),
            ('widget', self.list_caption),
            ('widget', self.word_list),
            ('layout', self.amount_box),
            ('layout', self.done_box),
        ]

        self.main_box = self.box('vertical', main_l)

        # podpiecie przyciskow
        slots = {
            'cancel': self.cancel,
            'done': self.done,
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

    # metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):
        self.list_model.appendRow(QStandardItem(item_to_add))

    def done(self):
        for item_nr in range(self.list_model.rowCount()):
            if self.list_model.item(item_nr).checkState() == 2:
                word = self.base_word_list.data[item_nr]
                que = word[0]
                ans = word[1]
                if not self.adding_words_list.search_if_is(word):
                    self.adding_words_list.add(word)
                    item = QStandardItem(que+" = "+ans)
                    self.word_pool.list_model.appendRow(item)
                    self.n_word_pool += 1
        self.counter.setText(str(self.n_word_pool))
        """
        self.adding_words_list.add(self.list_model.item(item_nr).text())
        if not self.session_word.search_if_is(word):
                    n += 1
                    item = QStandardItem(que+" = "+ans)
                    self.list_model.appendRow(item)
        # print('parent list get:\n', self.adding_words_list.get())
        """
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def cancel(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

#   definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])

    def item_change(self):
        self.n = 0
        for item_nr in range(self.list_model.rowCount()):
            if self.list_model.item(item_nr).checkState() == 2:
                self.n += 1
        self.amount_word.setText(str(self.n))
