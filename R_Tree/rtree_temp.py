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
            print("Inserting Root", rect.to_str())
            self.root.entries.append(rect)
            self.root.update_node_mbrs()

            # split
            if len(self.root.entries) <= self.max_entries:
                print(self.root.mbr.to_str())
                return
            else :
                print("Splitting Root")
                node_1 = RTreeNode()
                node_2 = RTreeNode()
                entries = self.root.entries

                for entry in entries:
                    print(entry.to_str())

                max_area = 0
                max_entries = []

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

                print("Max Area : ", max_area)
                print("Max Entries : ", max_entries[0].to_str(), max_entries[1].to_str())
                        
                node_1.entries.append(max_entries[0])
                node_1.update_node_mbrs()
                node_2.entries.append(max_entries[1])
                node_2.update_node_mbrs()

                for entry in entries:
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
                        if diff_area_1 == diff_area_2:
                            if node_1.mbr.area() <= node_2.mbr.area():
                                node_1 = temp_1
                                print("count : ", cnt , " win node 1")
                            else :
                                node_2 = temp_2
                                print("count : ", cnt , " win node 2")
                        elif diff_area_1 < diff_area_2:
                            node_1 = temp_1
                            print("count : ", cnt , " win node 1")
                        else :
                            node_2 = temp_2
                            print("count : ", cnt , " win node 2")
                    cnt += 1
                    print("{Node 1} : ", node_1.mbr.to_str())
                    print("{Node 2} : ", node_2.mbr.to_str())

                node_1.update_node_mbrs()
                print("Node 1 : ", node_1.mbr.to_str())
                node_2.update_node_mbrs()
                print("Node 2 : ", node_2.mbr.to_str())

                self.root = RTreeNode()
                self.root.children.append(node_1)
                self.root.children.append(node_2)
                self.root.is_leaf = False
                self.root.entries = []
                # self.root.entries.append(node_1.mbr)
                # self.root.entries.append(node_2.mbr)
                self.root.update_node_mbrs()


            return
        else :
            # find leaf
            print("Inserting leaf", rect.to_str())
            leaf_node = self.root
            while (leaf_node.is_leaf == False):
                # temp_node = RTreeNode()
                # temp_node.entries.append(rect)
                # temp_node.update_node_mbrs()
                # leaf_node.children.append(temp_node)
                # leaf_node.update_node_mbrs()
                # leaf_node.children.remove(temp_node)
                print("entering while")
                min_child = leaf_node.children[0]
                for child in leaf_node.children:
                    print("entering for")
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
                    if temp_1.mbr.area() > temp_2.mbr.area():
                        min_child = child

                leaf_node = min_child

                    
            print("Im here Shit")
            leaf_node.entries.append(rect)
            leaf_node.update_node_mbrs()
            
            
            print("Leaf node entries : ", len(leaf_node.entries))
            while( len(leaf_node.entries) > self.max_entries):
                # find parent
                parent_node = self.root
                end_flag = True
                while(parent_node.mbr.within(leaf_node.mbr) == False & parent_node.is_leaf == False):
                    print("hey")
                    for child in parent_node.children:
                        print("here!")
                        print(child)
                        if child.is_leaf == True:
                            print("true!!")
                            end_flag = False
                            break
                        if child.mbr.within(leaf_node.mbr):
                            parent_node = child
                            break
                    if end_flag == False:
                        break

                print("Splitting leaf")
                node_1 = RTreeNode()
                node_2 = RTreeNode()
                if leaf_node.is_leaf:
                    node_1.is_leaf = True
                    node_2.is_leaf = True
                entries = leaf_node.entries

                for entry in entries:
                    print(entry.to_str())
                    
                max_area = 0
                max_entries = []

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

                print("Max Area : ", max_area)
                print("Max Entries : ", max_entries[0].to_str(), max_entries[1].to_str())
                            
                node_1.entries.append(max_entries[0])
                node_1.update_node_mbrs()
                node_2.entries.append(max_entries[1])
                node_2.update_node_mbrs()

                for entry in entries:
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
                        if diff_area_1 == diff_area_2:
                            if node_1.mbr.area() <= node_2.mbr.area():
                                node_1 = temp_1
                                print("count : ", cnt , " win node 1")
                            else :
                                node_2 = temp_2
                                print("count : ", cnt , " win node 2")
                        elif diff_area_1 < diff_area_2:
                            node_1 = temp_1
                            print("count : ", cnt , " win node 1")
                        else :
                            node_2 = temp_2
                            print("count : ", cnt , " win node 2")
                    cnt += 1
                    print("{Node 1} : ", node_1.mbr.to_str())
                    print("{Node 2} : ", node_2.mbr.to_str())

                node_1.update_node_mbrs()
                print("Node 1 : ", node_1.mbr.to_str())
                node_2.update_node_mbrs()
                print("Node 2 : ", node_2.mbr.to_str())

                print("Leaf node : ", leaf_node.mbr.to_str())
                print("Parent node : ", parent_node.mbr.to_str())
                print("Parent children num : ", len(parent_node.children))
                for child in parent_node.children:
                    print("Child node : ", child.mbr.to_str())
                for entries in parent_node.entries:
                    print("Parent entries : ", entries.to_str())
                    # print("type of entries : ", type(entries))
                parent_node.children.remove(leaf_node)
                # parent_node.entries.remove(leaf_node.mbr)
                parent_node.children.append(node_1)
                parent_node.children.append(node_2)
                # leaf_node.is_leaf = False
                # parent_node.entries.append(node_1.mbr)
                # parent_node.entries.append(node_2.mbr)
                parent_node.update_node_mbrs()
                leaf_node = parent_node

            self.root.update_node_mbrs()
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
        print("Deleting leaf", delete_rectangle.to_str())
        target_node = self.root
        silk_load = []
        silk_load.append(target_node)
        
        if target_node.children[0].is_leaf == True:
            for child in target_node.children:
                print("t child : ", child.mbr.to_str())
                if child.mbr.overlap(delete_rectangle):
                    print("added")
                    target_node = child
                    silk_load.append(target_node)
                    break
        else :
            while(target_node.mbr.within(delete_rectangle) == True & target_node.is_leaf == False):
                for child in target_node.children:
                    print("child : ", child.mbr.to_str())
                    if child.mbr.within(delete_rectangle):
                        target_node = child
                        silk_load.append(target_node)
                        break
        
        same_one = target_node.entries[0]
        for entry in target_node.entries:
            print(entry.to_str())
            print("entry pos : ", entry.x1, entry.y1, entry.x2, entry.y2)
            if delete_rectangle.exact_overlap(entry):
                print("it is same!!!!!")
                same_one = entry

        print("delete rect : ", delete_rectangle.to_str())
        print("delete pos : ", delete_rectangle.x1 , delete_rectangle.y1, delete_rectangle.x2, delete_rectangle.y2)
        target_node.entries.remove(same_one)


        if len(target_node.entries) < self.min_entries:
            print("re insert")
            node_flag = False
            adding_rect = target_node.entries[0]
            for node in silk_load[::-1]:
                print("Iam : ", node.mbr.to_str())
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

            return [same_one]
        else :
            print("just delete")

            for node in silk_load[::-1]:
                print("Iam updating node : ", node.mbr.to_str())
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
        print("Searching leaf", search_rectangle.to_str())

        target_node = self.root
        search_entries = []
        
        if target_node.children[0].is_leaf == True:
            for child in target_node.children:
                print("t child : ", child.mbr.to_str())
                if child.mbr.overlap(search_rectangle):
                    print("searching.. : ", child.mbr.to_str())
                    target_node = child
                    # search_entries.append(target_node.entries)
                    break
        else :
            while(target_node.mbr.within(search_rectangle) == True & target_node.is_leaf == False):
                for child in target_node.children:
                    print("child : ", child.mbr.to_str())
                    if child.mbr.within(search_rectangle):
                        target_node = child
                        # search_entries.append(target_node.entries)
                        break
        
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
        child_len = len(root.children)
        if root.children:
            for child in root.children:
                queue.append((child, level + 1))
            child_flag = True
        else :
            print("]-[", end="")

        while queue:
            # Dequeue a node and its level
            node, level = queue.pop(0)
            if node.is_leaf:
                leaf_queue.append(node)

            level_cnt += 1
            if level > current_level:
                print(f"]-[", end="")
                current_level = level
                level_cnt = 0

            # Print the node's mbr
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
        return

        raise NotImplementedError("Implement this function")
    """
    END OF IMPLEMENTATION OF PRINT    
    """