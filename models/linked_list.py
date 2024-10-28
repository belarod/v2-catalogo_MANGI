class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

class LinkedList:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LinkedList, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        self.head = None
        
    def __str__(self):
        values = []
        current = self.head
        while current is not None:
            values.append(str(current.value))
            current = current.next
        return " -> ".join(values)
        
    def get_array(self):
        array = []
        current = self.head
        while current is not None:
            array.append(current.value)
            current = current.next
        return array
    
    def __len__(self):
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count
        
    def add(self, value):
        new_node = Node(value)
        
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
            
    def remove(self, value):
        current = self.head
        anterior = None
        
        while current is not None:
            if current.value == value:
                if anterior is None:
                    self.head = current.next
                else:
                    anterior.next = current.next
                return
            anterior = current
            current = current.next
            
    def clear(self):
        self.head = None