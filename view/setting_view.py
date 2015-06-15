__author__ = 'mcmushroom'

from PyQt4 import QtGui
from PyQt4.QtGui import *
import re

import random
import time

from model.data_storage import DataStorage
from view.view_template import View


class SettingWindow(View):

    def __init__(self, main, stacked_widgets):
        super().__init__()

        self.main = main
        self.stacked_widgets = stacked_widgets
        
        self.default = {
            'wrong_combo_limit': 5,
            'point_limit': 3,
            'avr_time_response': 3000,
            'random_distance': 5,
        }
        
        # sets storage
        self.sets = DataStorage('../data/settings')
        self.sets.open()

        # labels
        self.header = QLabel('<h1><b>Ustawienia</b></h1>', self)

        # editline
        self.wrong_combo_limit = QLineEdit(self)
        self.random_distance = QLineEdit(self)
        self.avr_time_response = QLineEdit(self)
        self.point_limit = QLineEdit(self)

        # button
        self.button = {}

        self.button["save"] = QPushButton('Zapisz', self)
        self.button["abort"] = QPushButton('Anuluj', self)
        self.button["defualt"] = QPushButton('Reset', self)

        # sets
        self.wrong_combo_limit.setMaximumWidth(50)
        self.random_distance.setMaximumWidth(50)
        self.avr_time_response.setMaximumWidth(50)
        self.point_limit.setMaximumWidth(50)

        # inicjalizacja jesli pusta
        if not self.sets.data:
            self.reset()
        else:
            self.set_editline()

        self.initUI()
        self.layout()

    #inicjalizacja widget'ow i layout'u
    def initUI(self):

        # layout

        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.header_box = self.box('horizontal', header_l)

        labels_l = [
            ('widget', QLabel('min odległość losowania słówka', self)),
            ('widget', QLabel('próg punktowy dla słówka', self)),
            ('widget', QLabel('limit błędnych odpowiedzi', self)),
            ('widget', QLabel('średni czas odpowiedzi', self)),
        ]

        self.labels_box = self.box('vertical', labels_l)

        editlines_l = [
            ('widget', self.random_distance),
            ('widget', self.point_limit),
            ('widget', self.wrong_combo_limit),
            ('widget', self.avr_time_response),
        ]

        self.editlines_box = self.box('vertical', editlines_l)

        contents_l = [
            ('stretch',),
            ('layout', self.labels_box),
            ('layout', self.editlines_box),
            ('stretch',),
        ]

        self.contens_box = self.box('horizontal', contents_l)
        
        button_l = [
            ('stretch',),
            ('widget', self.button['defualt']),
            ('widget', self.button['abort']),
            ('widget', self.button['save']),
        ]
        
        self.button_box = self.box('horizontal', button_l)
        
        main_l = [
            ('stretch',),
            ('layout', self.header_box),
            ('stretch',),
            ('layout', self.contens_box),
            ('stretch',),
            ('layout', self.button_box),
        ]
        
        self.main_box = self.box('vertical', main_l)
        
        #podpiecie przyciskow
        slots = {
            'save': self.save,
            'defualt': self.reset,
            'abort': self.abort,
            }

        self.slot_conn(slots)
        self.setLayout(self.main_box)
        self.show()

    #definicje funkcji podpinanych do przyciskow
    def save(self):
        self.sets.data[0]['wrong_combo_limit'] = int(self.wrong_combo_limit.text())
        self.sets.data[0]['point_limit'] = int(self.point_limit.text())
        self.sets.data[0]['avr_time_response'] = int(self.avr_time_response.text())
        self.sets.data[0]['random_distance'] = int(self.random_distance.text())
        self.sets.save()
        
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())

    def abort(self):
        self.stacked_widget.removeWidget(self.stacked_widget.currentWidget())
        
    def reset(self):
        self.sets.data[0] = self.default
        self.set_editline()
        #$
        print(self.sets.data[0])

    def set_editline(self):
        self.wrong_combo_limit.setText(str(self.sets.data[0]['wrong_combo_limit']))
        self.random_distance.setText(str(self.sets.data[0]['random_distance']))
        self.avr_time_response.setText(str(self.sets.data[0]['avr_time_response']))
        self.point_limit.setText(str(self.sets.data[0]['point_limit']))