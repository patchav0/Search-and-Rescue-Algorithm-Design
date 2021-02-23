# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 12:25:26 2021

@author: Bryan Van Scoy
"""


import math
import random
import numpy as np
import shapely.geometry
from perlin_noise import PerlinNoise


def scenario(name, size=(100,100)):
    '''Generate a random scenario
    
    Valid scenario names are 'maze', 'polyworld', and 'terrain'.
    '''
    
    if name == 'maze':
        grid, start, goal = random_maze(size[0], size[1])
        
        return grid, start, goal
    
    elif name == 'polyworld':
        polygons, start, goal = random_polygons(size[0], size[1], num_poly=5)
        
        return polygons, start, goal
    
    elif name == 'terrain':
        grid, start, goal = random_terrain(size[0], size[1])

        return grid, start, goal
    
    else:
        raise NameError('unknown scenario: %s' % name )


def random_maze(height, width=None):
    '''Generate a random maze
    
    Uses depth-first search to construct a random maze as in
    http://rosettacode.org/wiki/Maze_generation
    
    Returns a matrix of size (2*height+1, 2*width+1) where "0"
    corresponds to a path and "1" corresponds to a wall
    '''
    
    if width == None: width = height
    
    # constants
    PATH       = 0
    WALL       = 1
    NotVISITED = 2
    VISITED    = 3
    
    # dimension of matrix
    n = 2*width+3
    m = 2*height+3
    
    # offsets of neighboring cells (in linear coordinates)
    offsets = np.array([-1,n,1,-n])
    
    # initialize maze matrix
    maze = NotVISITED * np.ones( (m,n) )
    maze[ np.r_[0,1:m:2,m-1], : ] = WALL
    maze[ :, np.r_[0,1:n:2,n-1] ] = WALL
    
    maze = maze.flatten()  # row-major
    
    # start position (top-left corner)
    current_cell = 2*n+2
    
    # mark the current cell as VISITED
    maze[current_cell] = VISITED
    
    # list of VISITED cells that have NotVISITED neighbors
    S = [current_cell]
    
    # loop until all cells are VISITED
    while S:
        
        # get the neighboring cells that are NotVISITED
        unvisitedNeigbors = offsets[maze[current_cell+2*offsets] == NotVISITED]
        
        # if there are NotVISITED neighboring cells
        if unvisitedNeigbors.any():
            
            # index of a random neighbor that is NotVISITED
            offset = np.random.choice(unvisitedNeigbors)
            
            # the neighboring cell
            new_cell = current_cell + 2*offset
            
            # remove the wall between the current cell and its neighbor
            maze[current_cell + offset] = PATH
            
            # if the neighbor has any NotVISITED neighbors, add it to the list
            if (maze[new_cell+2*offsets] == NotVISITED).any():
                S.append(new_cell)
            
            # set the new cell as the current cell
            current_cell = new_cell
            
            # label the current cell as VISITED
            maze[current_cell] = VISITED
            
        # if all neighboring cells are VISITED
        else:
        
            # set the current cell as the first cell in the list, and remove it from the list
            current_cell = S.pop(0)
    
    # set VISITED to PATH
    maze[maze==VISITED] = PATH
    
    # reshape back to a matrix
    maze = np.reshape(maze, (m,n))
    
    # trim the extra outside wall
    maze  = maze[1:m-1,1:n-1]
    
    start = (1,1)
    goal  = (m-4,n-4)
    
    return maze, start, goal


def random_polygon(center, aveRadius, bounds, irregularity, spikeyness, maxVerts):
    '''Generate a random polygon
    
    Start with the center of the polygon, then creates the polygon
    by sampling points on a circle around the center. Randon noise
    is added by varying the angular spacing between sequential points,
    and by varying the radial distance of each point from the center.
    
    Params:
    center       - coordinates of the polygon center
    aveRadius    - the average radius in pixels
    irregularity - [0,1] variance in angles
    spikeyness   - [0,1] variance in radius
    numVerts     - maximum number of vertices
    
    Returns a shapely.geometry.Polygon object
    '''
    
    numVerts = 3 + random.randrange(maxVerts-3)
    irregularity = clip(irregularity, 0, 1) * 2*math.pi / numVerts
    spikeyness = clip(spikeyness, 0, 1) * aveRadius

    # generate n angle steps
    angleSteps = []
    lower = (2*math.pi / numVerts) - irregularity
    upper = (2*math.pi / numVerts) + irregularity
    
    for i in range(numVerts):
        tmp = random.uniform(lower, upper)
        angleSteps.append(tmp)

    # normalize the steps so that point 0 and point n+1 are the same
    for i in range(numVerts):
        angleSteps[i] *= (2*math.pi) / sum(angleSteps)

    # now generate the points
    points = []
    angle = random.uniform(0, 2*math.pi)
    for i in range(numVerts):
        r = clip( random.gauss(aveRadius, spikeyness), 0, 2*aveRadius )
        x = center[0] + r*math.cos(angle)
        y = center[1] + r*math.sin(angle)
        points.append( (clip(int(x),bounds[0],bounds[2]), clip(int(y),bounds[1],bounds[3])) )

        angle += angleSteps[i]

    return shapely.geometry.Polygon(points)


def random_polygons(height, width=None, num_poly=5):
    '''Generate a random set of polygons
    
    Returns an array of shapely.geometry.Polygon objects
    
    See environment.random_polygon
    '''
    
    if width == None: width = height
    
    polygons = []
    rr = min(width, height)
    
    for k in range(num_poly):
        r = rr/5 + random.randrange(rr/5)
        c = (random.randrange(width), random.randrange(height))
        polygons.append( random_polygon( center=c, aveRadius=r, bounds=(1,1,width-2,height-2), irregularity=0.25, spikeyness=0.2, maxVerts=6 ) )
    
    start = (0,0)
    goal  = (height-1,width-1)
    
    return polygons, start, goal


def random_terrain(height, width=None):
    '''Generate a random terrain
    
    Returns a matrix of size (height, width), where the value of each
    grid point is determined using Perlin noise.
    '''
    
    if width == None: width = height
    
    noise = PerlinNoise(octaves=10)
    grid  = np.matrix([[ noise([i/height,j/width]) for j in range(width)] for i in range(height)])
    grid  = ( grid - grid.min() ) / ( grid.max() - grid.min() )
    start = (0,0)
    goal  = (height-1,width-1)
    
    return grid, start, goal
    
    
def clip(x, a, b):
    '''Clip x to the interval [a,b]'''
    
    if   a > b : return x
    elif x < a : return a
    elif x > b : return b
    else       : return x