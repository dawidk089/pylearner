__author__ = 'mcmushroom'

# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re
from model.data_storage import DataStorage
import random
import time


class Learn(QtGui.QWidget):

    def __init__(self, stacked_widget, word_list):
        super().__init__()

        self.stacked_widget = stacked_widget

        # list definition
        self.init_word_list = word_list
        self.eliminated_word_list = {}
        self.init_list()

        # labels
        self.header = QLabel('<h1><b>Nauka</b></h1>', self)
        self.amount_not_learned = QLabel(str(0), self)
        self.progress = QLabel(str(0), self)
        self.que_line = QLabel('', self)
        self.your_ans_line = QLabel('', self)
        self.correct_ans_line = QLabel('', self)
        self.count_time_off = QLabel('', self)
        self.status = QLabel('', self)

        # editline
        self.ans_editline = QLineEdit(self)
        self.ans_editline.setMaximumWidth(200)

        # button
        self.button = {}

        self.button["ok"] = QPushButton('OK', self)
        self.button["abort"] = QPushButton('przerwij', self)

        # sets
        self.amount_not_learned.setMaximumWidth(20)
        self.progress.setMaximumWidth(20)
        self.button['ok'].resize(self.button['ok'].sizeHint())
        self.que_line.setMinimumWidth(200)
        self.ans_editline.returnPressed.connect(self.button['ok'].click)

        #queries storage
        self.current_id_word = None
        self.start_time = None

        self.initUI()
        self.rand_word()

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        # layout

        # preparing boxes
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.header_box = self.box('horizontal', header_l)

        not_learned_l = [
            ('widget', self.amount_not_learned),
            ('widget', QLabel('nauczonych słówek', self)),
        ]

        self.not_learned_box = self.box('horizontal', not_learned_l)

        progress_l = [
            ('widget', self.progress),
            ('widget', QLabel('postęp', self)),
        ]

        self.progress_box = self.box('horizontal', progress_l)

        ans_l = [
            ('widget', self.ans_editline),
            ('widget', self.button['ok']),
            ('stretch',),
        ]

        self.ans_editline_box = self.box('horizontal', ans_l)

        ans_label_l = [
            ('widget', QLabel('twoja odpowiedź to', self)),
            ('widget', QLabel('prawidłowa odpowiedź to', self)),
        ]

        self.ans_label_box = self.box('vertical', ans_label_l)

        ans_value_l = [
            ('widget', self.your_ans_line),
            ('widget', self.correct_ans_line),
        ]

        self.ans_value_box = self.box('vertical', ans_value_l)

        ans_l = [
            ('layout', self.ans_label_box),
            ('layout', self.ans_value_box),
        ]

        self.ans_box = self.box('horizontal', ans_l)

        countoff_l = [
            ('widget', QLabel('szacowany czas do końca')),
            ('widget', self.count_time_off),
        ]

        self.countoff_box = self.box('horizontal', countoff_l)

        abort_l = [
            ('stretch',),
            ('widget', self.button['abort']),
        ]

        self.abort_box = self.box('horizontal', abort_l)

        # folding boxes
        middle_l = [
            ('layout', self.header_box),
            ('stretch',),
            ('layout', self.not_learned_box),
            ('layout', self.progress_box),
            ('widget', self.que_line),
            ('layout', self.ans_editline_box),
            ('layout', self.ans_box),
            ('stretch',),
            ('layout', self.countoff_box),
            ('widget', self.status),
            ('stretch',),
            ('layout', self.abort_box),
        ]

        self.middle_box = self.box('vertical', middle_l)

        main_l = [
            ('stretch',),
            ('layout', self.middle_box),
            ('stretch',),
        ]

        self.main_box = self.box('horizontal', main_l)

        #podpiecie przyciskow
        slots = {
            'ok': self.ok,
            'abort': self.abort,
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

    #definicje funkcji podpinanych do przyciskow
    def ok(self):
        self.time = self.get_time() - self.time
        print('ok', self.time)
        answer = self.ans_editline.text()
        self.ans_editline.setText('')
        self.your_ans_line.setText(answer)
        print('word id', self.current_id_word)
        self.check_ans(answer)
        self.rand_word()

    def abort(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    # definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
            print(">checkpoint: slots plugging for key: ", key, 'in class: ', self.__class__.__name__)

    # definicje funkcji pomocniczych do logiki 'nauki'
    def init_list(self):
        n = 0
        for word in self.init_word_list.data:
            self.eliminated_word_list[n] = {
                'id': n,
                'word': word,
                'que': word[0],
                'ans': word[1],
                'points': 0,
                'wrong_combo': 0,
                'wrong_amount': 0,
            }
            n += 1


    def rand_word(self):
        word = random.choice(self.eliminated_word_list)
        self.current_id_word = word['id']
        self.que_line.setText(word['que'])
        self.time = self.get_time()

    def get_time(self):
        return int(round(time.time() * 1000))

    def check_ans(self, answer):
        correct = self.eliminated_word_list[self.current_id_word]['ans']
        self.correct_ans_line.setText(correct)
        word = self.eliminated_word_list[self.current_id_word]
        #m = re.search('\s*'+correct+'\s*', answer)
        #print('regex', m.group(0))
        """
        m = re.search('(?<=\ )\w+', str(answer))
        print('regex', m.group(0))
        """
        test = re.compile("\s*"+correct+"\s*")
        if test.match(answer):
            word['points'] += 1
            word['wrong_combo'] = 0


        else:
            word['wrong_combo'] += 1
            word['wrong_amount'] += 1