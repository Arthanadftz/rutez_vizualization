# encoding: utf-8
import os
import pickle
from collections import defaultdict
from config import config
import sqlite3


class Rutez:
    cache_folder = config.data_path

    def __init__(self):
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

    def top_sinset(self, sinset):
        pass

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
