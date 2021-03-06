# -*- coding: utf-8 -*-
from PyQt4.QtGui import *


# TODO dodac przycisk reset
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
        # TODO dodac ilosc znakow spliter'a obok split_line

        self.split_counter = QLabel('')

        self.word_list = QListView()

        self.button = {
            "add": QPushButton('+', self),
            "choose": QPushButton('+', self),
            "import": QPushButton('+', self),
            "cancel": QPushButton('Anuluj', self),
            "delete": QPushButton(u'Usuń', self),
            "reset": QPushButton(u'Resetuj', self),
            'done': QPushButton('Gotowe', self),
        }

        # ustawianie widget'ow
        self.que_editline.setMaximumWidth(200)
        self.ans_editline.setMaximumWidth(200)

        self.split_line.setText(self.main.sets.data[0]['splitter'])  # TODO wstawic domyslna wartosc split_line w ustawienia

        self.list_model = QStandardItemModel(self.word_list)
        self.word_list.setMinimumSize(600, 400)
        self.word_list.setModel(self.list_model)

        # ladowanie listy z sesji
        for row in self.main.session_word.get():
            item = QStandardItem(row[0]+" = "+row[1])
            #item.setCheckable(True)
            self.list_model.appendRow(item)
        self.counter.setText(str(len(self.main.session_word.data)))


        self.button["add"].setMaximumSize(20, 20)
        self.button["choose"].setMaximumSize(20, 20)
        self.button["import"].setMaximumSize(20, 20)

        self.split_line.setMaximumWidth(200)
        self.split_counter.setText(u"ilość znaków: "+str(len(self.split_line.text())))

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

        reset_l = [
            ('widget', self.button['reset']),
            ('stretch',),
        ]

        split_l = [
            ('widget', self.split_line),
            ('widget', self.split_counter),
        ]

        self.add_box = self.box('horizontal', add_butt)
        self.chs_box = self.box('horizontal', chs_butt)
        self.impt_box = self.box('horizontal', impt_butt)

        self.w_amount_box = self.box('horizontal', w_amount_l)
        self.cancel_box = self.box('horizontal', cancel_l)
        self.delete_box = self.box('horizontal', delete_l)
        self.reset_box = self.box('horizontal', reset_l)
        self.split_box = self.box('vertical', split_l)

        left_l = [
            ('widget', QLabel(u'słówko pytające', self)),
            ('widget', self.que_editline),
            ('widget', QLabel(u'słówko odpowiadające', self)),
            ('widget', self.ans_editline),
            ('layout', self.add_box),
            ('layout', self.chs_box),
            ('layout', self.impt_box),
            ('widget', QLabel(u'znaki rozdzielające', self)),
            ('layout', self.split_box),
            ('layout', self.delete_box),
            ('layout', self.reset_box),
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
            ('stretch',),
            ('layout', self.left_box),
            ('layout', self.right_box),
            ('stretch',),
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
        self.split_line.editingFinished.connect(self.count)

        self.slots = {
            'add': self.add,
            'choose': self.choose,
            'import': self.imprt,
            'done': self.done,
            'cancel': self.cancel,
            'delete': self.delete,
            'reset': self.reset,
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
            else:
                self.main.statusBar().showMessage(u'Już dodane do listy.', 3000)
        else:
            self.main.statusBar().showMessage(u'Uzupełnij formularz przed dodaniem.', 3000)
        # TODO podpiac enter pod przycisk add z answer editline, przelaczanie kursora do question editline

    def choose(self):
        self.main.switch_window('Choose')

    # TODO zabezpieczyc anuluj w QFileDialog
    def imprt(self):
        splitter = self.split_line.text()
        if splitter != '':
            try:
                file = open(QFileDialog(self).getOpenFileName())
            except UnicodeDecodeError:
                self.main.statusBar().showMessage(u'Błędny format pliku!', 3000)
                return
            if not file:
                return
            else:
                text = file.read()
            for row in text.split('\n'):
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
                        else:
                            self.main.statusBar().showMessage(u'Niektóre słówka są już na liście...', 3000)
                    else:
                        self.main.statusBar().showMessage(u'Istnieją linie w złym formacie...', 3000)
                else:
                    self.main.statusBar().showMessage(u'Istnieją puste linie...', 3000)
        else:
            self.main.statusBar().showMessage(u'Brak znaku rozdzielającego!', 3000)

        self.counter.setText(str(len(self.main.session_word.data)))

    def cancel(self):
        self.main.switch_window('Main')

    def delete(self):
        if not self.main.session_word.data:
            self.main.statusBar().showMessage(u'Nie ma już czego usuwać.', 3000)
        if self.choosen_item is not None:
            self.list_model.removeRow(self.choosen_item)
            self.main.session_word.remove(self.choosen_item)
            self.choosen_item = None
            self.counter.setText(str(len(self.main.session_word.data)))

    def reset(self):
        print('reset')
        self.main.session_word.clear()
        self.list_model.clear()
        print('reset done')

    def done(self):
        if not self.main.session_word.data:
            self.main.statusBar().showMessage(u'Nic nie wybrałeś!', 3000)
            return
        self.main.switch_window('Learn')

    def count(self):
        self.split_counter.setText(u"ilość znaków: "+str(len(self.split_line.text())))


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