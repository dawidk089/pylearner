__author__ = 'mcmushroom'

# -*- coding: utf-8 -*-

from PyQt4 import QtGui
from PyQt4.QtGui import *
import re
import random
import time
from view.main import View


class LearnWindow(View):

    def __init__(self, main, stacked_widget):
        super().__init__()

        # bedzie pobierane z ustawien
        self.wrong_combo_limit = 5
        self.point_limit = 3
        self.avr_time_response = 3000
        self.max_speed_writing = 1060/60/1000 #TODO trzeba podpiac max speed writing
        self.random_distance = 5

        self.main = main
        self.stacked_widget = stacked_widget

        # list definition
        self.init_word_list = self.main.session_word
        self.eliminated_word_list = {}
        self.init_list()

        for key in self.eliminated_word_list:
            word = self.eliminated_word_list[key]
            key_parent = key
            print(key)
            for key in word:
                print('\t', key, word[key])
        #print('eliminated word list:\n', self.eliminated_word_list)

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
        self.time = None
        self.hard_word = None

        #pierwsze zapytanie
        self.initUI()
        self.set_que_word()
        self.time = self.get_time()

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

    #definicje funkcji podpinanych do przyciskow
    def ok(self):
        # set time response
        self.time = self.get_time() - self.time
        answer = self.ans_editline.text()
        self.ans_editline.setText('')
        self.your_ans_line.setText(answer)
        self.correct_ans_line.setText(self.eliminated_word_list[self.current_id_word]['ans'])
        self.check_ans(answer)
        if self.end_asking():
            return
        # next question
        #$ oddzielacz
        print('-'*50)
        print('hard word: ', self.hard_word, sep='')
        self.set_que_word(self.hard_word)

    def abort(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    # definicje funkcji pomocniczych do logiki 'nauki'
    def init_list(self):
        n = 0
        for word in self.init_word_list.data:
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
            print(key)
            print('wrong combo: ', word['wrong_combo'], sep='')
            #for key in word:
            #   print('\t', key, '=', word[key])

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


def weighted_choice(weights):
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


def fix_word(l):
    whitespace = re.compile("\s*(?P<word>[A-Z]?(\s*[a-z\'])*[.|...|...?|?|!|?!]*)\s*$")
    m = whitespace.match(l)
    return bool(m) if not m else m.group('word')