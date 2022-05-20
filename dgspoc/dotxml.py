"""Module containing the logic for XML instance as dot object"""

from xml.etree import ElementTree

from dgspoc.utils import DotObject


class DotElement(ElementTree.Element):

    def __init__(self, tag, attrib=None, **extra):
        attrib = attrib or {}
        super().__init__(tag, attrib=attrib, **extra)
        self.parent = None

    def __getattribute__(self, item):
        result = super().__getattribute__(item)
        if item == 'attrib':
            if isinstance(result, DotElement):
                return result
            elif isinstance(result, dict):
                dot_object = DotObject(result)
                return dot_object
            else:
                return result
        else:
            return result

    @property
    def has_children(self):
        return len(self) == 0

    @property
    def children(self):
        for child in self:
            child.parent = self
            yield child

    @property
    def is_leaf(self):
        return not self.has_children

    @property
    def prev_sibling(self):
        if isinstance(self.parent, self.__class__):
            lst = list(self.parent.children)
            index = lst.index(self)
            if index > 0:
                return lst[index - 1]
            else:
                return None
        else:
            return None

    @property
    def next_sibling(self):
        if isinstance(self.parent, self.__class__):
            lst = list(self.parent.children)
            index = lst.index(self)
            if index < len(lst) - 1:
                return lst[index + 1]
            else:
                return None
        else:
            return None

    @classmethod
    def try_to_get(cls, node):
        if isinstance(node, cls):
            return node
        elif ElementTree.iselement(node):
            new_node = cls(node.tag, attrib=node.attrib)
            return new_node
        else:
            return node

    def find(self, path, namespaces=None):
        result = super().find(path, namespaces=namespaces)
        for index, item in enumerate(result):
            new_item = self.try_to_get(item)
            if new_item != item:
                result[index] = new_item
        return result

    def findall(self, path, namespaces=None):
        result = super().findall(path, namespaces=namespaces)
        for index, item in enumerate(result):
            new_item = self.try_to_get(item)
            if new_item != item:
                result[index] = new_item
        return result

    def iterfind(self, path, namespace=None):
        is_iter = False
        result = super().iterfind(path, namespaces=namespace)
        for node in result:
            is_iter = True
            new_node = self.try_to_get(node)
            yield new_node

        if not is_iter:
            yield from ()

    def iter(self, tag=None):
        is_iter = False
        result = super().iter(tag=tag)
        for node in result:
            is_iter = True
            new_node = self.try_to_get(node)
            yield new_node

        if not is_iter:
            yield from ()


class DotElementTree(ElementTree.ElementTree):

    def __init__(self, element=None, file=None):
        new_element = DotElement.try_to_get(element)
        super().__init__(element=new_element, file=file)

    def getroot(self):
        root = super().getroot()
        new_root = DotElement.try_to_get(root)
        return new_root

    def parse(self, source, parser=None):
        super().parse(source, parser=parser)
        root = self.getroot()
        return root


iselement = ElementTree.iselement


SubElement = ElementTree.SubElement


Comment = ElementTree.Comment


ProcessingInstruction = ElementTree.ProcessingInstruction


PI = ElementTree.PI


register_namespace = ElementTree.register_namespace


tostring = ElementTree.tostring


tostringlist = ElementTree.tostringlist


dump = ElementTree.dump


indent = ElementTree.indent


def parse(source, parser=None):
    tree = DotElementTree()
    tree.parse(source, parser)
    return tree
