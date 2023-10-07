class Node:

    def __init__(self, value, children=None):
        self.value = value
        if children is None:
            children = []
        self.children = children
