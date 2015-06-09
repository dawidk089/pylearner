__author__ = 'mcmushroom'

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re

class ChooseBase(QtGui.QWidget):

    def __init__(self, stacked_widget, main_base_word, word_list):
        super().__init__()

        self.stacked_widget = stacked_widget
        self.adding_words_list = word_list
        self.base_word_list = main_base_word

        print('base_word_list: ', self.adding_words_list)

        self.header = QLabel('<h1><b>Główna baza słówek</b></h1>', self)
        self.list_caption = QLabel('Wybierz słówka z bazy', self)

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

        self.initUI()

    # inicjalizacja widget'ow i layout'u
    def initUI(self):

        print('word list: ', self.word_list)

        #layout step 1


        #layout step 2
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        done_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', header_l)
        self.done_box = self.box('horizontal', done_l)

        # layout step 3
        main_l = [
            ('layout', self.header_box),
            ('widget', self.list_caption),
            ('widget', self.word_list),
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
        self.base_word_list.save()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def cancel(self):
        self.base_word_list.reset()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

#   definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])