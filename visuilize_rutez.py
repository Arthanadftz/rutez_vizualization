#!/usr/local/bin/python3
from rutez import Rutez
import json

rutez = Rutez()
rutez.load()

sinsets_keys = list(sorted(rutez.sinsets.keys()))

#print(sinsets_keys)
root = "ПОСТОЯННАЯ СУЩНОСТЬ"
root_container = rutez.sinsets[root]
root_sins = root_container['words']
root_rels = root_container['relations']


#print(root_rels)
"""
root = "ПОСТОЯННАЯ СУЩНОСТЬ"
root_container = rutez.sinsets[root]
root_sins = root_container['words']
root_rels = root_container['relations']

root_dict = {root: {}, "Synonyms": root_sins}

for rel in root_rels:
    if rel[0] == "НИЖЕ":
        #root_dict[root][rel[1]] = {rel[1]: rutez.sinsets[rel[1]]['relations'], "Synonyms": rutez.sinsets[rel[1]]['words']}
        root_dict[root][rel[1]] = {}
        root_dict[root][rel[1]]['Synonyms'] = rutez.sinsets[rel[1]]['words']
        rels = rutez.sinsets[rel[1]]['relations']
        for rela in rels:
            if rela[0] == "НИЖЕ":
                root_dict[root][rel[1]][rela[1]] = {}
                root_dict[root][rel[1]][rela[1]]["Synonyms"] = rutez.sinsets[rela[1]]['words']

#print(root_dict)
with open('vis_dict.json', 'w') as f:
    json.dump(root_dict, f, indent=4, ensure_ascii=False)
"""
root = "ПОСТОЯННАЯ СУЩНОСТЬ"
root_container = rutez.sinsets[root]
root_sins = root_container['words']

def dig_deep(root_key):
    root_rels = rutez.sinsets[root_key]['relations']
    root_sins = rutez.sinsets[root_key]['words']
    #, "Synonyms": rutez.sinsets[rel[1]]['words']

    d = {rel[1]: dig_deep(rel[1]) for rel in root_rels if rel[0] == "НИЖЕ"}
    d["Synonyms"] = root_sins
    #print(d)
    return d

    #for key in d:
    #    d[key] = dig_deep(key)

    """
    for rel in root_rels:
        if rel[0] == "НИЖЕ":
            #return {rel[1]: dig_deep(rel[1]), "Synonyms": root_sins}
            root_dict[rel[1]] = {rel[1]: dig_deep(root_dict[rel[1]], rel[1]), "Synonyms": root_sins}
            #root_dict["Synonyms"] = root_sins
    """


#dig_deep(root)
root_dict = {root: dig_deep(root), "Synonyms": root_sins}
#print(root_dict)

with open('vis_dict_test.json', 'w') as f:
    json.dump(root_dict, f, indent=4, ensure_ascii=False)
