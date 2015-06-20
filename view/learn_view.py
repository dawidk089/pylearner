# -*- coding: utf-8 -*-
from PyQt4.QtGui import *
from learner.learner import Learner
from wykres.activity import MyDynamicMplCanvas


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

        self.chart = MyDynamicMplCanvas(self, width=10, height=2, dpi=100)

        # ustawianie widget'ow
        self.amount_not_learned.setMaximumWidth(30)
        self.progress.setMaximumWidth(30)
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

        chart_l = [
            ('widget', QLabel('Aktywność odpowiedzi')),
            ('widget', self.chart),

        ]

        self.chart_box = self.box('vertical', chart_l)

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
            """
            ('stretch',),
            ('layout', self.chart_box),
            ('widget', self.status),
            ('stretch',),
            ('layout', self.abort_box),
            """
        ]

        self.middle_box = self.box('vertical', middle_l)

        top_l = [
            ('stretch',),
            ('layout', self.middle_box),
            ('stretch',),
        ]

        self.top_box = self.box('horizontal', top_l)

        main_l = [
            ('stretch',),
            ('layout', self.top_box),
            ('stretch',),
            ('layout', self.chart_box),
            ('stretch',),
            ('layout', self.abort_box),
        ]

        self.main_box = self.box('vertical', main_l)

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
        self.que_line.setText('<b>'+self.learner.question()+'</b>')
        self.learner.start_time()

    # definicja zdarzen
    def ok(self):
        # obsluzenie odpowiedzi
        self.learner.stop_time()
        answer = self.ans_editline.text()
        valid = self.learner.check_answer(answer)
        self.ans_editline.setText('')
        self.your_ans_line.setText(answer)

        if answer == '':
            self.your_ans_line.setText('zrezygnowano...')
            self.your_ans_line.setStyleSheet("QLabel { color : orange; }")
        else:
            self.chart.update_figure(self.learner.norm_time())
            if valid:
                self.your_ans_line.setStyleSheet("QLabel { color : green; }")
            elif not valid:
                self.your_ans_line.setStyleSheet("QLabel { color : red; }")

        self.correct_ans_line.setText(self.learner.correct_answer())
        self.correct_ans_line.setStyleSheet("QLabel { color : blue; }")

        #self.chart.update_figure(self.learner.norm_time())
        #self.chart.update_figure(self.learner.norm_time())

        #self.check_ans(answer)
        if self.learner.check_end():
            self.main.switch_window('Main')
            reply = QMessageBox()
            reply.addButton(QMessageBox.Ok)
            reply.setWindowTitle('Koniec :)')
            reply.setText(u'Skończyłeś się uczyć.')
            reply.setInformativeText(u'Umiesz już wszystko!')
            reply.exec()
            return

        # nastepne pytanie
        not_learned = len(self.learner.eliminated_list)
        self.amount_not_learned.setText(str(not_learned))
        all_word = len(self.main.session_word.data)
        learned = all_word - not_learned
        self.progress.setText(str(learned/all_word*100))
        self.que_line.setText('<b>'+self.learner.question()+'</b>')
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
