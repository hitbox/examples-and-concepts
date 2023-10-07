import argparse

from operator import itemgetter
from pprint import pprint
from xml.etree import ElementTree as ET

# two different walk functions?
# one each, for when we hit a dropzone and when we hit a draggable?

def is_draggable(element):
    return element.attrib.get('type') == 'draggable'

def is_dropzone(element):
    return element.attrib.get('type') == 'dropzone'

def walk_filter(element, predicate):
    if predicate(element):
        yield element
    for child in element:
        yield from walk_filter(child, predicate)

def walk_draggable(element):
    draggable = {
        'type': 'draggable',
        'data': eval(element.attrib['data']),
    }
    if any(walk_filter(element, is_dropzone)):
        # draggable has dropzone in it, continue walking
        draggable['dropzone'] = list(obj for child in element for obj in walk(child))
    yield draggable

def walk_dropzone(element):
    yield {
        element.attrib['key']: list(
            obj for child in element for obj in walk(child)
            if obj and obj.get('type') in ('draggable', 'dropzone')
        ),
    }

def walk(element):
    if is_draggable(element):
        generator = walk_draggable(element)
    elif is_dropzone(element):
        generator = walk_dropzone(element)
    else:
        generator = (obj for child in element for obj in walk(child))
    yield from generator

def main(argv=None):
    """
    Working out recursive function to change XML (HTML) state into nested
    object structure.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'htmlfile',
    )
    args = parser.parse_args(argv)

    tree = ET.parse(args.htmlfile)
    root = tree.getroot()

    result = list(walk(root))
    pprint(result)

if __name__ == '__main__':
    main()
