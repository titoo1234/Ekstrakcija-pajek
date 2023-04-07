import random
import psycopg2
import os
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx


def baza():
    return psycopg2.connect(host="localhost", user="user", password="SecretPassword")

conn = baza()

def dobi_page_type():
    '''
        pridobi iz tabele page stevilo strani ki so vrste HTML, BINARY, DUPLICATE...
    '''
    cur = conn.cursor()
    cur.execute("select count(*), page_type_code from crawldb.page group by page_type_code")
    return cur.fetchall()


def dobi_content_type():
    '''
        pridobi iz tabele page stevilo strani ki so vrste HTML, BINARY, DUPLICATE...
    '''
    cur = conn.cursor()
    cur.execute("select count(*),content_type from crawldb.image group by content_type order by count(*) desc;")
    return cur.fetchall()


def dobi_page_data():
    '''
        pridobi iz tabele page stevilo strani ki so vrste HTML, BINARY, DUPLICATE...
    '''
    cur = conn.cursor()
    cur.execute("select count(*),data_type_code from crawldb.page_data group by data_type_code order by count(*) desc;")
    return cur.fetchall()

def dobi_linke_otlinki():
    '''
        za linke z največ outlinki
    '''
    cur = conn.cursor()
    cur.execute("""
                SELECT from_page, to_page
            FROM crawldb.link
            WHERE from_page IN (
                SELECT from_page
                FROM crawldb.link
                GROUP BY from_page
                HAVING COUNT(*) > 200
            );
            """)
    return cur.fetchall()
    
def dobi_linke_inlinki():
    '''
        za linke z največ inlinki
    '''
    cur = conn.cursor()
    cur.execute("""SELECT from_page,to_page
            FROM crawldb.link
            WHERE to_page IN (
                SELECT to_page
                FROM crawldb.link
                GROUP BY to_page
                HAVING COUNT(*) = 2
            );""")
    return cur.fetchall()
def dobi_linke():
    '''
        vsi linki
    '''
    cur = conn.cursor()
    cur.execute("select * from crawldb.link;")
    return cur.fetchall()

def graf_omrezje_nakljucno():
    G = nx.DiGraph()
    sampled_links = dobi_linke()
    sampled_links = random.sample(sampled_links, 300)
    # add nodes
    nodes = set()
    for link in sampled_links:
        nodes.add(link[0])
        nodes.add(link[1])
    G.add_nodes_from(nodes)

    # add edges
    G.add_edges_from(sampled_links)
    nx.draw(G, with_labels=False, node_color='orange', edge_color='red',width = 1.0, node_size=40)
    plt.show()
    
    
def graf_omrezje_outlinki():
    G = nx.DiGraph()
    sampled_links = dobi_linke_otlinki()
    sampled_links = random.sample(sampled_links, 300)
    # add nodes
    nodes = set()
    for link in sampled_links:
        nodes.add(link[0])
        nodes.add(link[1])
    G.add_nodes_from(nodes)

    # add edges
    G.add_edges_from(sampled_links)
    nx.draw(G, with_labels=False, node_color='orange', edge_color='red',width = 1.0, node_size=40)
    plt.show()
    
def graf_omrezje_inlinki():
    G = nx.DiGraph()
    sampled_links = dobi_linke_inlinki()
    sampled_links = random.sample(sampled_links, 300)
    # add nodes
    nodes = set()
    for link in sampled_links:
        nodes.add(link[0])
        nodes.add(link[1])
    G.add_nodes_from(nodes)

    # add edges
    G.add_edges_from(sampled_links)
    nx.draw(G, with_labels=False, node_color='orange', edge_color='red',width = 1.0, node_size=40)
    plt.show()    
    
def uredi(t):
    '''
        dobi tabelo z vrednostmi (x, y) in vrne dve tabeli x in y
    '''
    a = []
    b = []
    for tup in t:
        a.append(tup[0])
        b.append(tup[1])
    return a,b


def pita(vr,labels):
    fig, ax = plt.subplots()
    #ax.pie(vr, labels=labels,autopct="f%")
    ax.pie(vr, labels=labels,autopct='%1.1f%%')
    plt.show()
    
    
#PITA 1
    
# vr = dobi_page_type()
# vr = uredi(vr)
# pita(vr[0], vr[1])



#graf_omrezje_nakljucno()
#graf_omrezje_outlinki()
#graf_omrezje_inlinki()


#PITA 2

# vr = dobi_content_type()
# vr = uredi(vr)
# pita(vr[0], vr[1])


#PITA 3

# vr = dobi_page_data()
# vr = uredi(vr)
# pita(vr[0], vr[1])
    
    
    
