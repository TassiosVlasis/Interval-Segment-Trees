import random


class node:
    def __init__(self, value):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None  # Added For Deletion
        self.height = 1  # Added For AVL


class Interval_Tree:
    def __init__(self):
        self.root = None
        self.lista = []
        self.temp = []
        self.alpha = []
        self.beta = []
        self.charlie = []
        self.delta = []

    
    def __repr__(self):
        if self.root == None:
            return ''
        content = '\n'  # to hold final string
        cur_nodes = [self.root]  # all nodes at current level
        cur_height = self.root.height  # height of nodes at current level
        sep = ' ' * (2**(cur_height - 1))  # variable sized separator between elements
        while True:
            cur_height += -1  # decrement current height
            if len(cur_nodes) == 0:
                break
            cur_row = ' '
            next_row = ''
            next_nodes = []

            if all(n is None for n in cur_nodes):
                break

            for n in cur_nodes:

                if n == None:
                    cur_row += '   ' + sep
                    next_row += '   ' + sep
                    next_nodes.extend([None, None])
                    continue

                if n.value != None:
                    buf = ' ' * int((5 - len(str(n.value))) / 2)
                    cur_row += '%s%s%s' % (buf, str(n.value), buf) + sep
                else:
                    cur_row += ' ' * 5 + sep

                if n.left_child != None:
                    next_nodes.append(n.left_child)
                    next_row += ' /' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

                if n.right_child != None:
                    next_nodes.append(n.right_child)
                    next_row += '\ ' + sep
                else:
                    next_row += '  ' + sep
                    next_nodes.append(None)

            content += (cur_height * '   ' + cur_row + '\n' + cur_height * '   ' + next_row + '\n')
            cur_nodes = next_nodes
            sep = ' ' * int(len(sep) / 2)  # cut separator size in half
        return content

    # Inserting a value

    def insert(self, value):
        if self.root is None:
            self.root = node(value)
            self.lista.append(value)  # list
        else:
            self._my_insert(value, self.root)

    # Private function that deals with functionality issues and easy understanding
    def _my_insert(self, value, current_node):
        if value < current_node.value:
            if current_node.left_child is None:
                current_node.left_child = node(value)
                self.lista.append(value)  # list
                current_node.left_child.parent = current_node  # For deletion
                self._inspect_insertion(current_node.left_child)
            else:
                self._my_insert(value, current_node.left_child)
        elif value > current_node.value:
            if current_node.right_child is None:
                current_node.right_child = node(value)
                self.lista.append(value)  # list
                current_node.right_child.parent = current_node  # For deletion
                self._inspect_insertion(current_node.right_child)
            else:
                self._my_insert(value, current_node.right_child)
        else:
            print("Value already inside the tree")

    # Display the tree
    def print_tree(self):
        if self.root != None:
            self._my_print_tree(self.root)

    def _my_print_tree(self, current_node):
        if current_node != None:
            self._my_print_tree(current_node.left_child)
            print(str(current_node.value))
            self._my_print_tree(current_node.right_child)

    # find the height
    def height(self):
        if self.root != None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, current_node, current_height):
        if current_node == None:
            return current_height
        left_height = self._height(current_node.left_child, current_height + 1)
        right_height = self._height(current_node.right_child, current_height + 1)
        return max(left_height, right_height)

    # Find if a value is in the tree
    def find(self, value):
        if self.root != None:
            return self._find(value, self.root)
        else:
            return None

    def _find(self, value, current_node):
        if value == current_node.value:
            return current_node
        elif value < current_node.value and current_node.left_child != None:
            return self._find(value, current_node.left_child)
        elif value > current_node.value and current_node.right_child != None:
            return self._find(value, current_node.right_child)

    # Function for deleting a node
    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):

        if node == None or self.find(node.value) == None:
            print("Node to be deleted not found in the tree!")
            return None

        def min_value_node(n):
            current = n
            while current.left_child != None:
                current = current.left_child
            return current

        def num_children(n):
            num_children = 0
            if n.left_child != None:
                num_children += 1
            if n.right_child != None:
                num_children += 1
            return num_children

        # Take the parent of the node that is gonna get deleted
        node_parent = node.parent

        # Take the num of children that are gonna get deleted
        node_children = num_children(node)

        # Below with have 3 states.. 0 chil , 1 chil , 2 chil

        # CASE 0 kids
        if node_children == 0:
            if node.parent != None:
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    node_parent.right_child = None
            else:
                self.root = None

        # CASE 1 kid
        if node_children == 1:
                # Look for the kid that is alone
            if node.left_child != None:
                child = node.left_child
            else:
                child = node.right_child

            if node_parent != None:
                # Change the node that is getting deleted with the child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child

            # Confirm parent's node
            child.parent = node_parent

        # CASE 2 Children
        if node_children == 2:

            # Taking the function(min_value_node) for proper selection on deletion
            successor = min_value_node(node.right_child)

            # Choosing the value that i want to delete
            node.value = successor.value

            self.delete_node(successor)

            return

        if node_parent != None:
            node_parent.height = 1 + max(self.get_height(node_parent.left_child), self.get_height(node_parent.right_child))

            self._inspect_deletion(node_parent)

    def search(self, value):
        if self.root != None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, current_node):
        if value == current_node.value:
            return True
        elif value < current_node.value and current_node.left_child != None:
            return self._search(value, current_node.left_child)
        elif value > current_node.value and current_node.right_child != None:
            return self._search(value, current_node.right_child)
        return False

##################### New Function For A General AVL Tree #################

    # A check while insertin a value , for exact positioning
    def _inspect_insertion(self, current_node, path=[]):
        if current_node.parent == None:
            return
        path = [current_node] + path

        left_height = self.get_height(current_node.parent.left_child)
        right_height = self.get_height(current_node.parent.right_child)

        if abs(left_height - right_height) > 1:
            path = [current_node.parent] + path
            self._rebalance_node(path[0], path[1], path[2])
            return

        new_height = 1 + current_node.height
        if new_height > current_node.parent.height:
            current_node.parent.height = new_height

        self._inspect_insertion(current_node.parent, path)

    # Check while deleting the height of the tree in order to get a rebalance if needed
    def _inspect_deletion(self, current_node):
        if current_node == None:
            return

        left_height = self.get_height(current_node.left_child)
        right_height = self.get_height(current_node.right_child)

        if abs(left_height - right_height) > 1:
            y = self.taller_child(current_node)
            x = self.taller_child(y)
            self._rebalance_node(current_node, y, x)

        self._inspect_deletion(current_node.parent)

    # The function for rebalancing the nodes in the tree
    def _rebalance_node(self, z, y, x):
        if y == z.left_child and x == y.left_child:
            self._right_rotate(z)
        elif y == z.left_child and x == y.right_child:
            self._left_rotate(y)
            self._right_rotate(z)
        elif y == z.right_child and x == y.right_child:
            self._left_rotate(z)
        elif y == z.right_child and x == y.left_child:
            self._right_rotate(y)
            self._left_rotate(z)
        else:
            raise Exception('_rebalance_node: z,y,x node configuration not recognized!')

    def _right_rotate(self, z):
        sub_root = z.parent
        y = z.left_child
        t3 = y.right_child
        y.right_child = z
        z.parent = y
        z.left_child = t3
        if t3 != None:
            t3.parent = z
        y.parent = sub_root
        if y.parent == None:
            self.root = y
        else:
            if y.parent.left_child == z:
                y.parent.left_child = y
            else:
                y.parent.right_child = y
        z.height = 1 + max(self.get_height(z.left_child),
                           self.get_height(z.right_child))
        y.height = 1 + max(self.get_height(y.left_child),
                           self.get_height(y.right_child))

    def _left_rotate(self, z):
        sub_root = z.parent
        y = z.right_child
        t2 = y.left_child
        y.left_child = z
        z.parent = y
        z.right_child = t2
        if t2 != None:
            t2.parent = z
        y.parent = sub_root
        if y.parent == None:
            self.root = y
        else:
            if y.parent.left_child == z:
                y.parent.left_child = y
            else:
                y.parent.right_child = y
        z.height = 1 + max(self.get_height(z.left_child),
                           self.get_height(z.right_child))
        y.height = 1 + max(self.get_height(y.left_child),
                           self.get_height(y.right_child))

    #  Get the height of the value and use it for the rebalance
    def get_height(self, current_node):
        if current_node == None:
            return 0
        return current_node.height

    # Which kid is taller of the iven value
    def taller_child(self, current_node):
        left = self.get_height(current_node.left_child)
        right = self.get_height(current_node.right_child)
        return current_node.left_child if left >= right else current_node.right_child


###################  Special Functions For Interval-Segment Trees ##########################

    # Searching all the intervals that are contained in the value i give
    def search_contains(self, value):
        for item in self.lista:
            if value[0] <= item[0] and value[1] >= item[1]:
                self.temp.append(item)
        return self.temp

    # Returns the intervals that contain the value i give
    def search_is_contained(self, value):
        for item in self.lista:
            if value[0] >= item[0] and value[1] <= item[1]:
                self.alpha.append(item)
        return self.alpha

    # Returns the intervals that they have at least one common point with the value i give on the left
    def left_search(self, value):
        for item in self.lista:
            if value[0] > item[0] and value[1] > item[1] and value[0] <= item[1]:
                self.beta.append(item)
        return self.beta

    # Returns the intervals that they have at least one common point with the value i give on the right
    def right_search(self, value):
        for item in self.lista:
            if value[0] < item[0] and value[1] < item[1] and value[1] >= item[0]:
                self.charlie.append(item)
        return self.charlie

    def stabbing_query(self, value):
        for item in self.lista:
            if value <= item[1] and value >= item[0]:
                self.delta.append(item)
        return self.delta

################# Code To Run ######################


tree = Interval_Tree()

#list = []

#res = random.sample(range(0, 50), 10)

#for num in res:
    #list.append([num, num * 2])
    #list.append([num,random.randrange(50,100),1]) # Here a second version of creating
# print(list)


#for temp in list:
    #tree.insert(temp)

#tree.insert([0, 2])
#tree.insert([1, 3])
#tree.insert([5, 10])
#tree.insert([6, 20])
#tree.insert([4, 5])
#tree.insert([1, 5])


#tree.print_tree()

#print("Height is: " + str(tree.height()))

#print(tree.search([0, 2]))

#tree.delete_value([0, 2])
# tree.print_tree()

print(tree.search_contains([0, 10]))
print(tree.search_is_contained([2, 3]))
print(tree.left_search([4, 6]))
print(tree.right_search([3, 7]))
print(tree.stabbing_query(4))


for i in range(10):
    print("Inserting %d" % i)
    tree.insert([i, i * 2])
    print(tree)
#for i in range(10):
    #print("Deleting %d" % i)
    #tree.delete_value(i)
    #print(tree)

