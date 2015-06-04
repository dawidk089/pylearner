__author__ = 'mcmushroom'

from model.data_storage import DataStorage

#zapis

main_base = DataStorage('test_storage_data.dat')

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

for element in data:
    main_base.add(element)

main_base.save()

del main_base

#odczyt

main_base2 = DataStorage('test_storage_data.dat')

print('all in new obj: ', main_base2.get())

main_base2.open()

print('all in load obj: ', main_base2.get())

print('one in load obj: ', main_base2.get()[5][1])