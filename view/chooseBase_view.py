# -*- coding: utf-8 -*-
from PyQt4.QtGui import *


class ChooseBase(QWidget):

    def __init__(self, main):
        super(ChooseBase, self).__init__()
        self.main = main

        # deklaracja zmiennych pomocniczych
        self.changed_item = None

        # deklaracja widget'ow
        self.header = QLabel(u"<h1><b>Główna baza słówek</b></h1>", self)
        self.list_caption = QLabel(u'Wybierz słówka z bazy', self)
        self.amount_word = QLabel(str(0), self)

        self.button = {
            "cancel": QPushButton('Anuluj', self),
            "done": QPushButton('Gotowe', self),
            }

        self.word_list = QListView()

        # ustawianie widget'ow
        self.word_list.setMinimumSize(600, 400)

        self.list_model = QStandardItemModel(self.word_list)
        for row in self.main.main_base_word.get():
            item = QStandardItem(row[0]+" = "+row[1])
            item.setCheckable(True)
            self.list_model.appendRow(item)

        self.word_list.setModel(self.list_model)

        # ustawianie layout'ow
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

        self.setLayout(self.main_box)

        # podlaczenie zdarzen
        self.list_model.itemChanged.connect(self.item_change)

        self.slots = {
            'cancel': self.cancel,
            'done': self.done,
            }

        self.slot_conn(self.slots)

    # definicja zdarzen
    def done(self):
        session = self.main.session_word
        #wordpool = self.main.windows['PoolWindow']['instance']
        #wordpool_list = self.main.session_word
        #wordpool_modellist = wordpool.list_model
        #counter = wordpool.counter
        for item_nr in range(self.list_model.rowCount()):
            if self.list_model.item(item_nr).checkState() == 2:
                word = self.main.main_base_word.data[item_nr]
                #que = word[0]
                #ans = word[1]
                if not session.search_if_is(word):
                    session.add(word)
        print('session: ', self.main.session_word.data)
        self.main.switch_window('Pool')

    def cancel(self):
        self.main.switch_window('Pool')

    def item_change(self):
        n = 0
        for item_nr in range(self.list_model.rowCount()):
            if self.list_model.item(item_nr).checkState() == 2:
                n += 1
        self.amount_word.setText(str(n))

    # TODO metode add_to_list wrzucic jako statyczna-pomocnicza lub podziedziczyc po innej klasie
    # metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):
        self.list_model.appendRow(QStandardItem(item_to_add))

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

    # TODO podziedziczyc metode slot_conn po innej klasie
    # definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])