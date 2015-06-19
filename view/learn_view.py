# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from learner.learner import Learner
import re
import random
import time


class Learn(QWidget):

    def __init__(self, main):
        super(Learn, self).__init__()
        self.main = main

        self.learner = Learner(
            self.main.session_word.data, self.main.sets.data
        )

        self.init_amount_word = len(self.learner.eliminated_list)

        # deklaracja widget'ow
        self.header = QLabel('<h1><b>Nauka</b></h1>', self)
        self.amount_not_learned = QLabel(str(0), self)
        self.progress = QLabel(str(0)+'%', self)
        self.que_line = QLabel('', self)
        self.your_ans_line = QLabel('', self)
        self.correct_ans_line = QLabel('', self)
        self.count_time_off = QLabel('', self)
        self.status = QLabel('', self)

        self.ans_editline = QLineEdit(self)
        self.ans_editline.setMaximumWidth(200)

        self.button = {
            "ok": QPushButton('OK', self),
            "abort": QPushButton('przerwij', self),
            }

        # ustawianie widget'ow
        self.amount_not_learned.setMaximumWidth(20)
        self.progress.setMaximumWidth(20)
        self.button['ok'].resize(self.button['ok'].sizeHint())
        self.que_line.setMinimumWidth(200)

        self.init_learn()

        # ustawianie layout'ow
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.header_box = self.box('horizontal', header_l)

        not_learned_l = [
            ('widget', self.amount_not_learned),
            ('widget', QLabel(u'nauczonych słówek', self)),
        ]

        self.not_learned_box = self.box('horizontal', not_learned_l)

        progress_l = [
            ('widget', self.progress),
            ('widget', QLabel(u'postęp', self)),
        ]

        self.progress_box = self.box('horizontal', progress_l)

        ans_l = [
            ('widget', self.ans_editline),
            ('widget', self.button['ok']),
            ('stretch',),
        ]

        self.ans_editline_box = self.box('horizontal', ans_l)

        ans_label_l = [
            ('widget', QLabel(u'twoja odpowiedź to', self)),
            ('widget', QLabel(u'prawidłowa odpowiedź to', self)),
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
            ('widget', QLabel(u'szacowany czas do końca')),
            ('widget', self.count_time_off),
        ]

        self.countoff_box = self.box('horizontal', countoff_l)

        abort_l = [
            ('stretch',),
            ('widget', self.button['abort']),
        ]

        self.abort_box = self.box('horizontal', abort_l)

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

        self.setLayout(self.main_box)

        # podlaczenie zdarzen
        self.ans_editline.returnPressed.connect(self.button['ok'].click)

        self.slots = {
            'ok': self.ok,
            'abort': self.abort,
            }

        self.slot_conn(self.slots)

        # pierwsze zapytanie
        # tymczasowo przeniesione do wordpool
        #self.set_que_word()
        #self.time = self.get_time()

    def init_learn(self):
        self.amount_not_learned.setText(str(len(self.learner.eliminated_list)))
        self.que_line.setText(self.learner.question())
        self.learner.start_time()

    # definicja zdarzen
    def ok(self):
        # obsluzenie odpowiedzi
        self.learner.stop_time()
        answer = self.ans_editline.text()
        valid = self.learner.check_answer(answer)
        self.ans_editline.setText('')
        self.your_ans_line.setText(answer)
        # TODO ustawic kolorki odpowiedzi
        self.correct_ans_line.setText(self.learner.correct_answer())
        #self.check_ans(answer)
        if self.learner.check_end():
            # TODO zrobic messagebox zakonczenia nauki
            self.main.switch_window('Main')
            return

        # nastepne pytanie
        not_learned = len(self.learner.eliminated_list)
        self.amount_not_learned.setText(str(not_learned))
        all_word = len(self.main.session_word.data)
        learned = all_word - not_learned
        print('progress: ', learned, '(', not_learned, ')/', all_word, '; ', valid, sep='')
        self.progress.setText(str(learned/all_word))
        self.que_line.setText(self.learner.question())
        self.learner.start_time()

    def abort(self):
        self.main.switch_window('Main')

    # TODO podziedziczyc metode slot_conn po innej klasie
    # definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])

    # TODO wrzucic metode box jako statyczna w main
    # pomocnicza metoda do budowania layout'u
    def box(self, el_type, elems):

        if el_type == 'vertical':
            box = QVBoxLayout()

        elif el_type == 'horizontal':
            box = QHBoxLayout()

        for elem in elems:
            if elem[0] == 'widget':
                box.addWidget(elem[1])
            elif elem[0] == 'layout':
                box.addLayout(elem[1])
            elif elem[0] == 'stretch':
                box.addStretch(1)

        return box
