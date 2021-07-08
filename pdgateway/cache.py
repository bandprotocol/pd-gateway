from typing import Dict

from requests.api import head

class LinkedNode:
    def __init__(self, key: str, val: any):
        self.key = key
        self.val = val
        self.next: LinkedNode = None
        self.prev: LinkedNode = None

class LRUCache:
    def __init__(self, maxsize: int = 128):
        self.maxsize = maxsize
        self.currsize = 0
        self.d: Dict[str, LinkedNode] = {}
        self.head: LinkedNode = None
        self.tail: LinkedNode = None

    def __remove_by_key(self, key: str) -> LinkedNode:
        if key not in self.d:
            return None

        node = self.d[key]
        if node is not self.head:
            node.prev.next = node.next
        if node is not self.tail:
            node.next.prev = node.prev
        
        if node is self.head:
            self.head = self.head.next
        elif node is self.tail:
            self.tail = self.tail.prev

        node.prev = None
        node.next = None

        self.d.pop(key, None)
        self.currsize -= 1

        return node

    def __insert_head(self, node: LinkedNode):
        if self.head is None:
            self.head = self.tail = node
        else:
            self.head.prev = node
            node.next = self.head
            self.head = self.head.prev
        
        self.d[node.key] = self.head
        self.currsize += 1

    def __remove_tail(self) -> LinkedNode:
        if self.tail is None:
            return None

        node = self.tail
        self.tail = node.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = None

        self.d.pop(node.key, None)
        self.currsize -= 1

        return node
        
    def is_hit(self, key: str) -> bool:
        return key in self.d

    def put(self, key: str, val: any) -> any:
        if key in self.d:
            self.__remove_by_key(key)
            self.__insert_head(LinkedNode(key, val))
        else:
            if self.currsize == self.maxsize and self.maxsize > 0:
                self.__remove_tail()
            self.__insert_head(LinkedNode(key, val))

            
