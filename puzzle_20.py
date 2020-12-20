#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 22:55:09 2020

@author: llnilschwein
"""

import numpy as np

# %%read data
with open('input_20.txt','r') as f:
    data = f.read().split('\n\n')
data.pop()

# %% organize data
tiles_dict = {}
for tile in data:
    header , signal = tile.split(':\n') 
    signal_list =[]
    for signal_line in signal.split('\n'):
        signal_list.append(list(signal_line.replace('.','0').replace('#','1')))  
    tiles_dict[int(header.split()[1])] = np.array(signal_list).astype('int')
  
# %% define functions 

def get_edges(M):
    e0 = M[0,:]
    e1 = M[:,0]
    e2 = M[-1,:]
    e3 = M[:,-1]
    e4 = np.flip(M[0,:])
    e5 = np.flip(M[:,0])
    e6 = np.flip(M[-1,:])
    e7 = np.flip(M[:,-1])
    edges = np.array([e0,e1,e2,e3,e4,e5,e6,e7])
    return edges

def match_edge(edge,M):
    edges = get_edges(M)
    L =(edge == edges).all(axis =1)
    matching_edge = np.where(L)[0]
    return matching_edge

# %%  find neighborcells
matches_dict = {}

for key, value in tiles_dict.items():
    matches_dict[key] = [[],[],[]]
    edges = get_edges(value)
    for k in range(4):
        for key2, value2 in tiles_dict.items():
            if key != key2:
                matching_edges = match_edge(edges[k,:],value2)
                if matching_edges.size !=0:
                    matches_dict[key][0].append(k)
                    matches_dict[key][1].append(matching_edges)
                    matches_dict[key][2].append(key2)
            
# %% find corner pieces and multiply IDs
x = 1
for y,k in matches_dict.items():
    if len(k[2])==2:
        print(y)
        x*=y
print('The answer for part 1 is %i'%x)

# %% assembling whole thing for part2
# first tile is 3229 placed in bottom left corner

picture = np.zeros((120,120))

picture[-10:,:10] = tiles_dict[3229]

