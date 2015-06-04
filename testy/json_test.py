__author__ = 'mcmushroom'

import json

data = [
    ('a poster ', ' plakat'),
    ('an advertisement ', ' reklama'),
    ('to work in advertising ', ' pracowac w reklamie'),
    ('the latest product ', ' najnowszy produkt'),
    ('the disaster fall ', ' katastrofalny spadek'),
    ('a considerable increase ', ' znaczny wzrost'),
    ('a slight drop ', ' niewielki spadek'),
    ('a baggage handler ', ' bagazowy'),
    ('an air-hostess ', ' stewardessa'),
    ('a flight attendant ', ' steward'),
    ('a boarding pass ', ' karta pokladowa'),
    ('luggage ', ' bagaz'),
    ('pear ', ' gruszka'),
    ('flavours ', ' smaki'),
    ('a leaflets ', ' ulotki'),
    ('a new site ', ' nowe miejsce'),
    ]

print('>pattern data[5][1]: ', data[5][1])

with open('data.json', 'w') as fp:
    json.dump(data, fp)



with open('data.json', 'r') as fp:
    data_load_json = json.load(fp)



print('>data to compare: ', data_load_json[5][1])