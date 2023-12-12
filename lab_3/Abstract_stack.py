#Abstract stack:
from abc import ABC, abstractmethod

class Stack(ABC):
    @abstractmethod
    def push(self, element):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def peek(self):
        pass

    @abstractmethod
    def is_empty(self):
        pass

    @abstractmethod
    def size(self):
        pass

# Implementation 1: ListStack
class ListStack(Stack):
    def __init__(self):
        self.items = []

    def push(self, element):
        self.items.append(element)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

# Implementation 2: LinkedStack
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedStack(Stack):
    def __init__(self):
        self.top = None
        self.size = 0

    def push(self, element):
        new_node = Node(element)
        new_node.next = self.top
        self.top = new_node
        self.size += 1

    def pop(self):
        if not self.is_empty():
            popped_data = self.top.data
            self.top = self.top.next
            self.size -= 1
            return popped_data

    def peek(self):
        if not self.is_empty():
            return self.top.data

    def is_empty(self):
        return self.size == 0

    def size(self):
        return self.size

# Implementation 3: PythonListStack
class PythonListStack(Stack):
    def __init__(self):
        self.items = []

    def push(self, element):
        self.items.append(element)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()

    def peek(self):
        if not self.is_empty():
            return self.items[-1]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)




# testing
def test_list_stack():
    stack = ListStack()

    # Test push and peek
    stack.push(1)
    assert stack.peek() == 1

    stack.push(2)
    stack.push(3)
    assert stack.peek() == 3

    # Test pop
    popped = stack.pop()
    assert popped == 3
    assert stack.peek() == 2

    # Test is_empty and size
    assert not stack.is_empty()
    assert stack.size() == 2

    # Test pop until empty
    stack.pop()
    stack.pop()
    assert stack.is_empty()
    assert stack.size() == 0

test_list_stack()
