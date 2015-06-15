__author__ = 'mcmushroom'

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from view.view_template import View


class ChooseBase(View):

    def __init__(self, main, stacked_widgets):
        super().__init__()

        # potrzebne referencje
        self.main = main
        self.stacked_widgets = stacked_widgets
        self.adding_words_list = self.main.session_word
        self.base_word_list = self.main.main_base_word
        self.n_word_pool = self.main.amount_word
        self.counter = self.self.main.windows['word_pool'].counter
        self.list_model = self.main.windows['word_pool'].list_model

        self.n = 0

        # print('base_word_list: ', self.adding_words_list)

        self.header = QLabel('<h1><b>Główna baza słówek</b></h1>', self)
        self.list_caption = QLabel('Wybierz słówka z bazy', self)
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

        self.initUI()

    # inicjalizacja widget'ow i layout'u
    def initUI(self):

        #layout step 1
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        amount_l = [
            ('widget', QLabel('Wybrano słówek:', self)),
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
                    self.list_model.appendRow(item)
                    self.n_word_pool += 1
        self.counter.setText(str(self.n_word_pool))

        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def cancel(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def item_change(self):
        self.n = 0
        for item_nr in range(self.list_model.rowCount()):
            if self.list_model.item(item_nr).checkState() == 2:
                self.n += 1
        self.amount_word.setText(str(self.n))
