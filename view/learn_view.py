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

        """

        # deklaracja zmiennych pomocniczych
        # TODO podpiac ustawienia z wczytanych ustawien z main zamiast definiowania na sztywno
        self.wrong_combo_limit = 5
        self.point_limit = 3
        self.avr_time_response = 3000
        self.max_speed_writing = 1060/60/1000 #TODO trzeba podpiac max speed writing
        self.random_distance = 5

        self.eliminated_word_list = {}
        # TODO zmienna statyczna n do poprawy/sprawdzania
        n = 0
        for word in self.main.session_word.data:
            words = len(word[0].split())
            letters = len(max(word[0].split(), key=len))
            self.eliminated_word_list[n] = {
                'id': n,
                'word': word,
                'que': word[0],
                'ans': word[1],
                'points': 0,
                'wrong_combo': 0,
                'wrong_amount': 0,
                'difficulty': letters/8,
            }
            n += 1

        # zmienne wspierajace losowanie, przechpwywanie i sprawdzanie slowka
        self.current_id_word = None
        self.time = None
        self.hard_word = None

        """

        # deklaracja widget'ow
        self.header = QLabel('<h1><b>Nauka</b></h1>', self)
        self.amount_not_learned = QLabel(str(0), self)
        self.progress = QLabel(str(0), self)
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
        self.progress.setText(str(self.progress))
        self.que_line.setText(self.learner.question())
        self.learner.start_time()

    # definicja zdarzen
    def ok(self):
        self.learner.stop_time()
        answer = self.ans_editline.text()
        self.learner.check_answer(answer)
        self.ans_editline.setText('')
        self.your_ans_line.setText(answer)
        self.correct_ans_line.setText(self.learner.correct_answer())
        self.check_ans(answer)
        if self.check_end():
            self.main.switch_window('Main')
        # next question
        self.amount_not_learned.setText(str(len(self.learner.eliminated_list)))
        self.progress.setText(str(self.progress))
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

"""
    # TODO przeniesc funkcjonalnosc losowania do oddzielnej klasy
    def end_asking(self):
        # sprawdzanie czy osiagnieta ilosc  graniczna punktow dla slowka
        if self.eliminated_word_list[self.current_id_word]['points'] > self.point_limit:
            del self.eliminated_word_list[self.current_id_word]

        if not self.eliminated_word_list and self.hard_word is None:
            print('wszystkie slowka sa nauczone')
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
            return True

    def ask(self):
        # setting que word
        self.set_que_word(self.hard_word)


    def get_time(self):
        return int(round(time.time() * 1000))

    def check_ans(self, answer):
        correct = fix_word(
            self.eliminated_word_list[self.current_id_word]['ans']
        )
        word = self.eliminated_word_list[self.current_id_word]
        your = fix_word(answer)
        if correct == your:
            #set color word answer
            self.your_ans_line.setStyleSheet("QLabel { color : green; }")

            # points proportial for average time response
            #TODO to fix depends on asking state
            word['points'] += self.avr_time_response/self.time
            word['wrong_combo'] = 0
            self.hard_word = None

        else:
            if your == '':
                self.your_ans_line.setText('zrezygnowano')
                self.your_ans_line.setStyleSheet("QLabel { color : orange; }")
            else:
                self.your_ans_line.setStyleSheet("QLabel { color : red; }")
            word['wrong_combo'] += 1
            word['wrong_amount'] += 1
            # checking for hard word
            if word['wrong_combo'] > self.wrong_combo_limit:
                self.hard_word = self.current_id_word # tu juz wiem ze jest

        #$ debugger printing eliminated list
        print('eliminated word list:')
        for key in self.eliminated_word_list:
            word = self.eliminated_word_list[key]
            key_parent = key

    def set_que_word(self, word_id=None):
        if word_id is not None:
            self.current_id_word = word_id
        else:
            #TODO create special random asking
            word = random.choice(self.eliminated_word_list)
            self.current_id_word = word['id']
        self.time = self.get_time()
        self.que_line.setText(self.eliminated_word_list[self.current_id_word]['que'])
        #$ printing cuurent random word
        print('current word:', self.current_id_word)


def weighted_random(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i


def list_from_dict_list(dict_list, dict_key):
    tab = []
    for value in dict_list:
        tab.append(value[dict_key])
    return tab


"""
