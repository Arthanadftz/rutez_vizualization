#!/usr/local/bin/python3
from rutez import Rutez
import json

rutez = Rutez()
rutez.load()

sinsets_keys = list(sorted(rutez.sinsets.keys()))

roots = [sinset[0] for sinset in rutez.top_sinsets()]
print(roots)
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
#root = "ПОСТОЯННАЯ СУЩНОСТЬ"
#root_container = rutez.sinsets[root]
#root_sins = root_container['words']

def dig_deep(root_key):
    root_rels = rutez.sinsets[root_key]['relations']
    root_sins = rutez.sinsets[root_key]['words']
    #, "Synonyms": rutez.sinsets[rel[1]]['words']

    d = {rel[1]: dig_deep(rel[1]) for rel in root_rels if rel[0] == "НИЖЕ"}

    if root_sins:
        d["Synonyms"] = root_sins

    return d

    """
    for rel in root_rels:
        if rel[0] == "НИЖЕ":
            #return {rel[1]: dig_deep(rel[1]), "Synonyms": root_sins}
            root_dict[rel[1]] = {rel[1]: dig_deep(root_dict[rel[1]], rel[1]), "Synonyms": root_sins}
            #root_dict["Synonyms"] = root_sins
    """

#root_dict = {"Root": [{root: dig_deep(root)} for root in roots]}
#root_dict = {"Root": {root: dig_deep(root)} for root in roots}
root_dict = {root: dig_deep(root) for root in roots}
root_root = {"Root": root_dict}
#root_lst = [{root: dig_deep(root)} for root in roots]
#dig_deep(root)
#root_dict = {root: dig_deep(root), "Synonyms": root_sins}
#print(root_dict)

with open('vis_dict_test.json', 'w') as f:
    #json.dump(root_dict, f, indent=4, ensure_ascii=False)
    json.dump(root_root, f, indent=4, ensure_ascii=False)


def dig_deep(root_key):
    root_rels = rutez.sinsets[root_key]['relations']
    #root_sins = rutez.sinsets[root_key]['words']
    d = {"name": root_key, "children": [dig_deep(rel[1]) for rel in root_rels if rel[0] == "НИЖЕ"]}
    if not d["children"]:
        del d["children"]
    #for rel in root_rels:
    #    if rel[0] == "НИЖЕ":
    #        d["name"] = rel[1]
    #        d["children"].append(dig_deep(rel[1]))

    return d
            #d = {"name": rel[1], "children": [dig_deep(rel[1])]}
            #return d

    #if root_sins:
    #    d["Synonyms"] = root_sins

    #return d
root_graph = {"name": "Rutez", "children": [dig_deep(root) for root in roots]}



#root_graph_ = {dig_deep(root) for root in roots}

#root_graph = {"name": "Root", "children": root_graph_}

with open('rutez_graph.json', 'w') as f:
    json.dump(root_graph, f, indent=4, ensure_ascii=False)

"""
{
 "name": "Root",
 "children": [
  {
   "name": "analytics",
   "children": [
    {
     "name": "cluster",
     "children": [
      {"name": "AgglomerativeCluster", "size": 3938},
      {"name": "CommunityStructure", "size": 3812},
      {"name": "HierarchicalCluster", "size": 6714},
      {"name": "MergeEdge", "size": 743}
     ]
    },
    {
     "name": "graph",
     "children": [
      {"name": "BetweennessCentrality", "size": 3534},
      {"name": "LinkDistance", "size": 5731},
      {"name": "MaxFlowMinCut", "size": 7840},
      {"name": "ShortestPaths", "size": 5914},
      {"name": "SpanningTree", "size": 3416}
     ]
    },
    {
     "name": "optimization",
     "children": [
      {"name": "AspectRatioBanker", "size": 7074}
     ]
    }
   ]
  }
 ]
}
"""
