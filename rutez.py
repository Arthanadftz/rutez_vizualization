#!/usr/local/bin/python3
# encoding: utf-8
import os
import pickle
from collections import defaultdict
import sqlite3

class Rutez:

    def __init__(self, cache_folder=None):
        if cache_folder is None:
            cache_folder = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'data'
            )

        self.cache_folder = cache_folder
        self.word2sinsets = defaultdict(list)
        self.sinsets = defaultdict(lambda: {'words': [], 'relations': []})

        self.load()

    def load(self):
        path = os.path.join(self.cache_folder, 'rutez_word2sinset.pickle')
        if os.path.exists(path):
            with open(path, 'rb') as handle:
                self.word2sinsets = pickle.load(handle)

        if os.path.exists(path):
            path = os.path.join(self.cache_folder, 'rutez_sinsets.pickle')
            with open(path, 'rb') as handle:
                self.sinsets = pickle.load(handle)

    def reload(self, dbpath):
        conn = sqlite3.connect(dbpath)
        c = conn.cursor()

        c.execute("""select s.name, w.name from sinset s
                     join word w on w.id = s.id
                  """)
        for sinset_name, word in c.fetchall():
            self.sinsets[sinset_name]['words'].append(word)
            self.word2sinsets[word].append(sinset_name)

        c.execute("""select w1.name, w2.name, rel.name from rel
                     join sinset w1 on w1.id = rel.id
                     join sinset w2 on w2.id = rel.link
                  """)

        for s1name, s2name, relation in c.fetchall():
            self.sinsets[s1name]['relations'].append((relation, s2name))

        self.word2sinsets = dict(self.word2sinsets)
        self.sinsets = dict(self.sinsets)
        self.save()

    def save(self):
        path = os.path.join(self.cache_folder, 'rutez_word2sinset.pickle')
        with open(path, 'wb') as handle:
            pickle.dump(self.word2sinsets, handle, protocol=pickle.HIGHEST_PROTOCOL)

        path = os.path.join(self.cache_folder, 'rutez_sinsets.pickle')
        with open(path, 'wb') as handle:
            pickle.dump(self.sinsets, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def top_sinsets(self):
        result = []
        for name, data in self.sinsets.items():
            if not [r for r, s in data['relations'] if r == 'ВЫШЕ']:
                result.append((name, data))
        return result

    def upper_sinsets(self, sinset):
        result = []
        found_some = True
        while found_some:
            result.append(sinset)
            found_some = False
            for rel_name, other_sinset in self.sinsets[sinset]['relations']:
                if rel_name == 'ВЫШЕ':
                    sinset = other_sinset
                    found_some = True
        return result



#print(rutez.sinsets)
if __name__ == '__main__':
    from pymorphy2 import MorphAnalyzer
    from collections import defaultdict
    
    rutez = Rutez()
    rutez.load()
    sinsets_keys = list(sorted(rutez.sinsets.keys()))
    #print(sinsets_keys[:10])
    #print({sinsets_keys[1]: rutez.sinsets[sinsets_keys[1]]})
    #print(rutez.sinsets['ГОРОД РОССИЙСКОЙ ФЕДЕРАЦИИ']['relations'])
    #print(rutez.sinsets['ГОРОД'])

    cities_rutez = rutez.sinsets['ГОРОД']['relations']
    #print(cities_rutez)
    cities = [city[1].split(',')[0].capitalize() for city in cities_rutez if city[0] == 'НИЖЕ']
    cities_ = [city[1] for city in cities_rutez if city[0] == 'НИЖЕ']
    cities_sins = [rutez.sinsets[city]['words'] for city in cities_]
    #print(cities_sins)
    #cities_with_sins = list(zip(cities, cities_sins))
    capitals_rutez = rutez.sinsets['СТОЛИЦА ГОСУДАРСТВА']['relations']
    capitals = [cap[1].capitalize() for cap in capitals_rutez if cap[0] == 'НИЖЕ']
    capitals_ = [cap[1] for cap in capitals_rutez if cap[0] == 'НИЖЕ']
    capitals_sins = [rutez.sinsets[city]['words'] for city in capitals_]
    #print(capitals_sins)
    cities.append('Санкт-Петербург')
    cities_sins.append(rutez.sinsets[('Санкт-Петербург').upper()]['words'])
    #print(list(sorted(capitals)))
    #print(rutez.sinsets[cities[3].upper()])
    all_cities_names = capitals + cities
    #all_cities_names = list(sorted(all_cities_names))
    #print(all_cities_names)
    all_cities_sins = capitals_sins + cities_sins
    #all_cities_sins = list(sorted(all_cities_sins))
    #print(all_cities_sins)
    cities_sins_ = defaultdict(lambda: {'sins': [], 'cases': []})
    #all_cities_dict = defaultdict(list)

    for city, sins in zip(all_cities_names, all_cities_sins):
        for sin in sins:
            cities_sins_[city]['sins'].append(sin)

    #print(dict(cities_sins_))

    morph = MorphAnalyzer()

    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']

    """cities_infl = defaultdict(list)
    for city, city_sinset in zip(all_cities_names, all_cities_sins):
        for sin in city_sinset:
            for case in cases:
                try:
                    c = morph.parse(sin)[0].inflect({case}).word
                except AttributeError:
                    continue
                else:
                    cities_sins_[city]['cases'].append(c)
                cities_sins_[city]['cases'] = list(set(cities_sins_[city]['cases']))"""

    """for k in cities_sins_:
        for kk, v in cities_sins_[k]:
            cities_sins_[k][kk] = list(set(v))
            """
    #print(dict(cities_sins_))
    #print(rutez.sinsets['ЕРЕВАН'])
    """cities_rutez_test = rutez.sinsets['ГОРОД']['relations']
    #print(cities_rutez_test)
    res = defaultdict(list)
    def get_city(sinset):
        root = rutez.sinsets[sinset]
        root_rels = root['relations']
        root_words = root['words']

        for rel in root_rels:
            if "НИЖЕ" not in rel and rel[0] != "ВЫШЕ":
                res[rel[1]].append(rutez.sinsets[sinset]['words'])
            elif rel[0] == "НИЖЕ":
                get_city(rel[1])

    get_city('ГОРОД')
    print(res)"""
    #print(rutez.sinsets['АВИНЬОН'])


    """morph = MorphAnalyzer()


    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']

    cities_infl = defaultdict(list)
    for city in cities:
        for case in cases:
            try:
                c = morph.parse(city)[0].inflect({case}).word
            except AttributeError:
                continue
            else:
                cities_infl[city].append(c)

    for k, v in cities_infl.items():
        cities_infl[k] = list(set(v))"""
        #for el in list(set(v)):
        #    if k.lower() == el:
        #        cities_infl[k].remove(el)

    #print(dict(cities_infl))
    #print(list(cities_infl.keys()))
    #print(morph.parse(cities[0])[0].inflect({'gent'}).word)

    #cities_rutez_test = rutez.sinsets['ГОРОД']['relations']

    res = defaultdict(list)
    def get_city(sinset):
        root = rutez.sinsets[sinset]
        root_rels = root['relations']
        root_words = root['words']
        #depth = 0
        for rel in root_rels:
            if rel[0] == "НИЖЕ":
                #depth += 1
                get_city(rel[1])
            elif "НИЖЕ" not in rel:
                for word in root_words:
                    res[sinset.capitalize()].append(word)

    get_city('ГОРОД')
    res = dict(res)
    for k, v in res.items():
        if k.lower().startswith('город') or k.lower().startswith('порт'):
            del res[k]
        res[k] = list(set(v))
    print(res, end='\n\n')
    """
    for k in res:
        for val in res[k]:
            for case in cases:
                try:
                    c = morph.parse(val)[0].inflect({case}).word
                except AttributeError:
                    continue
                else:
                    res[k].append(c.upper())
        res[k] = list(set(v))
    """
    #print(res)
    #test_key = list(res.keys())[0]
    #result = res[test_key]
    #res_tt = []
    #print(result)
    res_values = [res[key] for key in res]
    print(res_values, end='\n\n')

    cases = ['nomn', 'gent', 'datv', 'accs', 'ablt', 'loct']
    for i, value in enumerate(res_values):
        for val in value:
            for case in cases:
                try:
                    c = morph.parse(val)[0].inflect({case}).word
                except AttributeError:
                    continue
                else:
                    value.append(c.upper())
            res_values[i] = list(set(value))

    print(res_values)
    #print(list(set(result + res_tt)))
