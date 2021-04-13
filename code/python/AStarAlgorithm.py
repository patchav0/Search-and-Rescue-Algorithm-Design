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


class AStarAlgorithm:
    def __init__(self, graph, positions):
        self.graph = graph
        self.positions = positions
        self.start_node = len(graph.nodes) - 2
        self.end_node = len(graph.nodes) - 1
        self.weight = 1
        self.search()

    def display(self):
        print(self.graph.nodes)
        print(self.start_node)
        print(self.end_node)
        print(self.graph.edges)

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
                child.g = current_node.g + self.weight
                child.h = abs(child.pos[0] - end_node.pos[0]) + abs(child.pos[1] - end_node.pos[1])
                child.f = child.g + child.h
                # Child is already in the open_list and g cost is already lower
                if len([i for i in open_list if child == i and child.g > i.g]) > 0:
                    continue
                open_list.append(child)
