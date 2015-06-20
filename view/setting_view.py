# -*- coding: utf-8 -*-
from PyQt4.QtGui import *


class SettingWindow(QWidget):

    def __init__(self, main):
        super(SettingWindow, self).__init__()
        self.main = main

        # deklaracja zmiennych pomocniczych
        self.default = {
            'wrong_combo_limit': 5,
            'point_limit': 3,
            'avr_time_response': 3000,
            'random_distance': 5,
            'splitter': ' = ',
        }

        # deklaracja widget'ow
        self.header = QLabel('<h1><b>Ustawienia</b></h1>', self)

        self.wrong_combo_limit = QLineEdit(self)
        self.random_distance = QLineEdit(self)
        self.avr_time_response = QLineEdit(self)
        self.point_limit = QLineEdit(self)
        self.splitter = QLineEdit(self)

        self.button = {
            "save": QPushButton('Zapisz', self),
            "abort": QPushButton('Anuluj', self),
            "defualt": QPushButton('Reset', self),
            }

        # ustawianie widget'ow
        #self.wrong_combo_limit.setMaximumWidth(50)
        #self.random_distance.setMaximumWidth(50)
        #self.avr_time_response.setMaximumWidth(50)
        #self.point_limit.setMaximumWidth(50)

        # TODO sprawdzic zabezpieczenie ustawien przed usunieciem pliku
        # inicjalizacja jesli pusta
        #if not self.main.sets.data:
        #    self.reset()
        #else:
        self.set_editline()

        # ustawianie layout'ow
        header_l = [
            ('stretch',),
            ('widget', self.header),
            ('stretch',),
        ]

        self.header_box = self.box('horizontal', header_l)

        labels_l = [
            ('widget', QLabel(u'min odległość losowania słówka', self)),
            ('widget', QLabel(u'próg punktowy dla słówka', self)),
            ('widget', QLabel(u'limit błędnych odpowiedzi', self)),
            ('widget', QLabel(u'średni czas odpowiedzi', self)),
            ('widget', QLabel(u'znaki rozdzielające', self)),
        ]

        self.labels_box = self.box('vertical', labels_l)

        editlines_l = [
            ('widget', self.random_distance),
            ('widget', self.point_limit),
            ('widget', self.wrong_combo_limit),
            ('widget', self.avr_time_response),
            ('widget', self.splitter),
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

        self.setLayout(self.main_box)
        
        # podlaczenie zdarzen
        slots = {
            'save': self.save,
            'defualt': self.reset,
            'abort': self.abort,
            }

        self.slot_conn(slots)

    # definicja zdarzen
    def save(self):
        self.main.sets.data[0]['wrong_combo_limit'] = int(self.wrong_combo_limit.text())
        self.main.sets.data[0]['point_limit'] = int(self.point_limit.text())
        self.main.sets.data[0]['avr_time_response'] = int(self.avr_time_response.text())
        self.main.sets.data[0]['random_distance'] = int(self.random_distance.text())
        self.main.sets.data[0]['splitter'] = self.splitter.text()
        self.main.sets.save()
        
        self.main.switch_window('Main')

    def abort(self):
        self.main.sets.reset()
        self.set_editline()
        self.main.switch_window('Main')
        
    def reset(self):
        self.main.sets.data[0] = self.default
        self.set_editline()

    # metoda wspierajaca ustawianie biezacych wartosci w editline'ach
    def set_editline(self):
        self.wrong_combo_limit.setText(str(self.main.sets.data[0]['wrong_combo_limit']))
        self.random_distance.setText(str(self.main.sets.data[0]['random_distance']))
        self.avr_time_response.setText(str(self.main.sets.data[0]['avr_time_response']))
        self.point_limit.setText(str(self.main.sets.data[0]['point_limit']))
        self.splitter.setText(str(self.main.sets.data[0]['splitter']))

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