# Built off of Dr. Van Scoys environment generating main method.
# Important Methods: 
# AStarAlgorithm: Takes a graph and a list of coordinates
# corresponding to its nodes, and finds the optimal path
# polyWorldToGraph: Takes a multipolygon object, the size of 
# the environment and a start and goal position, creates a graph

import matplotlib.pyplot as plt
import descartes
import numpy as np 
import triangle as tr
import networkx as nx

from environment import scenario
from simulation import plot_endpoints
from shapely.ops import unary_union
from shapely.geometry import LineString

class Node:
    def __init__(self, parent=None, node=None, pos=None):
        self.parent = parent
        self.node = node
        self.pos = pos
        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.pos == other.pos


class WeightedAStarAlgorithm:
    def __init__(self, graph, positions):
        self.graph = graph
        self.positions = positions
        self.start_node = len(graph.nodes) - 2
        self.end_node = len(graph.nodes) - 1
        self.path = []
        # self.display()
        self.search()

    def display(self):
        print(self.graph.nodes)
        print(self.start_node)
        print(self.end_node)

    def return_path(self, item_node):
        current = item_node
        while current is not None:
            self.path.append(current)
            current = current.parent
        self.path = self.path[::-1]
        print("--------------- A star search path --------------")
        print_string = ""
        for i in range(len(self.path)):
            p_item = self.path[i]
            print_string += str(p_item.node) + " --> "
            # if i == 0 or i == len(path) - 1:
            #     print_string += str(p_item.node) + " --> "
            # else:
            #     print_string += str(p_item.pos) + " --> "
        print(print_string[:-5])

    def get_children(self, item_node):
        res_nodes = []
        connected_edges = self.graph.edges(item_node.node)
        for edge in connected_edges:
            if not edge[0] == item_node.node:
                res_nodes.append(Node(item_node, edge[0], self.positions[edge[0]]))
            if not edge[1] == item_node.node:
                res_nodes.append(Node(item_node, edge[1], self.positions[edge[1]]))
        return res_nodes

    def search(self):
        start_node = Node(None, self.start_node, self.positions[self.start_node])
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.end_node, self.positions[self.end_node])
        end_node.g = end_node.h = end_node.f = 0
        open_list = []
        close_list = []
        open_list.append(start_node)
        outer_iterations = 0
        max_iterations = 1000
        # loop until you get the target
        while len(open_list) > 0:
            # Every time any node is referred from open_list
            outer_iterations += 1
            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index
            # if path is greater than max_iterations, stop search
            if outer_iterations > max_iterations:
                print("Too many iterations for given start, end")
                return self.return_path(current_node)
            # Pop current node out off yet_to_visit list, add to visited list
            open_list.pop(current_index)
            close_list.append(current_node)
            # test if goal is reached or not, if yes then return the path
            if current_node == end_node:
                return self.return_path(current_node)
            children = self.get_children(current_node)
            # Loop through children
            for child in children:
                # Child is on the visited list (search entire visited list)
                if len([close_item for close_item in close_list if close_item == child]) > 0:
                    continue
                # Create the f, g, and h values
                child.g = current_node.g + self.graph.edges[current_node.node, child.node]['weight']
                child.h = abs(child.pos[0] - end_node.pos[0]) + abs(child.pos[1] - end_node.pos[1])
                child.f = child.g + child.h
                # Child is already in the open_list and g cost is already lower
                if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                    continue
                open_list.append(child)
                
class Maze:
    def __init__(self, grid, size):
        self.data = grid
        self.rows = size[0]
        self.cols = size[1]


class Graph:
    def __init__(self, M, start, end):
        self.rows = M.rows
        self.cols = M.cols
        self.maze_array = M.data
        self.weight = 1
        self.start_node = None
        self.end_node = None
        self.graph = nx.Graph()
        ####################
        self.positions = {}
        ####################
        self.create_graph(start, end)

    def create_graph(self, start, end):
        graph = nx.Graph()
        for r_index, row in enumerate(self.maze_array):
            for c_index, col in enumerate(row):
                item_index = r_index * len(row) + c_index
                # add nodes to graph
                graph.add_node(item_index, pos=(r_index, c_index), data=col)
                ############################################
                self.positions[item_index] = [r_index, c_index]
                ###########################################
                if col == start:
                    self.start_node = item_index
                if col == end:
                    self.end_node = item_index
                # add edges to graph
                if col == '1':
                    continue
                if r_index == 1 and c_index == 0:
                    continue
                _up = r_index - 1
                _left = c_index - 1
                if _up > 0 and self.maze_array[_up][c_index] != '1':
                    _up_index = _up * len(row) + c_index
                    graph.add_edge(_up_index, item_index, weight=self.weight)
                if _left > 0 and self.maze_array[r_index][_left] != '1':
                    _left_index = r_index * len(row) + _left
                    graph.add_edge(_left_index, item_index, weight=self.weight)
        self.graph = graph
        return graph



class polyworldToGraph:
    def __init__(self, polygons, size, start, goal):
        self.polygons = polygons
        self.ylen = size[0]
        self.xlen = size[1]
        self.start = list(start)
        self.goal = list(goal)
        self.nodes = {}
        self.graph = self.createGraph()
    
       
    def createGraph(self):
        
        def checkCollision(A, B, C, D):
            line1 = LineString([A,B])
            line2 = LineString([C,D])
            return line1.crosses(line2)
            

        G = nx.Graph()
        holes = np.empty((len(polygons),2), dtype=int)
        corners = np.empty((100,2), dtype=int) 
        f = 0;
        for k in range(len(polygons)):
            # store holes in array
            point = polygons[k].centroid
            holes[k] = [point.x, point.y]
      
            # add each verticy in an array and dictionary
            vertices = list(polygons[k].exterior.coords)
            vertices = np.array(tuple(tuple(map(int, x)) for x in vertices))
            for j in range(len(vertices)-1):
                c = vertices[j];
                corners[f] = c
                f += 1  
        
        # add corners of environment boundaries
        expansionx = 0 * self.xlen
        expansiony = 0 * self.ylen
        corners[f] = [0 - expansionx, 0 - expansiony]
        f += 1
        corners[f] = [self.xlen + expansionx, 0 - expansiony]
        f += 1
        corners[f] = [self.xlen + expansionx, self.ylen + expansiony]
        f += 1
        corners[f] = [0 - expansionx, self.ylen + expansiony]
        f += 1
        corners = corners[0:f,:]
        
        # store segments in array
        segments = np.empty((100,2), dtype=int)
        g = 0
        for h in range(len(polygons)):
            vertices = list(polygons[h].exterior.coords)
            vertices = np.array(tuple(tuple(map(int, x)) for x in vertices))
            for n in range(len(vertices)-1):
                c = [vertices[n][0],vertices[n][1]]
                c2 = [vertices[n+1][0],vertices[n+1][1]]
                ind1 = corners.tolist().index(c)
                ind2 = corners.tolist().index(c2)
                segments[g] = [ind1, ind2]
                g += 1
        # add walls of environment
        segments[g] = [f-4, f-3]
        g += 1
        segments[g] = [f-3, f-2]
        g += 1
        segments[g] = [f-2, f-1]
        g += 1
        segments[g] = [f-1, f-4]
        g += 1
        segments = segments[0:g,:]
        
        # Create Dictionary  
        poly = {'holes': holes,
                'vertices': corners,
                'segments': segments} 
        t = tr.triangulate(poly, 'pc')
        
        triList = t['triangles'];
        corners = t['vertices'];
        triGraph = {}
        
        # find and plot centers of triangles (remember nodes closest to start and goal )
        startNodeIndex = 0
        sVal = self.xlen
        goalNodeIndex = 0
        gVal = self.xlen
        
        for q in range(len(triList)):
            # coordinate of the vertices  
            vert1 = corners[triList[q][0]]
            vert2 = corners[triList[q][1]]
            vert3 = corners[triList[q][2]]
            # calculate centroid  
            x = np.uint8((vert1[0] + vert2[0] + vert3[0]) / 3)
            y = np.uint8((vert1[1] + vert2[1] + vert3[1]) / 3)
            # store in a node dictionary
            self.nodes[q] = [x, y]
            #find closest nodes to start and end 
            temp = np.linalg.norm(np.array([goal[1],goal[0]])-np.array([x,y]))
            if temp < gVal:
                gVal = temp;
                goalNodeIndex = q
            temp = np.linalg.norm(np.array(start)-np.array([x,y]))
            if temp < sVal:
                sVal = temp;
                startNodeIndex = q
                
        # if any of the previous nodes share 2 verticies
        # add them to the dictionary
        for d in range(len(self.nodes)):
            vert1 = triList[d][0]
            vert2 = triList[d][1]
            vert3 = triList[d][2]
            for b in range(len(self.nodes)):
                verta = triList[b][0]
                vertb = triList[b][1]
                vertc = triList[b][2]
                count = 0;
                if np.any([verta == vert1, verta == vert2, verta == vert3]):
                    count += 1
                if np.any([vertb == vert1, vertb == vert2, vertb == vert3]):
                    count += 1
                if np.any([vertc == vert1, vertc == vert2, vertc == vert3]):
                    count += 1
                    
                if count == 2:
                    if d in triGraph:
                        triGraph[d] = [*triGraph[d], b]
                        G.add_node(d)
                    else:
                        triGraph[d] = [b];
                        G.add_node(d)
                        
        fig, ax = plt.subplots(1, 1)
        # plot nodes and edges of graph              
        for u in triGraph:
            uCoords = self.nodes[u]
            for v in range(len(triGraph[u])):
                vCoords = self.nodes[triGraph[u][v]]
                #check each connection for collision
                flag = 1
                for i in range(len(segments)):
                    
                    aCoords = corners[segments[i][0]]
                    bCoords = corners[segments[i][1]]
                    collision = checkCollision(uCoords, vCoords, aCoords, bCoords) 
                    if collision:
                        flag = 0
                        #find coordinates of closest vertice
                        dist1 = np.linalg.norm(np.array(uCoords)-np.array(aCoords)) + np.linalg.norm(np.array(vCoords)-np.array(aCoords))
                        dist2 = np.linalg.norm(np.array(uCoords)-np.array(bCoords)) + np.linalg.norm(np.array(vCoords)-np.array(bCoords))
                        
                        if (dist1 < dist2):
                            closestVerticeCoords = aCoords
                        else: 
                            closestVerticeCoords = bCoords
                             
                # # plot and add edge 
                if flag:
                    plt.plot([self.nodes[u][0],self.nodes[triGraph[u][v]][0]],[self.nodes[u][1],self.nodes[triGraph[u][v]][1]], 'ko-') 
                    wt = np.linalg.norm(np.array(uCoords)-np.array(vCoords))
                    G.add_edge(triGraph[u][v], u, weight=wt)
                  
                # connect edges to closest vertice if collision occurs
                else:
                    # add node 
                    self.nodes[len(self.nodes)] = list(closestVerticeCoords)
                    G.add_node(len(self.nodes)-1)
                    # plot and add edges
                    plt.plot([self.nodes[u][0],closestVerticeCoords[0]],[self.nodes[u][1], closestVerticeCoords[1]], 'ko-')
                    wt = np.linalg.norm(np.array(uCoords)-np.array(closestVerticeCoords))
                    G.add_edge(u, len(self.nodes)-1, weight=wt)
                    plt.plot([self.nodes[triGraph[u][v]][0],closestVerticeCoords[0]],[self.nodes[triGraph[u][v]][1], closestVerticeCoords[1]], 'ko-')
                    wt = np.linalg.norm(np.array(vCoords)-np.array(closestVerticeCoords))
                    G.add_edge(len(self.nodes)-1,triGraph[u][v],  weight=wt)
                               
        # add start and end points 
        self.nodes[len(self.nodes)] = list(start)
        self.nodes[len(self.nodes)] = list([goal[1],goal[0]])
        triGraph[len(triGraph)] = [startNodeIndex]
        G.add_node(len(triGraph)-1)
        triGraph[len(triGraph)] = [goalNodeIndex]
        G.add_node(len(triGraph)-1)
        G.add_edge(startNodeIndex, len(self.nodes)-2, weight=sVal)
        G.add_edge(goalNodeIndex, len(self.nodes)-1, weight=gVal)

        
                
        #Run A* and plot path
        A = WeightedAStarAlgorithm(G, self.nodes)
        path = A.path
        for i in range(len(path)-1):
            node1 = A.path[i].node
            node2 = A.path[i+1].node
            plt.plot([self.nodes[node1][0],self.nodes[node2][0]],[self.nodes[node1][1],self.nodes[node2][1]], 'yo-')
            

        # add start and end point markers
        for poly in polygons:
            ax.add_patch(descartes.PolygonPatch(poly, fc='blue', alpha=0.5))
        plot_endpoints(ax, start, goal)
        plt.show()
        
        
        return G
    
    
                
if __name__ == '__main__':
    
    size = (50, 100)
    
    ###########################################################################
    # MAZE
    ###########################################################################
    grid, start, goal = scenario('maze', size)

    fig, ax = plt.subplots(1, 1)
    
    plt.imshow(grid, cmap='Greys', origin='lower')
    
    plot_endpoints(ax, start, goal)
    grid[start] = 3
    grid[goal] = 2
    
    plt.axis('off')
    # plt.savefig('maze.pdf', bbox_inches='tight', pad_inches=0, dpi=600)
    #plt.show()
    MG = Graph(Maze(grid, size), '3', '2')
    #AStarAlgorithm(MG.graph, MG.positions)

    
    
    ###########################################################################
    # POLYGON WORLD
    ###########################################################################
    polygons, start, goal = scenario('polyworld', size)
    #combine overlapping polygons
    polygons = unary_union(polygons)
    
    fig, ax = plt.subplots(1, 1)
    
    for poly in polygons:
        ax.add_patch(descartes.PolygonPatch(poly, fc='blue', alpha=0.5))
    
    plot_endpoints(ax, start, goal)
    
    fig.set_facecolor('white')
    fig.set_edgecolor('white')
    plt.axis('on')
    #plt.savefig('polyworld.pdf', bbox_inches='tight', pad_inches=0, dpi=600, facecolor='white', edgecolor='white')
    plt.show()
    
    # CREATE GRAPH AND APPLY A*
    polyGraph = polyworldToGraph(polygons, size, start, goal)
    
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
