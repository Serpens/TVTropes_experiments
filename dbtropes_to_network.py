#!/usr/bin/env python
import os, sys
import networkx as nx
from collections import defaultdict


HAS_FEATURE_PATTERN = '<http://skipforward.net/skipforward/resource/seeder/skipinions/hasFeature>'
COMMON_PREFIX = '<http://dbtropes.org/resource/'


def get_hasfeature_from_file(file_handle):
    result = [i for i in file_handle.readlines() if HAS_FEATURE_PATTERN in i]
    return result


def clean_url(url):
    result = url.replace(COMMON_PREFIX, '')
    result = result.replace('>', '')
    return result


def rstrip_int(str_with_int):
    index = str_with_int.find('int_')
    if index > -1:
        return str_with_int[:(index-1)]
    return str_with_int


def jaccard_index(set1, set2):
    return len(set1.intersection(set2)) / len(set1.union(set2))


if __name__ == '__main__':
    dbtropes_path = sys.argv[1]
    graph_path = sys.argv[2]
    # get trope->media and media-> trope links
    with open(dbtropes_path) as f:
        has_feature_line = get_hasfeature_from_file(f)
    links = [(clean_url(i[0]), rstrip_int(clean_url(i[2]))) \
        for i in [i.split(' ') for i in has_feature_line]]     # i[1] is always HAS_FEATURE_PATTERN, i[2] is always '.\n'
    interesting_links = [i for i in links if \
        (i[0].startswith('Main/') and not i[1].startswith('Main/')) or \
        (not i[0].startswith('Main/') and i[1].startswith('Main/'))]
    node_names = set([i[0] for i in interesting_links] + [i[1] for i in interesting_links])
    # create graph
    G = nx.Graph()
    G.add_nodes_from(node_names)
    G.add_edges_from(interesting_links)
    nx.write_gml(G, graph_path)
    # create trope and media graphs
    trope_names = [i for i in node_names if i.startswith('Main/')]
    media_names = [i for i in node_names if not i.startswith('Main/')]


for t in trope_names:
    media_for_trope[t] = set([m for m in media_names if G.has_edge(t, m)])

for m in media_names:
    tropes_for_media[t] = set([t for t in trope_names if G.has_edge(t, m)])


    G_tropes.add_nodes_from(trope_names)

    for i in enumerate(trope_names):
        for j in enumerate(trope_names):
            if i[0] > j[0]:
                weight = jaccard_index(media_for_trope[i[1]], media_for_trope[j[1]])
                if weight > 0.0:
                    G_tropes.add_edge(i[1], j[1], weight=weight)
