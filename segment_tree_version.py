from math import ceil, log2

# An utility function to get the middle index from corner indexes.
def get_Mid(s, e):
    return s + (e - s) // 2


""" A  function to get the sum of values in the given array. The following are parameters for this function.  
  
    seg_tree_pointer --> Pointer to segment tree  												# st
    seg_tree_index_of_node --> Index of current node in the segment tree.  						# si
           Initially 0 is passed as root is always at index 0  
    seg_tree_start_index & seg_tree_end_index --> Starting and ending indexes of the segment 	# ss
                	represented by current node  												# se
    query_start & query_end  --> Starting and ending indexes of query range """					# qs
    																							# qe


def get_Summary_Utility(seg_tree_pointer, seg_tree_start_index, seg_tree_end_index, query_start, query_end, seg_index_of_node):

    # If segment of this node is a part of given range, then return the sum of the segment
    if (query_start <= seg_tree_start_index and query_end >= seg_tree_end_index):
        return seg_tree_pointer[seg_index_of_node]

    # If segment of this node is outside the given range
    if (seg_tree_end_index < query_start or seg_tree_start_index > query_end):
        return 0

    # If a part of this segment overlaps with the given range
    mid = get_Mid(seg_tree_start_index, seg_tree_end_index)

    return get_Summary_Utility(seg_tree_pointer, seg_tree_start_index, mid, query_start, query_end, 2 * seg_index_of_node + 1) + \
        get_Summary_Utility(seg_tree_pointer, mid + 1, seg_tree_end_index, query_start, query_end, 2 * seg_index_of_node + 2)


""" A function to update the nodes in their range.    
i --> index of the element to be updated.This index is in the input array.  
diff --> Value to be added to all nodes which have i in range """


def replace_value_utility(seg_tree_pointer, seg_tree_start_index, seg_tree_end_index, i, diff, seg_index_of_node): #updateValueUtil

    # Base Case: If the input index lies
    # outside the range of this segment
    if (i < seg_tree_start_index or i > seg_tree_end_index):
        return

    # If the input index is in range of this node,
    # then update the value of the node and its children
    seg_tree_pointer[seg_index_of_node] = seg_tree_pointer[seg_index_of_node] + diff

    if (seg_tree_end_index != seg_tree_start_index):

        mid = get_Mid(seg_tree_start_index, seg_tree_end_index)
        replace_value_utility(seg_tree_pointer, seg_tree_start_index, mid, i,
                        diff, 2 * seg_index_of_node + 1)
        replace_value_utility(seg_tree_pointer, mid + 1, seg_tree_end_index, i,
                        diff, 2 * seg_index_of_node + 2)

def updateValue(array, seg_tree_pointer, n, i, new_value):

    # Check for erroneous input index
    if (i < 0 or i > n - 1):

        print("Invalid Input", end="")
        return

    # Get the difference between
    # new value and old value
    diff = new_value - array[i]

    # Update the value in array
    array[i] = new_value

    # Update the values of nodes in segment tree
    replace_value_utility(seg_tree_pointer, 0, n - 1, i, diff, 0)

# Return sum of elements in range from index qs (query start) to qe (query end). It mainly uses get_Summary_Utility()


def get_Summmary(seg_tree_pointer, n, query_start, query_end):

    # Check for erroneous input values
    if (query_start < 0 or query_end > n - 1 or query_start > query_end):

        print("Invalid Input", end="")
        return -1

    return get_Summary_Utility(seg_tree_pointer, 0, n - 1, query_start, query_end, 0)

# A recursive function that constructs
# Segment Tree for array[ss..se].
# si is index of current node in segment tree seg_tree_pointer


def constructSTUtil(array, seg_tree_start_index, seg_tree_end_index, seg_tree_pointer, seg_tree_index_of_node):

    # If there is one element in array,
    # store it in current node of
    # segment tree and return
    if (seg_tree_start_index == seg_tree_end_index):

        seg_tree_pointer[seg_tree_index_of_node] = array[seg_tree_start_index]
        return array[seg_tree_start_index]

    # If there are more than one elements,
    # then recur for left and right subtrees
    # and store the sum of values in this node
    mid = get_Mid(seg_tree_start_index, seg_tree_end_index)

    seg_tree_pointer[seg_tree_index_of_node] = constructSTUtil(array, seg_tree_start_index, mid, seg_tree_pointer, seg_tree_index_of_node * 2 + 1) +\
        constructSTUtil(array, mid + 1, seg_tree_end_index, seg_tree_pointer, seg_tree_index_of_node * 2 + 2)

    return seg_tree_pointer[seg_tree_index_of_node]


""" Function to construct segment tree  
from given array. This function allocates memory 
for segment tree and calls constructSTUtil() to  
fill the allocated memory """


def constructST(array, n):

    # Allocate memory for the segment tree

    # Height of segment tree
    x = (int)(ceil(log2(n)))

    # Maximum size of segment tree
    max_size = 2 * (int)(2**x) - 1

    # Allocate memory
    seg_tree_pointer = [0] * max_size

    # Fill the allocated memory st
    constructSTUtil(array, 0, n - 1, seg_tree_pointer, 0)

    # Return the constructed segment tree
    return seg_tree_pointer

    # Driver Code


array = [1, 3, 5, 7, 9, 11]
n = len(array)
# Build segment tree from given array
seg_tree_pointer = constructST(array, n)
print(seg_tree_pointer)

# Print sum of values in array from index 1 to 3
print("Sum of values in given range = ",
      get_Summmary(seg_tree_pointer, n, 0, 3))

# Update: set arr[1] = 10 and update
# corresponding segment tree nodes
updateValue(array, seg_tree_pointer, n, 1, 10)

# Find sum after the value is updated
print("Updated sum of values in given range = ",
      get_Summmary(seg_tree_pointer, n, 0, 3))