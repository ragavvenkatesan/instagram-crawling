#!/usr/bin/python

import matplotlib.pyplot as plt
import networkx as nx
import csv
        
def save_graph(graph,file_name):
    
    #initialze Figure
    plt.figure(num=None, figsize=(20, 20), dpi=80)
    plt.axis('off')
    fig = plt.figure(1)
    pos = nx.spring_layout(graph)
    nx.draw(graph,pos)
    
    plt.draw()
    plt.show()

def calculate_degree_centrality(g):
    dc = nx.degree_centrality(g)
    nx.set_node_attributes(g,'degree_cent',dc)
    degcent_sorted = sorted(dc.items(), reverse=True)
    for key, value in degcent_sorted[0:10] :
        print "Highest degree Centrality:",key,value
    return dc

def main():

    G=nx.DiGraph()

    with open('./userdata/edges.csv', 'Ur') as f:
        edges = list(tuple(rec) for rec in csv.reader(f, delimiter=','))

    for edge in edges[1:200]:
            G.add_edge(*edge)

    calculate_degree_centrality(G)

    save_graph(G,'graph.pdf')


if __name__ == '__main__':
    main ()





