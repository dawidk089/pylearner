# -*- coding: utf-8 -*-


import re
import time
import random


class Learner:
    def __init__(self, word_list, settings):

        self.settings = settings
        self.init_list = word_list
        print('init word: ', self.init_list)

        self.eliminated_list = {}
        for indx, word in self.init_list:
            letters = len(max(word[0].split(), key=len))
            self.eliminated_list[indx] = {
                'id': indx,
                'word': word,
                'que': word[0],
                'ans': word[1],
                'points': 0,
                'wrong_combo': 0,
                'wrong_amount': 0,
                'difficulty': letters/8,
            }

        self.current_id = None
        self.hard_id = None
        self.time = None

    def start_time(self):
        self.time = get_time()

    def stop_time(self):
        self.time = get_time() - self.time

    def reset_time(self):
        self.time = None

    def question(self):
        if self.hard_id:
            return self.eliminated_list[self.hard_id]['que']
        else:
            weights = []
            for key in self.eliminated_list:
                weights.append(self.eliminated_list[key]['difficulty'])
            ind = weighted_random(weights)
            print('wylosowano', ind)
            return self.eliminated_list[ind]['que']

    def check_answer(self, answer):
        current = self.eliminated_list[self.current_id]
        if fix_word(answer) == fix_word(current['que']):
            # dobra odpowiedz
            current['points'] = self.time/self.settings['avr_time_response']
            current['wrong_combo'] = 0
            self.hard_id = None
            return True
        else:
            # zla odpowiedz
            current['wrong_combo'] += 1
            current['worng_amount'] += 1
            return False

    def check_end(self):
        current = self.eliminated_list[self.current_id]
        self.time = None
        if current['wrong_combo'] >= self.settings['wrong_combo_limit']:
            self.hard_id = current['id']
            self.current_id = None
            return False
        elif current['points'] >= self.settings['point_limit']:
            del self.eliminated_list[self.current_id]
            self.current_id = None
            if not self.eliminated_list:
                del self
                return True

    def correct_answer(self):
        return self.eliminated_list[self.current_id]['ans']


def fix_word(l):
    whitespace = re.compile("\s*(?P<word>[A-Z]?(\s*[a-z\'])*[.|...|...?|?|!|?!]*)\s*$")
    m = whitespace.match(l)
    return bool(m) if not m else m.group('word')


def weighted_random(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    print('total:', running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i


def get_time():
        return int(round(time.time() * 1000))




