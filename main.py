import networkx as nx


class Maze:
    def __init__(self, file):
        self.file = file
        self.data = []
        self.create_maze_array()
        self.print_maze()

    def create_maze_array(self):
        file = open(self.file, 'r')
        maze_array = []
        for line in file:
            line = line.strip()
            items = line.split(" ")
            maze_array.append(items)
        self.data = maze_array

    def print_maze(self):
        print("--------------------- Matrix --------------------")
        for index1, row in enumerate(self.data):
            row_string = ""
            prv_str = ""
            for index2, item in enumerate(row):
                if not item == '0':
                    if prv_str == "" or prv_str == '1':
                        row_string += item + "       "
                    else:
                        row_string += "   " + item + "       "
                    prv_str = '1'
                else:
                    if prv_str == "" or prv_str == 'tuple':
                        row_string += "(" + str(index1) + ", " + str(index2) + ")  "
                    else:
                        row_string = row_string[:-3]
                        row_string += "(" + str(index1) + ", " + str(index2) + ")  "
                    prv_str = 'tuple'
            row_string = row_string[:-2]
            row_string += ""
            print(row_string)


class Graph:
    def __init__(self, maze_array, start, end):
        self.maze_array = maze_array
        self.weight = 1
        self.start_node = None
        self.end_node = None
        self.graph = nx.Graph()
        self.create_graph(start, end)
        self.print_graph()

    def create_graph(self, start, end):
        graph = nx.Graph()
        for r_index, row in enumerate(self.maze_array):
            for c_index, col in enumerate(row):
                item_index = r_index * len(row) + c_index
                # add nodes to graph
                graph.add_node(item_index, pos=(r_index, c_index), data=col)
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

    def print_graph(self):
        print("--------------------- Graph ---------------------")
        for node in self.graph.nodes:
            edges = self.graph.edges(node)
            if len(edges) == 0:
                continue
            line_string = ""
            for index, edge in enumerate(edges):
                if index == 0:
                    if edge[0] == self.start_node or edge[0] == self.end_node:
                        line_string += str(self.graph.nodes[edge[0]]['data']) + " --> " + str(self.graph.nodes[edge[1]]['pos']) + ", "
                    else:
                        line_string += str(self.graph.nodes[edge[0]]['pos']) + " --> " + str(self.graph.nodes[edge[1]]['pos']) + ", "
                else:
                    line_string += str(self.graph.nodes[edge[1]]['pos']) + ", "
            print(line_string[:-2])


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


class Algorithm:
    def __init__(self, G):
        self.G = G
        self.graph = G.graph
        self.start_node = G.start_node
        self.end_node = G.end_node
        self.search()

    def return_path(self, item_node):
        path = []
        current = item_node
        while current is not None:
            path.append(current)
            current = current.parent
        path = path[::-1]
        print("--------------- A star search path --------------")
        print_string = ""
        for i in range(len(path)):
            p_item = path[i]
            if i == 0 or i == len(path) - 1:
                print_string += str(self.graph.nodes[p_item.node]['data']) + " --> "
            else:
                print_string += str(self.graph.nodes[p_item.node]['pos']) + " --> "
        print(print_string[:-5])

    def get_children(self, item_node):
        res_nodes = []
        connected_edges = self.graph.edges(item_node.node)
        for edge in connected_edges:
            if not edge[0] == item_node.node:
                res_nodes.append(Node(item_node, edge[0], self.graph.nodes[edge[0]]['pos']))
            if not edge[1] == item_node.node:
                res_nodes.append(Node(item_node, edge[1], self.graph.nodes[edge[1]]['pos']))
            # if edge[0] < item_node.node or edge[1] < item_node.node:
            #     continue
            # if edge[0] > item_node.node:
            #     res_nodes.append(Node(item_node, edge[0], self.graph.nodes[edge[0]]['pos']))
            # elif edge[1] > item_node.node:
            #     res_nodes.append(Node(item_node, edge[1], self.graph.nodes[edge[1]]['pos']))
        return res_nodes

    def search(self):
        start_node = Node(None, self.start_node, self.graph.nodes[self.start_node]['pos'])
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, self.start_node, self.graph.nodes[self.end_node]['pos'])
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
                child.g = current_node.g + self.G.weight
                # select one child from eucledian distance
                # child.h = (((child.pos[0] - end_node.pos[0]) ** 2) + ((child.pos[1] - end_node.pos[1]) ** 2))
                child.h = abs(child.pos[0] - end_node.pos[0]) + abs(child.pos[1] - end_node.pos[1])
                child.f = child.g + child.h
                # Child is already in the open_list and g cost is already lower
                if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                    continue
                open_list.append(child)


if __name__ == '__main__':
    M = Maze('input1.txt')
    G = Graph(M.data, '3', '2')
    A = Algorithm(G)
