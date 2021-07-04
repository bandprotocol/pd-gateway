from typing import Dict

class LinkedNode:
    def __init__(self, key: str, val: any):
        self.key = key
        self.val = val
        self.next: LinkedNode = None
        self.prev: LinkedNode = None

class LRUCache:
    def __init__(self, maxsize: int):
        self.maxsize = maxsize
        self.currsize = 0
        self.d: Dict[str, LinkedNode] = {}
        self.head: LinkedNode = None
        self.tail: LinkedNode = None

    def __remove_by_key(self, key: str) -> LinkedNode:
        if key not in self.d:
            return None

        node = self.d[key]
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None
        return node

    def __insert_head(self, node: LinkedNode):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            self.head = self.head.prev

    def __remove_tail(self) -> LinkedNode:
        if self.tail is None:
            return None

        node = self.tail
        self.tail = node.prev
        return node
        
    def is_hit(self, key: str) -> bool:
        return key in self.d

    def put(self, key: str, val: any) -> any:
        if self.currsize == self.maxsize:
            self.__remove_tail()

        if key in self.d:
            node = self.__remove_by_key(key)
            self.__insert_head(node)
        else:
            self.__insert_head(LinkedNode(key, val))

        self.d[key] = self.head
        self.currsize += 1

            
