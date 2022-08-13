# Implementation of B+-tree functionality.

from index import *
from math import log, ceil
from queue import Queue

def pnn(nn):
    for i in range(len(nn)):
        print(i, nn[i])

# Utility methods
def isLeafNode( node ):
    return node.pointers.pointers[0] == 0

# return: tuple of indices traversed to node that fits key
def getNodePath( index, key ):
    if len(index.nodes) == 0:
        return tuple()
    out = (0,)
    cur_index = 0
    cur_node = index.nodes[cur_index]
    while not isLeafNode(cur_node): 
        if key < cur_node.keys.keys[0]:
            cur_index = cur_node.pointers.pointers[0]
        elif key < cur_node.keys.keys[1] or cur_node.keys.keys[1] == -1:
            cur_index = cur_node.pointers.pointers[1]
        else:
            cur_index = cur_node.pointers.pointers[2]
        cur_node = index.nodes[cur_index]
        out += (cur_index,)
    return out

def nodeHeight( index ):
    return ceil(log(2*index + 3, 3))

def newNode( keys, pointers):
    return Node(\
        KeySet(keys),\
        PointerSet(pointers))

def shiftRight( index, node_index, shift):
    node = index.nodes[node_index]
    index.nodes[node_index] = Node()
    if not isLeafNode(node):
        for child in node.pointers.pointers:
            if child:
                shiftRight(index, child, shift*3)
        node.pointers = PointerSet(\
            tuple([(i + shift*3) if i else 0 for i in node.pointers.pointers]))
    else:
        node.pointers = PointerSet(\
            tuple([(i + shift) if i else 0 for i in node.pointers.pointers]))
    index.nodes[node_index + shift] = node

def addUnsplitChildren(index, new_nodes, cur_node, node_path, root_split):
    if not isLeafNode(cur_node):
        for child in cur_node.pointers.pointers:
            if child and child not in node_path:
                new_nodes[nodeHeight(child) - nodeHeight(node_path[0]) + (1 if root_split else 0)].append( \
                    index.nodes[child])
                new_nodes = addUnsplitChildren(index, new_nodes, index.nodes[child], node_path, root_split)
    return new_nodes

def getFirstKeyOfNode(node):
    return node.keys.keys[0]

def getNodesToUpdate( index, key, node_path, root_split=False ):
    new_nodes = []
    for i in range(len(node_path) + (1 if root_split else 0)):
        new_nodes.append([])

    # Iterate through node_path except root
    for i in range(len(node_path)-1, (-1 if root_split else 0), -1):
        cur_node = index.nodes[node_path[i]]

        # get children of node
        new_nodes = addUnsplitChildren(index, new_nodes, cur_node, node_path, root_split)

        # get new split nodes
        keys_to_split = list(cur_node.keys.keys) + [key]
        keys_to_split.sort()

        level = new_nodes[nodeHeight(node_path[i]) - nodeHeight(node_path[0]) + (1 if root_split else 0)]

        # If leaf node keep middle index
        if nodeHeight(node_path[i]) == nodeHeight(node_path[-1]):
            level.append(newNode((keys_to_split[1], keys_to_split[2]),(0,0,0)))
        else:
            level.append(newNode((keys_to_split[2], -1),(0,0,0)))

        level.append(newNode((keys_to_split[0], -1),(0,0,0)))

        # update key sent to next level up
        key = keys_to_split[1]

    # Add root
    if root_split:
        new_nodes[0].append(newNode((key, -1),(3*node_path[0] + 1, 3*node_path[0] + 2, 0)))
    else:
        root_keys = [index.nodes[node_path[0]].keys.keys[0]] + [key]
        new_nodes[0].append(newNode((min(root_keys),max(root_keys)),(\
            3*node_path[0] + 1,\
            3*node_path[0] + 2,\
            3*node_path[0] + 3)))

    # Sort nodes at each level
    for i in range(len(new_nodes)):
        new_nodes[i] = sorted(new_nodes[i], key=getFirstKeyOfNode)
    
    return new_nodes

def clearSubtree(index, i, max_h):
    index.nodes[i] = Node()
    if nodeHeight(i) < max_h:
        for child in (3*i + 1, 3*i + 2, 3*i + 3):
            clearSubtree(index, child, max_h)
    

# You should implement all of the static functions declared
# in the ImplementMe class and submit this (and only this!) file.
class ImplementMe:
    
    # Returns a B+-tree obtained by inserting a key into a pre-existing
    # B+-tree index if the key is not already there. If it already exists,
    # the return value is equivalent to the original, input tree.
    #
    # Complexity: Guaranteed to be asymptotically linear in the height of the tree
    # Because the tree is balanced, it is also asymptotically logarithmic in the
    # number of keys that already exist in the index.
    @staticmethod
    def InsertIntoIndex( index, key ):
        node_path = getNodePath(index, key)

        # If no root node, create it and return
        if not node_path:
            index.nodes.append(newNode((key, -1),(0,0,0)))
            return index

        # If key exists, return 
        leaf_node = index.nodes[node_path[-1]]
        if key in leaf_node.keys.keys:
            return index

        # Find deepest parent with space
        split_root = -1
        for i in range(len(node_path)-1,-1,-1):
            if -1 in index.nodes[node_path[i]].keys.keys:
                split_root = node_path[i]
                node_path = node_path[i:]
                break

        # If root split not required
        if split_root >= 0:
            # If leaf node has space add key to leaf 
            if split_root == node_path[-1]:
                leaf_node.keys = KeySet((\
                    min(key, leaf_node.keys.keys[0]),\
                    max(key, leaf_node.keys.keys[0])))
                return index

            else:
                # Shift middle node and children to right to right to make room if needed
                split_root_node = index.nodes[split_root]
                if split_root_node.pointers.pointers[0] in node_path:
                    shiftRight(index, split_root_node.pointers.pointers[0], 1)
                
                # Get 2d list of non-empty nodes in each level of changed subtree of split_root
                nodes_to_update = getNodesToUpdate(index, key, node_path)

                # Update split_root with pointers
                index.nodes[split_root] = nodes_to_update[0][0]

                # Initialize queue of indices to add nodes
                q = Queue()
                if split_root_node.pointers.pointers[0] in node_path:
                    q.put(nodes_to_update[0][0].pointers.pointers[1])
                    q.put(nodes_to_update[0][0].pointers.pointers[0])
                else:
                    q.put(nodes_to_update[0][0].pointers.pointers[2])
                    q.put(nodes_to_update[0][0].pointers.pointers[1])

                while not q.empty():
                    cur = q.get()
                    keys = nodes_to_update[nodeHeight(cur) - nodeHeight(split_root)].pop().keys.keys
                    # calculate pointers for directory nodes
                    if nodeHeight(cur) < nodeHeight(node_path[-1]):
                        pointers = ( \
                            3*cur + 1, \
                            3*cur + 2, \
                            3*cur + 3 if -1 not in keys else 0)
                        # Update queue
                        for i in range(2, -1, -1):
                            p = pointers[i]
                            if p:
                                q.put(p)
                            else:
                                # Fill subtree of any 0 pointers with blank nodes
                                clearSubtree(index, 3*cur + 3, nodeHeight(node_path[-1]))
                    # Leave leaf node pointers blank for now
                    else:
                        pointers = (0,0,0)
                    # Update index
                    index.nodes[cur] = newNode(keys, pointers)

        # If root split required
        else:
            new_nodes = getNodesToUpdate(index, key, node_path, root_split=True)
            
            index = Index([Node()]*(int)((1-3**(nodeHeight(node_path[-1])+1))/-2)) 
            index.nodes[0] = new_nodes[0][0]
            
            # Initialize queue of indices to add nodes
            q = Queue()
            q.put(2)
            q.put(1)

            
            while not q.empty():
                cur = q.get()
                keys = new_nodes[nodeHeight(cur) - 1].pop().keys.keys
                # calculate pointers for directory nodes
                if nodeHeight(cur) < nodeHeight(node_path[-1]) + 1:
                    pointers = ( \
                        3*cur + 1, \
                        3*cur + 2, \
                        3*cur + 3 if -1 not in keys else 0)
                    # Update queue
                    for i in range(2, -1, -1):
                        p = pointers[i]
                        if p:
                            q.put(p)
                        else:
                            # Fill subtree of any 0 pointers with blank nodes
                            clearSubtree(index, 3*cur + 3, nodeHeight(node_path[-1]))
                # Leave leaf node pointers blank for now
                else:
                    pointers = (0,0,0)
                # Update index
                index.nodes[cur] = newNode(keys, pointers)
            
        # Fix leaf pointers
        # Find last leaf node index
        next_index = len(index.nodes) - 1
        while index.nodes[next_index].keys.keys[0] == -1:
            next_index -= 1

        # Update pointers
        cur_index = next_index - 1
        while nodeHeight(cur_index) == nodeHeight(next_index):
            if index.nodes[cur_index].keys.keys[0] != -1:
                index.nodes[cur_index].pointers.pointers = (0, 0, next_index)
                next_index = cur_index
            cur_index -= 1
        return index

    # Returns a boolean that indicates whether a given key
    # is found among the leaves of a B+-tree index.
    #
    # Complexity: Guaranteed not to touch more nodes than the
    # height of the tree
    @staticmethod
    def LookupKeyInIndex( index, key ):
        node_path = getNodePath(index, key)

        # If no root node, return False
        if not node_path:
            return False
        
        # If key exists, return True; otherwise return False 
        if key in index.nodes[node_path[-1]].keys.keys:
            return True
        return False

    # Returns a list of keys in a B+-tree index within the half-open
    # interval [lower_bound, upper_bound)
    #
    # Complexity: Guaranteed not to touch more nodes than the height
    # of the tree and the number of leaves overlapping the interval.
    @staticmethod
    def RangeSearchInIndex( index, lower_bound, upper_bound ):
        node_path = getNodePath(index, lower_bound)        

        # Scan nodes to get all the keys, return dem keys
        key_list = []
        if node_path:
            cur_node = index.nodes[node_path[-1]]
            while cur_node:
                for k in cur_node.keys.keys:
                    if k >= lower_bound and k < upper_bound:
                        key_list += [k]
                    elif k != -1:
                        return key_list
                if cur_node.pointers.pointers[2]:
                    cur_node = index.nodes[cur_node.pointers.pointers[2]]
                else:
                    break
        return key_list