#!/usr/bin/env python
import os, sys
import networkx as nx


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
