__author__ = 'mcmushroom'

import json
from io import StringIO

class Word:

    def __init__(self, path="../data/words"):
        self.word_list = json.load(StringIO(open(path, 'r').read()))
        self.point_amount = 0

    def get(self):
        return self.word_list

    def get_listing(self):
        w_list = []
        for w in self.word_list:
            w_list.append(w[0]+"="+w[1])

        return self.word_list

    tablica = []
    for wiersz in open(path, 'r').read().spli('\n'):
        tablica.append(wiersz.split('='))