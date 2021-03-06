__author__ = 'mcmushroom'

import json


class DataStorage:

    def __init__(self, path_data):
        self.data = []
        self.path = path_data

    # TODO get do usuniecia
    def get(self):
        return self.data

    def add(self, item):
        self.data.append(item)

    def open(self):
        self.data = json.load(open(self.path, 'r'))

    def save(self):
        json.dump(self.data, open(self.path, 'w'))

    def remove(self, i):
        self.data.pop(i)

    def reset(self):
        self.data = []
        self.open()

    def clear(self):
        self.data = []
        self.save()

    def search_if_is(self, element):
        if element in self.data:
            return True
        else:
            return False