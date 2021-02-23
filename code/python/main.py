# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:25:26 2021

@author: Bryan Van Scoy
"""


import matplotlib.pyplot as plt
import descartes

from environment import scenario
from simulation import plot_endpoints


if __name__ == '__main__':
    
    size = (50,100)
    
    ###########################################################################
    # MAZE
    ###########################################################################
    grid, start, goal = scenario('maze', size)
    
    fig, ax = plt.subplots(1, 1)
    
    plt.imshow(grid, cmap='Greys', origin='lower')
    
    plot_endpoints(ax, start, goal)
    
    plt.axis('off')
    # plt.savefig('maze.pdf', bbox_inches='tight', pad_inches=0, dpi=600)
    plt.show()
    
    
    ###########################################################################
    # POLYGON WORLD
    ###########################################################################
    polygons, start, goal = scenario('polyworld', size)
    
    fig, ax = plt.subplots(1, 1)
    
    for poly in polygons:
        ax.add_patch(descartes.PolygonPatch(poly, fc='blue', alpha=0.5))
    
    plot_endpoints(ax, start, goal)
    
    fig.set_facecolor('white')
    fig.set_edgecolor('white')
    plt.axis('off')
    # plt.savefig('polyworld.pdf', bbox_inches='tight', pad_inches=0, dpi=600, facecolor='white', edgecolor='white')
    plt.show()
    
    
    ###########################################################################
    # TERRAIN
    ###########################################################################
    grid, start, goal = scenario('terrain', size)
    
    fig, ax = plt.subplots(1, 1)
    
    plt.imshow(grid, cmap='jet', origin='lower')
    
    plot_endpoints(ax, start, goal)
    
    plt.axis('off')
    # plt.savefig('terrain.pdf', bbox_inches='tight', pad_inches=0, dpi=600)
    plt.show()