__author__ = 'mcmushroom'

# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore, Qt
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import re


class BaseWindow(QtGui.QWidget):

    def __init__(self, stacked_widget, word_list):
        super().__init__()

        self.stacked_widget = stacked_widget

        self.base_word_list = word_list

        self.header = QLabel('<h1><b>Główna baza słówek</b></h1>', self)

        self.button = {}

        self.button["add"] = QtGui.QPushButton('Dodaj', self)
        self.button["import"] = QtGui.QPushButton('Importuj', self)
        self.button["change"] = QtGui.QPushButton('Zmień', self)
        self.button["delete"] = QtGui.QPushButton('Usuń', self)
        self.button["cancel"] = QtGui.QPushButton('Anuluj', self)
        self.button["done"] = QtGui.QPushButton('Gotowe', self)

        #definicja listy
        self.word_list = QListView()
        self.word_list.setMinimumSize(600, 400)
        #word_list.setWindowTitle('Example List')
        self.list_model = QStandardItemModel(self.word_list)
        print('list_model before: ', self.list_model)
        for row in self.base_word_list.get():
            print('row: ', row)
            self.list_model.appendRow(QStandardItem(row[0]+" = "+row[1]))
        print('list_model after: ', self.list_model)
        self.word_list.setModel(self.list_model)
        self.word_list.clicked.connect(self.catch_item)
        self.choosen_item = None

        self.que = QLineEdit(self)
        self.ans = QLineEdit(self)

        self.initUI()

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        print('word list: ', self.word_list)
        #layout step 1
        self.add_butt_l = [
            ('stretch',),
            ('widget', self.button['add']),
        ]

        self.add_que_l = [
            ('widget', QLabel('słówko pytające', self)),
            ('widget', self.que),
        ]

        self.add_ans_l = [
            ('widget', QLabel('słówko odpowiadające', self)),
            ('widget', self.ans),
        ]

        self.add_butt_box = self.box('vertical', self.add_butt_l)
        self.add_que_box = self.box('vertical', self.add_que_l)
        self.add_ans_box = self.box('vertical', self.add_ans_l)

        #layout step 2
        self.header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.add_l = [
            ('layout', self.add_butt_box),
            ('layout', self.add_que_box),
            ('layout', self.add_ans_box),
            ('stretch',),
        ]

        self.import_l = [
            ('widget', self.button['import']),
            ('stretch',),
        ]

        self.change_l = [
            ('widget', self.button['change']),
            ('stretch',),
        ]

        self.delete_l = [
            ('widget', self.button['delete']),
            ('stretch',),
        ]

        self.done_l = [
            ('stretch',),
            ('widget', self.button['cancel']),
            ('widget', self.button['done']),
        ]

        self.header_box = self.box('horizontal', self.header_l)
        self.add_box = self.box('horizontal', self.add_l)
        self.import_box = self.box('horizontal', self.import_l)
        self.change_box = self.box('horizontal', self.change_l)
        self.delete_box = self.box('horizontal', self.delete_l)
        self.done_box = self.box('horizontal', self.done_l)

        #layout step 3
        main_l = [
            ('layout', self.header_box),
            ('layout', self.add_box),
            ('layout', self.import_box),
            ('layout', self.change_box),
            ('layout', self.delete_box),
            ('widget', self.word_list),
            ('layout', self.done_box),
        ]

        self.main_box = self.box('vertical', main_l)

        #podpiecie przyciskow
        slots = {
            'add': self.add,
            'change': self.change,
            'import': self.imprt,
            'delete': self.delete,
            'cancel': self.cancel,
            'done': self.done,
            }

        self.slot_conn(slots)

        self.set_edit_line(200)
        self.slot_conn()
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

    #metoda pomocnicza do dodawania elementow do listy
    def add_to_list(self, item_to_add):

        item = QStandardItem(item_to_add)
        item.setCheckable(True)
        self.list_model.appendRow(item)

    #definicje funkcji podpinanych do przyciskow
    def add(self):
        print('add')
        self.add_word()

    def change(self):
        print('change: ', self.choosen_item)
        self.list_model.setItem(self.choosen_item, QStandardItem("makarena"))

    def delete(self):
        print('delete: ', self.choosen_item)
        self.list_model.removeRow(self.choosen_item)
        self.base_word_list.remove(self.choosen_item)

    def done(self):
        print('done')
        self.base_word_list.save()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def cancel(self):
        print('cancel')
        self.base_word_list.reset()
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def imprt(self):
        print('import')
        self.file_dialog()

    def set_edit_line(self, a):
        self.que.setMaximumWidth(a)
        self.ans.setMaximumWidth(a)

#   definicja podpiec
    def slot_conn(self, slots={}):
        for key in slots:
            self.button[key].clicked.connect(slots[key])
            print(">checkpoint: slots plugging for key: ", key, 'in class: ', self.__class__.__name__)

    def add_word(self):
            que = self.que.text()
            ans = self.ans.text()
            self.que.setText("")
            self.ans.setText("")

            if que != "" and ans != "":
                print('que is empty string')
                self.base_word_list.add([que, ans])
                print('word_list: ', self.word_list)
                self.list_model.appendRow(QStandardItem(que+" = "+ans))

    def file_dialog(self):
        splitter = ''#self.left_l[8][1].text()
        list = self.word_list
        if splitter == '':
            splitter = '='
        fd = QtGui.QFileDialog(self)
        file = open(fd.getOpenFileName()).read()

        for row in file.split('\n'):
            if row != '':
                list_item = QStandardItem(row)
                self.list_model.appendRow(list_item)
                list.setModel(self.list_model)

                new_word = []
                for element in row.split(splitter):
                    new_word.append(element)
                self.base_word_list.add(new_word)

    def catch_item(self):
        items = self.word_list.selectedIndexes()
        for item in items:
            self.choosen_item = item.row()
            print('selected item index found at %s' % item.row())

#if __name__ == '__main__':
#    app = QtGui.QApplication([])
#    window = BaseWindow(None)
#    window.show()
#    app.exec_()