# Singly Linked Lists

A singly linked list is a data structure that holds elements in a unidirectional pattern, where it has both a head and tail.

This can be seen in this diagram here:

![Singly Linked List](data_structures/tutorials/assets/singly_linked_list.png)

Each node in this list points to another node, and the tail points to null.

We can define nodes as such:

```python
class Node():
    def __init__(self, value):
        self.value = value
        self.next = None
    def __repr__(self):
        return f'{self.value}'
```

## Node Components

1. `self.value`: holds the current value of the node
2. `self.next`: points to the next node in the chain
3. `__repr__`: stands for represents. When you invoke a print statement, it will print the value of the node

To contain all these nodes, we need to implement a container structure that will keep track of them.

This can be done by doing something like this:

```python
class LinkedList():
    def __init__(self, head=None, tail=None):
        self.head = head
        self.tail = tail
```

## Linked List Components

1. `self.head`: pointing to the front of the list
2. `self.tail`: pointing to the end of the list

## Inserting

We can insert into the list in order as so:

```python
container = [4, 6, 8, 2]
for element in container:
    linked_list.add_front(Node(element))
# 4 -> 6 -> 8 -> 2
# would be the representation of the list
```

The algorithm goes something like this:

1. Check if the node is null; if it is, set the new node to the head and tail
2. If the head is not null, set a temporary variable holding head
    a. Iterate over the collection until you reach the end
    b. Insert the node and set it to the tail

Implemented in code:

```python
def add_front(self, node: Node):
    if not(isinstance(node, Node)):
        raise ValueError
    if not(self.head):
        self.head = self.tail = node
        return
    current = self.head
    # iterate to the end
    while(current.next):
        current = current.next
    # before: 1 -> 2 -> NULL
    current.next = node
    # after: 1 -> 2 -> 3 -> NULL
```

You might notice the `isinstance` check at the top.
This step is normally unnecessary but is good practice to get into when programming.
It allows you to stop errors faster as you are ensuring the parameters passed into the function are what they are supposed to be.
