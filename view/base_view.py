# -*- coding: utf-8 -*-
from PyQt4.QtGui import *


class BaseWindow(QWidget):

    def __init__(self, main):
        super(BaseWindow, self).__init__()
        self.main = main

        # deklaracja zmiennych pomocniczych
        self.choosen_item_indx = None
        self.choosen_item = None

        # deklaracja widget'owWindow
        self.header = QLabel(u'<h1><b>Główna baza słówek</b></h1>', self)

        self.button = {
            "add": QPushButton('Dodaj', self),
            "import": QPushButton('Importuj', self),
            "change": QPushButton(u'Zmień', self),
            "delete": QPushButton(u'Usuń', self),
            "cancel": QPushButton('Anuluj', self),
            "done": QPushButton('Gotowe', self),
            }

        self.que_editline = QLineEdit(self)
        self.ans_editline = QLineEdit(self)
        self.new_que_editline = QLineEdit(self)
        self.new_ans_editline = QLineEdit(self)
        self.split_editline = QLineEdit(self)

        self.word_list = QListView()

        # ustawianie widget'ow
        self.word_list.setMinimumSize(600, 500)

        self.list_model = QStandardItemModel(self.word_list)

        for row in self.main.main_base_word.get():
            self.list_model.appendRow(QStandardItem(row[0]+" = "+row[1]))

        self.word_list.setModel(self.list_model)

        self.que_editline.setFixedWidth(150)
        self.ans_editline.setFixedWidth(150)
        self.new_que_editline.setFixedWidth(150)
        self.new_ans_editline.setFixedWidth(150)
        self.split_editline.setFixedWidth(50)

        self.split_editline.setText(' = ')

        # ustawianie layout'ow
        add_butt_l = [
            ('stretch',),
            ('widget', self.button['add']),
        ]

        add_que_l = [
            ('widget', QLabel(u'słówko pytające', self)),
            ('widget', self.que_editline),
        ]

        add_ans_l = [
            ('widget', QLabel(u'słówko odpowiadające', self)),
            ('widget', self.ans_editline),
        ]

        change_butt_l = [
            ('stretch',),
            ('widget', self.button['change']),
        ]

        change_que_l = [
            ('widget', QLabel(u'słówko pytające', self)),
            ('widget', self.new_que_editline),
        ]

        change_ans_l = [
            ('widget', QLabel(u'słówko odpowiadające', self)),
            ('widget', self.new_ans_editline),
        ]


        self.add_butt_box = self.box('vertical', add_butt_l)
        self.change_butt_box = self.box('vertical', change_butt_l)
        self.add_que_box = self.box('vertical', add_que_l)
        self.add_ans_box = self.box('vertical', add_ans_l)
        self.change_que_box = self.box('vertical', change_que_l)
        self.change_ans_box = self.box('vertical', change_ans_l)

        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        add_l = [
            ('layout', self.add_butt_box),
            ('layout', self.add_que_box),
            ('layout', self.add_ans_box),
            ('stretch',),
        ]

        import_l = [
            ('widget', self.button['import']),
            ('widget', self.split_editline),
            ('stretch',),
        ]

        change_l = [
            ('layout', self.change_butt_box),
            ('layout', self.change_que_box),
            ('layout', self.change_ans_box),
            ('stretch',),
        ]

        delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        done_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', header_l)
        self.add_box = self.box('horizontal', add_l)
        self.import_box = self.box('horizontal', import_l)
        self.change_box = self.box('horizontal', change_l)
        self.delete_box = self.box('horizontal', delete_l)
        self.done_box = self.box('horizontal', done_l)

        left_l = [
            ('layout', self.add_box),
            ('layout', self.import_box),
            ('layout', self.change_box),
            ('layout', self.delete_box),
            ('stretch',),
        ]

        self.left_box = self.box('vertical', left_l)

        middle_l = [
            ('layout', self.left_box),
            ('widget', self.word_list),
        ]

        self.middle_box = self.box('horizontal', middle_l)

        main_l = [
            ('layout', self.header_box),
            ('layout', self.middle_box),
            ('layout', self.done_box),
        ]

        self.main_box = self.box('vertical', main_l)

        self.setLayout(self.main_box)

        # podlaczenie zdarzen
        self.word_list.clicked.connect(self.catch_item)

        self.slots = {
            'add': self.add,
            'change': self.change,
            'import': self.imprt,
            'delete': self.delete,
            'cancel': self.cancel,
            'done': self.done,
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
            if not self.main.main_base_word.search_if_is(word):
                self.main.main_base_word.add(word)
                self.list_model.appendRow(QStandardItem(que+" = "+ans))
            else:
                self.main.statusBar().showMessage(u'Już dodane do bazy.', 3000)
        else:
            self.main.statusBar().showMessage(u'Uzupełnij formularz przed dodaniem.', 3000)

    def change(self):
        que = self.new_que_editline.text()
        ans = self.new_ans_editline.text()
        self.new_que_editline.setText("")
        self.new_ans_editline.setText("")
        if que != "" and ans != "":
            if self.choosen_item:
                word = [que, ans]
                if not self.main.main_base_word.search_if_is(word):
                    self.main.main_base_word.data[self.choosen_item_indx] = word
                    #self.choosen_item = QStandardItem(que+" = "+ans)

                    self.list_model.setItem(self.choosen_item_indx, QStandardItem(que+" = "+ans))
                else:
                    self.main.statusBar().showMessage(u'Słówko jest już w bazie.', 3000)
            else:
                self.main.statusBar().showMessage(u'Nie zaznaczono żadnego słówka.', 3000)
        else:
            self.main.statusBar().showMessage(u'Uzupełnij formularz przed dodaniem.', 3000)

    def delete(self):
        if self.choosen_item:
            self.list_model.removeRow(self.choosen_item_indx)
            self.main.main_base_word.remove(self.choosen_item_indx)
            self.choosen_item_indx = None
            self.choosen_item = None
        else:
            self.main.statusBar().showMessage(u'Nie zaznaczono żadnego słówka.', 3000)

    def done(self):
        self.main.main_base_word.save()
        self.main.switch_window('Main')

    def cancel(self):
        self.main.main_base_word.reset()
        self.main.switch_window('Main')

    def imprt(self):
        splitter = self.split_editline.text()
        if splitter != "":
            try:
                file = open(QFileDialog(self).getOpenFileName()).read()
            except UnicodeDecodeError:
                self.main.statusBar().showMessage(u'Błędny format pliku!', 3000)
                return
            for row in file.split('\n'):
                if row != '':
                    word = row.split(splitter)
                    if len(word) == 2:
                        que = row.split(splitter)[0]
                        ans = row.split(splitter)[1]
                        word = [que, ans]
                        if not self.main.main_base_word.search_if_is(word):

                            item = QStandardItem(que+" = "+ans)
                            self.list_model.appendRow(item)
                            self.main.main_base_word.add(word)

                        else:
                                self.main.statusBar().showMessage(u'Niektóre słówka są już na liście...', 3000)
                    else:
                        self.main.statusBar().showMessage(u'Istnieją linie w złym formacie...', 3000)
                else:
                    self.main.statusBar().showMessage(u'Istnieją puste linie...', 3000)
        else:
            self.main.statusBar().showMessage(u'Brak znaku rozdzielającego!', 3000)

    # TODO podziedziczyc metode catch_item po innej klasie
    def catch_item(self):
        items = self.word_list.selectedIndexes()
        for item in items:
            self.choosen_item = item.row
            self.choosen_item_indx = item.row()

        que = self.main.main_base_word.data[self.choosen_item_indx][0]
        ans = self.main.main_base_word.data[self.choosen_item_indx][1]

        self.new_que_editline.setText(que)
        self.new_ans_editline.setText(ans)

    # TODO metode add_to_list wrzucic jako statyczna-pomocnicza lub podziedziczyc po innej klasie
    # metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):
        self.list_model.appendRow(QStandardItem(item_to_add))

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
