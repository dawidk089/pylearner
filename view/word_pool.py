# -*- coding: utf-8 -*-
from PyQt4.QtGui import *


class PoolWindow(QWidget):

    def __init__(self, main):
        super(PoolWindow, self).__init__()
        self.main = main

        # deklaracja zmiennych pomocniczych
        self.choosen_item = None

        # deklaracja widget'ow
        self.counter = QLabel(str(0), self)

        self.que_editline = QLineEdit(self)
        self.ans_editline = QLineEdit(self)
        self.split_line = QLineEdit(self)  # TODO zmienic nazwe split_line na split_editline

        self.word_list = QListView()

        self.button = {
            "add": QPushButton('+', self),
            "choose": QPushButton('+', self),
            "import": QPushButton('+', self),
            "cancel": QPushButton('Anuluj', self),
            "delete": QPushButton(u'Usuń', self),
            'done': QPushButton('Gotowe', self),
        }

        # ustawianie widget'ow
        self.que_editline.setMaximumWidth(200)
        self.ans_editline.setMaximumWidth(200)

        self.split_line.setText(' = ')  # TODO wstawic domyslna wartosc split_line w ustawienia

        self.list_model = QStandardItemModel(self.word_list)
        self.word_list.setMinimumSize(600, 400)
        self.word_list.setModel(self.list_model)

        self.button["add"].setMaximumSize(20, 20)
        self.button["choose"].setMaximumSize(20, 20)
        self.button["import"].setMaximumSize(20, 20)

        # ustawianie layout'ow
        header = [
            ('stretch',),
            ('widget', QLabel(u'<h1><b>Nauka indywidualna</b></h1>', self)),
            ('stretch',),
        ]

        add_butt = [
            ('widget', QLabel(u'Dopisz słówko do puli', self)),
            ('widget', self.button['add']),
        ]

        chs_butt = [
            ('widget', QLabel('Wybierz z bazy', self)),
            ('widget', self.button['choose']),
        ]

        impt_butt = [
            ('widget', QLabel('Importuj z pliku', self)),
            ('widget', self.button['import']),
        ]

        w_amount_l = [
            ('widget', QLabel(u'Ilość: ', self)),
            ('widget', self.counter),
            ('stretch',),
        ]

        cancel_l = [
            ('stretch',),
            ('widget', self.button['done']),
            ('widget', self.button['cancel']),
        ]

        delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        self.add_box = self.box('horizontal', add_butt)
        self.chs_box = self.box('horizontal', chs_butt)
        self.impt_box = self.box('horizontal', impt_butt)

        self.w_amount_box = self.box('horizontal', w_amount_l)
        self.cancel_box = self.box('horizontal', cancel_l)
        self.delete_box = self.box('horizontal', delete_l)

        left_l = [
            ('widget', QLabel(u'słówko pytające', self)),
            ('widget', self.que_editline),
            ('widget', QLabel(u'słówko odpowiadające', self)),
            ('widget', self.ans_editline),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QLabel(u'znak rozdzielający', self)),
            ('widget', self.split_line),
            ('layout', self.delete_box),
            ('stretch',),
        ]

        right_l = [
            ('widget', QLabel(u'Wybrane słówka', self)),
            ('widget', self.word_list),
            ('layout', self.w_amount_box),
            ('layout', self.cancel_box),
        ]

        self.left_box = self.box('vertical', left_l)
        self.right_box = self.box('vertical', right_l)

        self.top_box = self.box('horizontal', header)

        bottom_l = [
            ('layout', self.left_box),  # TODO poprawic layout left box (?)
            ('layout', self.right_box),
        ]

        self.bottom_box = self.box('horizontal', bottom_l)

        main_l = [
            ('layout', self.top_box),
            ('layout', self.bottom_box),
        ]

        self.main_box = self.box('vertical', main_l)

        self.setLayout(self.main_box)

        # podlaczenie zdarzen
        self.word_list.clicked.connect(self.catch_item)

        self.slots = {
            'add': self.add,
            'choose': self.choose,
            'import': self.imprt,
            'done': self.done,
            'cancel': self.cancel,
            'delete': self.delete,
            }

        self.slot_conn(self.slots)

    # definicja zdarzen
    def add(self):
        que = self.que_editline.text()
        ans = self.ans_editline.text()
        self.que_editline.setText("")
        self.ans_editline.setText("")
        if que != "" and ans != "":
            word = [que, ans]
            if not self.main.session_word.search_if_is(word):
                self.main.session_word.add(word)
                self.list_model.appendRow(QStandardItem(que+' = '+ans))
                self.counter.setText(str(len(self.main.session_word.data)))

    def choose(self):
        self.main.switch_window('ChooseBase')

    def imprt(self):
        splitter = self.split_line.text()
        if splitter != '':
            file = open(QFileDialog(self).getOpenFileName()).read()
            for row in file.split('\n'):
                if row != '':
                    word = row.split(splitter)
                    if len(word) == 2:
                        que = row.split(splitter)[0]
                        ans = row.split(splitter)[1]
                        word = [que, ans]
                        if not self.main.session_word.search_if_is(word):
                            item = QStandardItem(que+" = "+ans)
                            self.list_model.appendRow(item)
                            self.main.session_word.add(word)

            self.counter.setText(str(len(self.main.session_word.data)))

    def cancel(self):
        self.main.switch_window('MainWindow')

    def delete(self):
        if self.choosen_item is not None:
            self.list_model.removeRow(self.choosen_item)
            self.main.session_word.remove(self.choosen_item)
            self.choosen_item = None
            self.counter.setText(str(len(self.main.session_word.data)))

    def done(self):
        learn = self.main.windows['Learn']['instance']
        learn.set_que_word()
        learn.time = self.get_time()
        self.main.switch_window('Learn')

    # TODO metode add_to_list wrzucic jako statyczna-pomocnicza lub podziedziczyc po innej klasie
    # metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):
        self.list_model.appendRow(QStandardItem(item_to_add))

    # TODO podziedziczyc metode catch_item po innej klasie
    # zlapanie slowka po kliknieciu w nie i zaznaczeniu (w celu pozniejszej zmiany/pozniejszego usuniecia)
    def catch_item(self):
        items = self.word_list.selectedIndexes()
        for item in items:
            self.choosen_item = item.row()

    # pomocnicza metoda do budowania layout'u
    # TODO wrzucic metode box jako statyczna w main
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

    # definicja podpiec przyciskow pod zdarzenie klikniecia
    # TODO podziedziczyc metode slot_conn po innej klasie
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])