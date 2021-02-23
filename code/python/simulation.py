# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:25:26 2021

@author: Bryan Van Scoy
"""


import matplotlib.pyplot as plt

plt.rc('axes', facecolor='black')
plt.rc('axes', edgecolor='black')
plt.rc('figure', facecolor='black')
plt.rc('figure', edgecolor='black')
plt.rc('savefig', facecolor='black')
plt.rc('savefig', edgecolor='black')


def plot_endpoints(ax, start, goal):
    '''Plot the start and goal'''
    
    plt.scatter(start[1], start[0], s=100, c='b', zorder=2)
    plt.scatter( goal[1],  goal[0], s=100, c='r', zorder=2)
    ax.annotate('S', (start[1],start[0]), ha='center', va='center', fontsize=7, color='w', zorder=3)
    ax.annotate('G', ( goal[1], goal[0]), ha='center', va='center', fontsize=7, color='w', zorder=3)
    return None