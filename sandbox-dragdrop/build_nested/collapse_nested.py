import argparse

from node import Node

def collapse_stack(visit, root):
    stack = [root]
    visited = set()
    while stack:
        node = stack.pop()
        visit(node)
        visited.add(node)
        if not node.children:
            pass
        else:
            for subnode in node.children:
                if subnode not in visited:
                    stack.append(subnode)

def collapse(predicate, root, path=None, depth=0):
    if path and not root.children:
        yield path
    else:
        for node in root.children:
            if predicate(root.value):
                if not path:
                    path = []
                path.append((depth, root))
            yield from collapse(predicate, node, path, depth+1)

def run():
    tree = Node('root', [
        Node('a', [
            Node('1', [
                Node('aa', [
                    Node('11', [
                        Node('aaa'),
                    ]),
                ]),
            ])
        ]),
        Node('b', [
            Node('2', [
                Node('bb'),
            ])
        ]),
        Node('c', [
            Node('3', [
                Node('cc', [
                    Node('33', [
                        Node('ccc'),
                    ]),
                ]),
            ])
        ]),
    ])
    for path in collapse(str.isalpha, tree):
        for depth, node in path:
            print(' '*depth, node.value)
        print()

def main(argv=None):
    """
    """
    parser = argparse.ArgumentParser()
    args = parser.parse_args(argv)
    run()

if __name__ == '__main__':
    main()
