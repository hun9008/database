from typing import List, Tuple
import math
from itertools import combinations


class Rectangle:
    
    def __init__(self, x1 : int, y1 : int, x2 : int = None, y2 : int = None, name : str = None):
        
        if x2 is None and y2 is None:
            x2, y2 = x1, y1
        elif x2 is None and y2 is not None:
            raise ValueError("invalid rectangle nor a point") 
        elif x2 is not None and y2 is None:
            raise ValueError("invalid rectangle nor a point")   
        
        ## Rearrange the coordinates x2 being greater than x1 and y2 being greater than y1
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.name = name
            
    
    def area(self) -> int:
        return (self.x2 - self.x1) * (self.y2 - self.y1)
    
    
    def to_str(self) -> str:
        if self.name is None:
            return f"Rectangle({self.x1}, {self.y1}, {self.x2}, {self.y2})"
        else :
            return f"Rectangle_{self.name}({self.x1}, {self.y1}, {self.x2}, {self.y2})"

    
    def overlap(self, other) -> bool:
        return not (self.x1 > other.x2 or self.x2 < other.x1 or self.y1 > other.y2 or self.y2 < other.y1)
    
    
    def exact_overlap(self, other) -> bool:
        return self.x1 == other.x1 and self.y1 == other.y1 and self.x2 == other.x2 and self.y2 == other.y2
    
    
    def within(self, other) -> bool:
        return self.x1 >= other.x1 and self.y1 >= other.y1 and self.x2 <= other.x2 and self.y2 <= other.y2
    

class RTreeNode:
    
    def __init__(
        self,
        entries : List[Rectangle] = [],
        is_leaf : bool = True
    ):  
        self.entries = entries or []
        self.is_leaf = is_leaf
        self.children = []
        self.mbr = Rectangle(0, 0, 0, 0)
    
    
    def update_node_mbrs(self):
        # Update mbr using entries or children 
        if self.is_leaf:
            x1 = min(rect.x1 for rect in self.entries)
            y1 = min(rect.y1 for rect in self.entries)
            x2 = max(rect.x2 for rect in self.entries)
            y2 = max(rect.y2 for rect in self.entries)
        else :
            x1 = min(child.mbr.x1 for child in self.children)
            y1 = min(child.mbr.y1 for child in self.children)
            x2 = max(child.mbr.x2 for child in self.children)
            y2 = max(child.mbr.y2 for child in self.children)
        
        self.mbr = Rectangle(x1, y1, x2, y2)
    
    
    

class RTree:
    
    def __init__(self, max_entries=3, min_entries=1):
        self.root = RTreeNode()
        self.max_entries = max_entries
        self.min_entries = min_entries

    """
    START OF IMPLEMENTATION OF INSERT
    """
    
    def insert(self, rect : Rectangle):
        """
        Given a rectangle 'rect', insert the rectangle into the index
        """
        if self.root.is_leaf:
            # insert
            # print("Inserting Root", rect.to_str())
            self.root.entries.append(rect)
            self.root.update_node_mbrs()

            # split
            if len(self.root.entries) <= self.max_entries:
                # print(self.root.mbr.to_str())
                return
            else :
                # print("Splitting Root")
                node_1 = RTreeNode()
                node_2 = RTreeNode()
                entries = self.root.entries

                # for entry in entries:
                #     print(entry.to_str())

                max_area = 0
                max_entries = []
                max_entries_idx = []

                for i in range(0, len(entries)):
                    for j in range(i+1, len(entries)):
                        temp = RTreeNode()
                        temp.entries.append(entries[i])
                        temp.entries.append(entries[j])
                        temp.update_node_mbrs()
                        # print(temp.mbr.area())
                        if temp.mbr.area() > max_area:
                            max_area = temp.mbr.area()
                            max_entries = [entries[i], entries[j]]
                            max_entries_idx = [i, j]

                # print("Max Area : ", max_area)
                # print("Max Entries : ", max_entries[0].to_str(), max_entries[1].to_str())
                        
                if max_entries_idx[0] < max_entries_idx[1]:
                    node_1.entries.append(max_entries[0])
                    node_1.update_node_mbrs()
                    node_2.entries.append(max_entries[1])
                    node_2.update_node_mbrs()
                else:
                    node_1.entries.append(max_entries[1])
                    node_1.update_node_mbrs()
                    node_2.entries.append(max_entries[0])
                    node_2.update_node_mbrs()

                # node_1.entries.append(max_entries[0])
                # node_1.update_node_mbrs()
                # node_2.entries.append(max_entries[1])
                # node_2.update_node_mbrs()

                sorted_entries = []
                for entry in entries:
                    if entry.exact_overlap(max_entries[0]) or entry.exact_overlap(max_entries[1]):
                        continue
                    else :
                        temp_1 = RTreeNode()
                        temp_2 = RTreeNode()
                        for temp_entry in node_1.entries:
                            temp_1.entries.append(temp_entry)
                        for temp_entry in node_2.entries:
                            temp_2.entries.append(temp_entry)
                        temp_1.entries.append(entry)
                        temp_1.update_node_mbrs()
                        temp_2.entries.append(entry)
                        temp_2.update_node_mbrs()
                        diff_area_1 = temp_1.mbr.area() - node_1.mbr.area()
                        diff_area_2 = temp_2.mbr.area() - node_2.mbr.area()
                        diff_area = diff_area_1 - diff_area_2
                        if diff_area < 0:
                            diff_area = -diff_area
                        sorted_entries.append([(diff_area), entry])
                        
                
                sorted_entries.sort(key=lambda x: x[0], reverse=True)

                # print("Sorted Entries : ")
                # for diff_area ,entry in sorted_entries:
                #     print("Diff Area : ", diff_area, " Entry : ", entry.to_str())
                #     # print()

                # for diff_area ,entry in sorted_entries:
                while(len(sorted_entries) > 0):
                    # print("sorted len : ", len(sorted_entries))
                    temp_sorted_entries = []
                    for diff_area, entry in sorted_entries:
                        if entry.exact_overlap(max_entries[0]) or entry.exact_overlap(max_entries[1]):
                            continue
                        else :
                            temp_1 = RTreeNode()
                            temp_2 = RTreeNode()
                            for temp_entry in node_1.entries:
                                temp_1.entries.append(temp_entry)
                            for temp_entry in node_2.entries:
                                temp_2.entries.append(temp_entry)
                            temp_1.entries.append(entry)
                            temp_1.update_node_mbrs()
                            temp_2.entries.append(entry)
                            temp_2.update_node_mbrs()
                            diff_area_1 = temp_1.mbr.area() - node_1.mbr.area()
                            diff_area_2 = temp_2.mbr.area() - node_2.mbr.area()
                            diff_area = diff_area_1 - diff_area_2
                            if diff_area < 0:
                                diff_area = -diff_area
                            temp_sorted_entries.append([(diff_area), entry])     
                    sorted_entries = []
                    for diff_area, entry in temp_sorted_entries:
                        sorted_entries.append([diff_area, entry])
                
                    sorted_entries.sort(key=lambda x: x[0], reverse=True)
                    # print("Sorted Entries : ")
                    # for diff_area ,entry in sorted_entries:
                    #     print("Diff Area : ", diff_area, " Entry : ", entry.to_str())

                    cnt = 0
                    if entry.exact_overlap(max_entries[0]) or entry.exact_overlap(max_entries[1]):
                        continue
                    else :
                        # print("@@@@@@@@@@@@@ case 1 @@@@@@@@@@@@@")
                        temp_1 = RTreeNode()
                        temp_2 = RTreeNode()
                        for temp_entry in node_1.entries:
                            temp_1.entries.append(temp_entry)
                        for temp_entry in node_2.entries:
                            temp_2.entries.append(temp_entry)
                        temp_1.entries.append(sorted_entries[0][1])
                        temp_1.update_node_mbrs()
                        temp_2.entries.append(sorted_entries[0][1])
                        temp_2.update_node_mbrs()
                        diff_area_1 = temp_1.mbr.area() - node_1.mbr.area()
                        diff_area_2 = temp_2.mbr.area() - node_2.mbr.area()
                        # print("=====================================")
                        # print("diff area 1 : ", diff_area_1)
                        # print("diff area 2 : ", diff_area_2)
                        # print("=====================================")
                        if diff_area_1 == diff_area_2:
                            if node_1.mbr.area() <= node_2.mbr.area():
                                if (len(node_1.entries) == self.max_entries-1 and len(node_2.entries) < self.min_entries):
                                    node_2 = temp_2
                                    # print("count : ", cnt , " win node 2(min case)")
                                else:
                                    node_1 = temp_1
                                    # print("count : ", cnt , " win node 1")
                            else :
                                if (len(node_2.entries) == self.max_entries-1 and len(node_1.entries) < self.min_entries):
                                    node_1 = temp_1
                                    # print("count : ", cnt , " win node 1(min case)")
                                else:
                                    node_2 = temp_2
                                    # print("count : ", cnt , " win node 2")
                        elif diff_area_1 < diff_area_2:
                            if (len(node_1.entries) == self.max_entries-1 and len(node_2.entries) < self.min_entries):
                                node_2 = temp_2
                                # print("count : ", cnt , " win node 2(min case)")
                            else:
                                node_1 = temp_1
                                # print("count : ", cnt , " win node 1")
                        else :
                            if len(node_2.entries) == self.max_entries-1 and len(node_1.entries) < self.min_entries:
                                node_1 = temp_1
                                # print("count : ", cnt , " win node 1(min case)")
                            else:
                                node_2 = temp_2
                                # print("count : ", cnt , " win node 2")
                    cnt += 1
                    # print("{Node 1} : ", node_1.mbr.to_str())
                    # print("{Node 2} : ", node_2.mbr.to_str())
                    node_1.update_node_mbrs()
                    node_2.update_node_mbrs()
                    sorted_entries.remove(sorted_entries[0])

                node_1.update_node_mbrs()
                # print("Node 1 : ", node_1.mbr.to_str())
                node_2.update_node_mbrs()
                # print("Node 2 : ", node_2.mbr.to_str())

                self.root = RTreeNode()
                self.root.children.append(node_1)
                self.root.children.append(node_2)
                self.root.is_leaf = False
                self.root.entries = []
                # self.root.entries.append(node_1.mbr)
                # self.root.entries.append(node_2.mbr)
                self.root.update_node_mbrs()

            # print("||| insert ||| : ", rect.to_str())
            return
        else :
            # find leaf
            # print("Inserting leaf", rect.to_str())
            leaf_node = self.root
            while (leaf_node.is_leaf == False):
                # temp_node = RTreeNode()
                # temp_node.entries.append(rect)
                # temp_node.update_node_mbrs()
                # leaf_node.children.append(temp_node)
                # leaf_node.update_node_mbrs()
                # leaf_node.children.remove(temp_node)
                # print("entering while")
                min_child = leaf_node.children[0]
                for child in leaf_node.children:
                    # print("entering for")
                    temp_1 = RTreeNode()
                    temp_2 = RTreeNode()
                    for temp_entry in min_child.entries:
                        temp_1.entries.append(temp_entry)
                    for temp_entry in child.entries:
                        temp_2.entries.append(temp_entry)
                    temp_1.entries.append(rect)
                    temp_1.update_node_mbrs()
                    temp_2.entries.append(rect)
                    temp_2.update_node_mbrs()
                    # print("min_child : ", temp_1.mbr.to_str(), " area : ", temp_1.mbr.area() - min_child.mbr.area())
                    # print("child : ", temp_2.mbr.to_str(), " area : ", temp_2.mbr.area() - child.mbr.area())
                    
                    if temp_1.mbr.area() - min_child.mbr.area() > temp_2.mbr.area() - child.mbr.area():
                        # print("change child!")
                        # print("min_child : ", min_child.mbr.to_str())
                        # print("child : ", child.mbr.to_str())
                        min_child = child
                leaf_node = min_child

                    
            # print("Im here Shit")
            # print("find Leaf : ", leaf_node.mbr.to_str())
            leaf_node.entries.append(rect)
            leaf_node.update_node_mbrs()
            
            
            # print("Leaf node entries : ", len(leaf_node.entries))
            while( len(leaf_node.entries) > self.max_entries or len(leaf_node.children) > self.max_entries):
                # find parent
                parent_node = self.root
                # print("root : " , self.root.mbr.to_str())
                # for child in parent_node.children:
                #     print("child : ", child.mbr.to_str(), " is leaf : ", child.is_leaf)
                # print("root child : ", self.root.children[0].mbr.to_str())
                if parent_node.mbr.exact_overlap(parent_node.children[0].mbr):
                    # print("what the same!")
                    self.root = self.root.children[0]
                    parent_node = self.root
                elif parent_node.children[0].is_leaf == True:
                    # print("parent_node is root : ", parent_node.mbr.to_str())
                    # print("", end="")
                    empty_box = 0
                else :
                    # while(parent_node.mbr.within(leaf_node.mbr) == False & parent_node.is_leaf == False):
                    while(leaf_node.mbr.within(parent_node.mbr) == False and parent_node.is_leaf == False):
                        # print("hey")
                        for child in parent_node.children:
                            # print("here!")
                            # print("child : ", child.mbr.to_str())
                            if child.mbr.overlap(leaf_node.mbr):
                            # if leaf_node.mbr.within(child.mbr):
                                # print("parent changed!")
                                parent_node = child
                                break   
                # print("Parent node : ", parent_node.mbr.to_str())
                # print("Splitting leaf")
                node_1 = RTreeNode()
                node_2 = RTreeNode()
                if leaf_node.is_leaf:
                    node_1.is_leaf = True
                    node_2.is_leaf = True

                if leaf_node.is_leaf:
                    entries = leaf_node.entries
                    # for entry in entries:
                    #     # print(entry.to_str())
                    #     print()
                else:
                    entries = []
                    for child in leaf_node.children:
                        entries.append(child.mbr)
                    # for entry in entries:
                    #     # print(entry.to_str())
                    #     print()
                    
                max_area = 0
                max_entries = []
                max_entries_idx = []

                for i in range(0, len(entries)):
                    for j in range(i+1, len(entries)):
                        temp = RTreeNode()
                        temp.entries.append(entries[i])
                        temp.entries.append(entries[j])
                        temp.update_node_mbrs()
                        # print(temp.mbr.area())
                        if temp.mbr.area() >= max_area:
                            max_area = temp.mbr.area()
                            max_entries = [entries[i], entries[j]]
                            max_entries_idx = [i, j]

                # print("Max Area : ", max_area)
                # print("Max Entries : ", max_entries[0].to_str(), max_entries[1].to_str())
                # print("idx : ", max_entries_idx[0], max_entries_idx[1])

                if max_entries_idx[0] < max_entries_idx[1]:
                    if max_entries[0].x1 < max_entries[1].x1 and max_entries[0].y1 > max_entries[1].y1:
                        if (max_entries[0].y2 - max_entries[1].y1) == self.min_entries or (max_entries[0].x1 - max_entries[1].x1) == self.min_entries:
                            node_1.entries.append(max_entries[1])
                            node_1.update_node_mbrs()
                            node_2.entries.append(max_entries[0])
                            node_2.update_node_mbrs()
                        else:
                            node_1.entries.append(max_entries[0])
                            node_1.update_node_mbrs()
                            node_2.entries.append(max_entries[1])
                            node_2.update_node_mbrs()
                    else:
                        # print("case x")
                        if (max_entries[0].x1 - max_entries[1].x1) == self.min_entries and (max_entries[0].y1 < max_entries[1].y1):
                            node_1.entries.append(max_entries[1])
                            node_1.update_node_mbrs()
                            node_2.entries.append(max_entries[0])
                            node_2.update_node_mbrs()
                        else:
                            node_1.entries.append(max_entries[0])
                            node_1.update_node_mbrs()
                            node_2.entries.append(max_entries[1])
                            node_2.update_node_mbrs()
                else:
                    node_1.entries.append(max_entries[1])
                    node_1.update_node_mbrs()
                    node_2.entries.append(max_entries[0])
                    node_2.update_node_mbrs()


                # node_1.entries.append(max_entries[0])
                # node_1.update_node_mbrs()
                # node_2.entries.append(max_entries[1])
                # node_2.update_node_mbrs()

                sorted_entries = []
                for entry in entries:
                    if entry.exact_overlap(max_entries[0]) or entry.exact_overlap(max_entries[1]):
                        continue
                    else :
                        # print("@@@@@@@@@@@@@ case 2 @@@@@@@@@@@@@")
                        temp_1 = RTreeNode()
                        temp_2 = RTreeNode()
                        for temp_entry in node_1.entries:
                            temp_1.entries.append(temp_entry)
                        for temp_entry in node_2.entries:
                            temp_2.entries.append(temp_entry)
                        temp_1.entries.append(entry)
                        temp_1.update_node_mbrs()
                        temp_2.entries.append(entry)
                        temp_2.update_node_mbrs()
                        # print("@@@@@ parent : ", parent_node.mbr.to_str())
                        # print("@@@@@ root child: ", len(self.root.children))
                        # if len(self.root.children) == self.min_entries:
                        #     diff_area = temp_1.mbr.area() + temp_2.mbr.area()
                        # else:
                        diff_area = (temp_1.mbr.area() - node_1.mbr.area()) - (temp_2.mbr.area() - node_2.mbr.area())
                        if diff_area < 0:
                            diff_area = -diff_area
                        sorted_entries.append([(diff_area), entry])
                
                # if len(self.root.children) == self.min_entries:
                #     sorted_entries.sort(key=lambda x: x[0])
                # else:
                sorted_entries.sort(key=lambda x: x[0], reverse=True)
                # print("root child 0 : ", sorted_entries[0][0])
                # if len(self.root.children) == self.min_entries and sorted_entries[0][0] == 0:
                #     sorted_entries.sort(key=lambda x: x[0])
                # else:  
                #     sorted_entries.sort(key=lambda x: x[0], reverse=True)
                # print("Sorted Entries : ")
                # for diff_area ,entry in sorted_entries:
                    # print("Diff Area : ", diff_area, " Entry : ", entry.to_str())
                    # print()
                for diff_area ,entry in sorted_entries:
                    # print("root child: ", len(self.root.children))
                    cnt = 0
                    if entry.exact_overlap(max_entries[0]) or entry.exact_overlap(max_entries[1]):
                        continue
                    else :
                        temp_1 = RTreeNode()
                        temp_2 = RTreeNode()
                        for temp_entry in node_1.entries:
                            temp_1.entries.append(temp_entry)
                        for temp_entry in node_2.entries:
                            temp_2.entries.append(temp_entry)
                        temp_1.entries.append(entry)
                        temp_1.update_node_mbrs()
                        temp_2.entries.append(entry)
                        temp_2.update_node_mbrs()
                        diff_area_1 = temp_1.mbr.area() - node_1.mbr.area()
                        diff_area_2 = temp_2.mbr.area() - node_2.mbr.area()
                        # print("=====================================")
                        # print("diff area 1 : ", diff_area_1)
                        # print("diff area 2 : ", diff_area_2)
                        # print("=====================================")
                        if diff_area_1 == diff_area_2:
                            if node_1.mbr.area() <= node_2.mbr.area():
                                if (len(node_1.entries) == self.max_entries-1 and len(node_2.entries) < self.min_entries):
                                    node_2 = temp_2
                                    # print("count : ", cnt , " win node 2(min case)")
                                else:
                                    node_1 = temp_1
                                    # print("count : ", cnt , " win node 1")
                            else :
                                if (len(node_2.entries) == self.max_entries-1 and len(node_1.entries) < self.min_entries):
                                    node_1 = temp_1
                                    # print("count : ", cnt , " win node 1(min case)")
                                else:
                                    node_2 = temp_2
                                    # print("count : ", cnt , " win node 2")
                        elif diff_area_1 < diff_area_2:
                            if (len(node_1.entries) == self.max_entries-1 and len(node_2.entries) < self.min_entries):
                                node_2 = temp_2
                                # print("count : ", cnt , " win node 2(min case)")
                            else:
                                node_1 = temp_1
                                # print("count : ", cnt , " win node 1")
                        else :
                            if len(node_2.entries) == self.max_entries-1 and len(node_1.entries) < self.min_entries:
                                node_1 = temp_1
                                # print("count : ", cnt , " win node 1(min case)")
                            else:
                                node_2 = temp_2
                                # print("count : ", cnt , " win node 2")
                    cnt += 1
                    # print("{Node 1} : ", node_1.mbr.to_str())
                    # print("{Node 2} : ", node_2.mbr.to_str())

                node_1.update_node_mbrs()
                # print("Node 1 : ", node_1.mbr.to_str())
                node_2.update_node_mbrs()
                # print("Node 2 : ", node_2.mbr.to_str())

                # print("Leaf node : ", leaf_node.mbr.to_str())
                # print("Parent node : ", parent_node.mbr.to_str())
                # print("Parent children num : ", len(parent_node.children))
                # for child in parent_node.children:
                #     # print("Child node : ", child.mbr.to_str())
                # for entries in parent_node.entries:
                #     print("Parent entries : ", entries.to_str())
                    # print("type of entries : ", type(entries))
                # print("leaf is : ", leaf_node.mbr.to_str())
                # print("leaf is real leaf? : ", leaf_node.is_leaf)

                # print("node children")
                # for node1_child in node_1.children:
                #     print("node1 child : ", node1_child.mbr.to_str())
                # for node2_child in node_2.children:
                #     print("node2 child : ", node2_child.mbr.to_str())

                # print(" NODE 1 & 2 LEAF CHECK : ", node_1.is_leaf, node_2.is_leaf)
                if leaf_node.is_leaf:
                    # if leaf_node.mbr.within(parent_node):
                    # print("@@@ check @@@")
                    # for child in parent_node.children:
                    #     print("parent child : ", child.mbr.to_str())
                    p = parent_node.children[0].children
                    # for child in p:
                    #     # print("parent child : ", child.mbr.to_str())
                    flag = True
                    while (flag):
                        for child in parent_node.children:
                            if leaf_node.mbr.within(child.mbr):
                                if leaf_node.mbr.exact_overlap(child.mbr):
                                    flag = False
                                    break
                                else :
                                    parent_node = child
                                    break

                    parent_node.children.remove(leaf_node)
                    # print("case 1")

                    parent_node.children.append(node_1)
                    parent_node.children.append(node_2)
                    # print("node 1 : ", node_1.mbr.x1)
                    # print("node 2 : ", node_2.mbr.x2)
                    # if node_1.mbr.x1 == node_2.mbr.x2:
                    #     parent_node.children.append(node_2)
                    #     parent_node.children.append(node_1)
                    # else:
                    #     if node_1.mbr.area() < node_2.mbr.area():
                    #         print("case 1-1")
                    #         parent_node.children.append(node_1)
                    #         parent_node.children.append(node_2)
                    #     else:
                    #         print("case 1-2")
                    #         parent_node.children.append(node_2)
                    #         parent_node.children.append(node_1)
                        # parent_node.children.append(node_1)
                        # parent_node.children.append(node_2)
                else:
                    node_1.is_leaf = False
                    node_2.is_leaf = False
                    for parent_child in parent_node.children:
                        if parent_child.mbr.within(node_1.mbr):
                            node_1.children.append(parent_child)
                        elif parent_child.mbr.within(node_2.mbr):
                            node_2.children.append(parent_child)
                        else :
                            # print("================== error ===================")
                            break
                    parent_node.children.clear()
                    # print("case 2")
                    # if node_1.mbr.area() < node_2.mbr.area():
                    #     parent_node.children.append(node_1)
                    #     parent_node.children.append(node_2)
                    # else:
                    #     parent_node.children.append(node_2)
                    #     parent_node.children.append(node_1)
                    parent_node.children.append(node_1)
                    parent_node.children.append(node_2)

                # parent_node.entries.remove(leaf_node.mbr)
                # parent_node.children.append(node_1)
                # parent_node.children.append(node_2)
                # leaf_node.is_leaf = False
                # parent_node.entries.append(node_1.mbr)
                # parent_node.entries.append(node_2.mbr)
                parent_node.update_node_mbrs()
                # print("updated leaf_node(p) : ", parent_node.mbr.to_str())
                # print("updated leaf_node(p) children num : ", len(parent_node.children))
                leaf_node = parent_node
                # print("updated leaf_node : ", leaf_node.mbr.to_str())
                # print("updated leaf_node children num : ", len(leaf_node.children))
                # print("\n\n\n")
            
            # print("Leaf Check : ", leaf_node.is_leaf)
            # print("Leaf node entries : ", leaf_node.mbr.to_str())
            target_node = self.root
            silk_load = []
            silk_load.append(target_node)
            
            if target_node.children[0].is_leaf == True:
                for child in target_node.children:
                    # print("t child : ", child.mbr.to_str())
                    if child.mbr.overlap(leaf_node.mbr):
                        # print("added")
                        target_node = child
                        silk_load.append(target_node)
                        break
            else :
                find_leaf = None
                queue = []
                queue.append(self.root)

                # find leaf within rect
                while queue:
                    node = queue.pop(0)
                    if node.is_leaf:
                        for entry in node.entries:
                            if entry.exact_overlap(rect):
                                find_leaf = node
                                break
                    else :
                        for child in node.children:
                            queue.append(child)
                
                # print("find leaf : ", find_leaf.mbr.to_str())
                # find_leaf.update_node_mbrs()


                while(target_node.is_leaf == False):
                # while(target_node.is_leaf == False):
                    for child in target_node.children:
                        # print("f leaf : ", find_leaf.mbr.to_str())
                        # print("child : ", child.mbr.to_str())
                        # if child.mbr.overlap(leaf_node.mbr):
                        if find_leaf.mbr.overlap(child.mbr):
                            # print("within")
                            target_node = child
                            silk_load.append(target_node)
                            # break
                silk_load.append(find_leaf)

            # print("silk load : ")
            # for silk in silk_load:
            #     print(silk.mbr.to_str())

            silk_load.reverse()
            for silk in silk_load:
                # print("Iam updating node : ", silk.mbr.to_str())
                silk.update_node_mbrs()

            self.root.update_node_mbrs()
            # print("Root : ", self.root.mbr.to_str())
            # print("||| insert ||| : ", rect.to_str())
            return


        raise NotImplementedError("Implement this function")
    """
    END OF IMPLEMENTATION OF INSERT
    """
    
    """
    START OF IMPLEMENTATION OF DELETE
    """
    def delete(self, delete_rectangle : Rectangle) -> List[Rectangle]:
        """
        Given a deleting_rectangle 'delete_rectangle', delete the index record with that same rectangle
        if successful, return the deleted index record
        if not successful, return None
        """
        # print("\n\n\n\n####### Deleting leaf ##########", delete_rectangle.to_str())
        target_node = self.root
        silk_load = []
        silk_load.append(target_node)
        
        if target_node.children[0].is_leaf == True:
            for child in target_node.children:
                # print("t child : ", child.mbr.to_str())
                if child.mbr.overlap(delete_rectangle):
                    # print("added")
                    target_node = child
                    silk_load.append(target_node)
                    break
        else :
            while(target_node.mbr.within(delete_rectangle) == True & target_node.is_leaf == False):
                for child in target_node.children:
                    # print("child : ", child.mbr.to_str())
                    if child.mbr.overlap(delete_rectangle):
                        target_node = child
                        silk_load.append(target_node)
                        break
        
        same_one = target_node.entries[0]
        for entry in target_node.entries:
            # print(entry.to_str())
            # print("entry pos : ", entry.x1, entry.y1, entry.x2, entry.y2)
            if delete_rectangle.exact_overlap(entry):
                # print("it is same!!!!!")
                same_one = entry

        # print("delete rect : ", delete_rectangle.to_str())
        # print("delete pos : ", delete_rectangle.x1 , delete_rectangle.y1, delete_rectangle.x2, delete_rectangle.y2)
        target_node.entries.remove(same_one)
        target_node.update_node_mbrs()

        # for silk in silk_load:
        #     # print("silk : ", silk.mbr.to_str())

        # print("target : ", target_node.mbr.to_str())
        # print("target len : ", len(target_node.entries))
        if len(target_node.entries) < self.min_entries:
            # print("re insert")
            # print("target : ", target_node.mbr.to_str())
            node_flag = False
            adding_rect = target_node.entries[0]
            # print("adding rect : ", adding_rect.to_str())
            for node in silk_load[::-1]:
                # print("Iam : ", node.mbr.to_str())
                if node is target_node:
                    node_flag = True
                    continue
                else :
                    if node_flag:
                        node.children.remove(target_node)
                        node.update_node_mbrs()
                        node_flag = False
                    else:
                        node.update_node_mbrs()
                    
            self.insert(adding_rect)
            # for silk in silk_load:
                # print("silk : ", silk.mbr.to_str())

            balance = True
            # check tree balance
            queue = []
            queue.append(self.root)
            while queue:
                node = queue.pop(0)
                if len(node.children) < self.min_entries:
                    balance = False
                    break
                else :
                    for child in node.children:
                        if child.is_leaf == False:
                            queue.append(child)

            if balance == True:
                # print("\n\nbalanced\n\n")
                return [same_one]
            else: 

                # i = 0
                # target_node = silk_load[-2 - i]
                # print("target : ", target_node.mbr.to_str())
                new_silk_load = []
                target_node = self.root
                queue = []
                queue.append(target_node)
                del_node = None
                while queue:
                    node = queue.pop(0)
                    if len(node.children) >= self.min_entries:
                        for child in node.children:
                            queue.append(child)
                    else :
                        del_node = node
                        break
                
                # target_node = del_node
                new_silk_load.append(target_node)

                if target_node.children[0].is_leaf == True:
                    # print("leaf")
                    for child in target_node.children:
                        # print("t child : ", child.mbr.to_str())
                        if child.mbr.overlap(delete_rectangle):
                            # print("added")
                            target_node = child
                            new_silk_load.append(target_node)
                            break
                else:
                    # print("not leaf")
                    # print("target : ", target_node.mbr.to_str())
                    # print("del : ", del_node.mbr.to_str())
                    # print(target_node.mbr.within(del_node.mbr))
                    # print(del_node.mbr.within(target_node.mbr))
                    while(del_node.mbr.within(target_node.mbr) == True and target_node.is_leaf == False):
                        # print("enter")
                        for child in target_node.children:
                            # print("child : ", child.mbr.to_str(), "childs : ", len(child.children))
                            if child.mbr.overlap(del_node.mbr):
                                target_node = child
                                new_silk_load.append(target_node)
                                break

                # for silk in new_silk_load:
                    # print("new_silk : ", silk.mbr.to_str(), " childs : ", len(silk.children))
                
                new_silk_load.reverse()

                # for silk in new_silk_load:
                #     print("reverse silk : ", silk.mbr.to_str(), " childs : ", len(silk.children))

                leaf_node = new_silk_load[0]
                del_leaf = leaf_node
                # print("leaf node : ", leaf_node.mbr.to_str())
                new_silk_load.remove(leaf_node)

                for silk in new_silk_load:
                    silk.children.remove(del_leaf)
                    # silk.update_node_mbrs()
                    del_leaf = silk
                
                leaves = []

                for Leaf in leaf_node.entries:
                    # print("leaf entries : ", Leaf.to_str())
                    leaves.append(Leaf)
                for Leaf in leaf_node.entries:
                    leaf_node.entries.remove(Leaf)

                for leaf in leaves:
                    print("leaf : ", leaf.to_str())

                # print("\n\n\n insert leaves 0 \n\n\n")
                # self.insert(leaves[0])
                # print("\n\n\n insert leaves 1 \n\n\n")
                # self.insert(leaves[1])
                for Leaf in leaves:
                    self.insert(Leaf)

                return [same_one]
        else :
            # print("just delete")

            for node in silk_load[::-1]:
                # print("Iam updating node : ", node.mbr.to_str())
                node.update_node_mbrs()

            return [same_one]
        

        raise NotImplementedError("Implement this function")
    """
    END OF IMPLEMENTATION OF DELETE
    """
    
    """
    START OF IMPLEMENTATION OF SEARCH
    """
    def search(self, search_rectangle : Rectangle) -> List[Rectangle]:
        """
         Given a rectangle 'search_rectangle', find all index records whoose
            rectangles overlap with 'search_rectangle'
        """
        # print("Searching leaf", search_rectangle.to_str())

        target_node = self.root
        target_nodes = []
        search_entries = []
        
        if target_node.children[0].is_leaf == True:
            for child in target_node.children:
                # print("t child : ", child.mbr.to_str())
                if child.mbr.overlap(search_rectangle):
                    # print("searching.. : ", child.mbr.to_str())
                    target_node = child
                    target_nodes.append(target_node)
                    # search_entries.append(target_node.entries)
                    # break
        else :
            # while(target_node.mbr.within(search_rectangle) == True & target_node.is_leaf == False):
            # while(target_node.mbr.overlap(search_rectangle) == True):
            #     for child in target_node.children:
            #         print("child : ", child.mbr.to_str())
            #         if child.mbr.within(search_rectangle):
            #             target_node = child
            #             target_nodes.append(target_node)
            #             # search_entries.append(target_node.entries)
            #             # break
            queue = []
            queue.append(target_node)
            while queue:
                node = queue.pop(0)
                if node.is_leaf:
                    target_nodes.append(node)
                else :
                    if node.mbr.overlap(search_rectangle):
                        target_nodes.append(node)
                        for child in node.children:
                            queue.append(child)
                    else :
                        continue
                        
        for target_node in target_nodes:
            for entry in target_node.entries:
                if entry.within(search_rectangle):
                    search_entries.append(entry)

        return search_entries
        raise NotImplementedError("Implement this function")  
    """
    END OF IMPLEMENTATION OF SEARCH
    """
    
    """
    START OF IMPLEMENTATION OF PRINT    
    """
    def print_tree(self) -> str:
        """
            print node mbrs traversing bfs
            print each level mbrs
            [Rectangle(n,n,n,n)]-[Rectagle(n,n,n,n), Rectangle(n,n,n,n)]-[Rectagle(n,n,n,n), Rectangle(n,n,n,n)]
        """

        # # Initialize the queue with the root
        # print("print start!")
        queue = [(self.root, 0)]
        leaf_queue = []
        current_level = 0
        level_cnt = 0
        child_flag = False
        root, level = queue.pop(0)

        print(f"[{root.mbr.to_str()}", end="")

        if root.is_leaf:
            len_entries = len(root.entries)
            for entry in root.entries:
                if len_entries == len(root.entries):
                    print("]-[", end="")
                len_entries -= 1
                if len_entries == 0:
                    print(f"{entry.to_str()}]", end="")
                else :
                    print(f"{entry.to_str()}, ", end="")
            return ""
        child_len = len(root.children)
        # print("child len : ", child_len)
        if root.children:
            for child in root.children:
                queue.append((child, level + 1))
            child_flag = True
        else :
            print("]-[", end="")
        
        child_temp_len = 0
        # print("start queue")
        while queue:
            # Dequeue a node and its level
            node, level = queue.pop(0)
            child_temp_len += len(node.children)
            if node.is_leaf:
                leaf_queue.append(node)

            level_cnt += 1
            if level > current_level:
                print(f"]-[", end="")
                # print("current level : ", current_level, "level : ", level)                
                current_level = level
                level_cnt = 0
                if current_level > 1:
                    child_len = child_temp_len
                # print("child len : ", child_len)
                

            # Print the node's mbr
            # print(level_cnt, " " , child_len, end="")
            if level_cnt == child_len - 1:
                print(f"{node.mbr.to_str()}", end="")
            else :
                print(f"{node.mbr.to_str()}, ", end="")


            # Enqueue the node's children
            if node.children:
                for child in node.children:
                    queue.append((child, level + 1))

        # Print a newline at the end
        if child_flag:
            leafs_all_entries = 0
            for leaf in leaf_queue:
                leafs_all_entries += len(leaf.entries)
            print("]-[", end="")
            leaf_cnt = 0
            for leaf in leaf_queue:
                for entry in leaf.entries:
                    leaf_cnt += 1
                    if leaf_cnt == leafs_all_entries:
                        print(entry.to_str(), end="]")
                        break
                    else :
                        print(entry.to_str(), end=", ")
        return ""

        raise NotImplementedError("Implement this function")
    """
    END OF IMPLEMENTATION OF PRINT    
    """