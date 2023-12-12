
from abc import abstractmethod, ABC
#Abstract Queue Interface:

class Queue(ABC):
    @abstractmethod
    def enqueue(self, element):
        pass

    @abstractmethod
    def dequeue(self):
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


# Implementation 1: ListQueue
class ListQueue(Queue):
    def __init__(self):
        self.items = []

    def enqueue(self, element):
        self.items.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)

# Implementation 2: LinkedQueue
class LinkedQueue(Queue):
    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def enqueue(self, element):
        new_node = Node(element)
        if self.is_empty():
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if not self.is_empty():
            dequeued_data = self.front.data
            self.front = self.front.next
            self.size -= 1
            return dequeued_data

    def peek(self):
        if not self.is_empty():
            return self.front.data

    def is_empty(self):
        return self.size == 0

    def size(self):
        return self.size

# Implementation 3: PythonListQueue
class PythonListQueue(Queue):
    def __init__(self):
        self.items = []

    def enqueue(self, element):
        self.items.append(element)

    def dequeue(self):
        if not self.is_empty():
            return self.items.pop(0)

    def peek(self):
        if not self.is_empty():
            return self.items[0]

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


# testing
def test_list_queue():
    queue = ListQueue()

    # Test enqueue and peek
    queue.enqueue(1)
    assert queue.peek() == 1

    queue.enqueue(2)
    queue.enqueue(3)
    assert queue.peek() == 1

    # Test dequeue
    dequeued = queue.dequeue()
    assert dequeued == 1
    assert queue.peek() == 2

    # Test is_empty and size
    assert not queue.is_empty()
    assert queue.size() == 2

    # Test dequeue until empty
    queue.dequeue()
    queue.dequeue()
    assert queue.is_empty()
    assert queue.size() == 0

test_list_queue()
