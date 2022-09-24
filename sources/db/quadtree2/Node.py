from enum import IntEnum
from copy import deepcopy
from numpy import hypot as distance

from items.MoodVec import MoodVec
from items.Song import Song


class ChildDirection(IntEnum):
    nw = 0
    ne = 1
    se = 2
    sw = 3


class Point:
    """
    A Point item represents a point in a 2D space by (x,y).
    Each Point has a payload of a Song object.
    """

    def __init__(self, x: float = 0.00, y: float = 0.00, payload: Song = None):
        self.x, self.y = x, y
        self.payload = payload

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            raise AttributeError(f"Can't measure distance between Point and {type(other)}")

        return distance(self.x - other_x, self.y - other_y)


class Frame:
    """
        A rectangle frame defined by the following:
        cx - rectangle's center x value
        cy - rectangle's center y value
        w - width
        h - height
    """
    def __init__(self, top_left: Point = Point(x=0.0, y=1.0),
                 bottom_right: Point = Point(x=1.0, y=0.0)):
        self.top_left = top_left
        self.bottom_right = bottom_right

    def __repr__(self):
        return f"TL: {str(self.top_left)}, BR: {str(self.bottom_right)}"

    def __str__(self):
        return self.__repr__()

    def contains(self, point: Point) -> bool:
        """
        The contains methods checks if the Rectangle contains a given point and returns a boolean indicates the answer.
        :param point: A Point object.
        :return: True if the point is inside the borders.
        """
        return (self.top_left.x <= point.x < self.bottom_right.x and
                self.bottom_right.y <= point.y < self.top_left.y)

    def find_location(self, point: Point) -> ChildDirection:
        is_north = self.bottom_right.y <= point.y < (self.bottom_right.y + self.top_left.y / 2)
        is_west = self.top_left.x < point.x <= (self.top_left.x + self.bottom_right.x / 2)

        if is_north:
            return ChildDirection.nw if is_west else ChildDirection.ne
        return ChildDirection.sw if is_west else ChildDirection.se

    def generate_subframe(self, direction: ChildDirection):
        """
        Divides this nodes into 4 new children nodes: \n
        - nw - Northwestern child (Top-Left)
        - ne - Northeastern child (Top-Right)|
        - se - Southeastern child (Bottom-Right)|
        - sw - Southwestern child (Bottom-Left)
        :return: None.
        """
        top_left = deepcopy(self.top_left)
        bottom_right = deepcopy(self.bottom_right)

        x_step = (self.bottom_right.x - self.top_left.x) / 2
        y_step = (self.bottom_right.y - self.top_left.y) / 2

        match direction:
            case ChildDirection.nw:
                bottom_right.x += x_step
                bottom_right.y -= y_step
            case ChildDirection.ne:
                top_left.x -= x_step
                bottom_right.y += y_step
            case ChildDirection.se:
                top_left.x -= x_step
                top_left.y -= y_step
            case ChildDirection.sw:
                top_left.y -= y_step
                bottom_right.x -= x_step

        return Frame(top_left=top_left, bottom_right=bottom_right)


class NodeData:

    def __init__(self, position: Point, data: Song = None):
        self.position = position
        self.data = data

    def __repr__(self):
        if self.data is None:
            return f"<{repr(self.position)}"
        return f"<{repr(self.position)} | {self.data.title} by: {self.data.artist}>"

    def __str__(self):
        return self.__repr__()


class Node:

    def __init__(self, frame: Frame = None):
        self.frame = frame

        self.data = None
        self.children = [None] * 4
        self.parent = None
        self.is_divided = False

    def add_child_in_direction(self, child, direction: int):
        assert (isinstance(child, Node) and 0 <= direction < 4)
        child.parent = self
        self.children[direction] = child

    def add_child(self, direction: ChildDirection):
        candidate_node = Node()
        candidate_node.parent = self
        candidate_node.frame = self.frame.generate_subframe(direction=direction)
        self.is_divided = True
        self.children[direction] = candidate_node

    def insert(self, node_data):

        # assert isinstance(node, Node)

        # Current NodeData's position is not in the current Node's frame
        if not self.frame.contains(point=node_data.position):
            return

        # Current Node has no data AND it's not divided i.e. an empty square Node
        if self.data is None and not self.is_divided:
            self.data = node_data
            return

        data_position = self.frame.find_location(point=node_data.position)  # In what position this NodeData lies within the current Node's frame
        candidate_node = self.children[data_position]  # The candidate child-Node in which we wish to insert the NodeData
        if self.data is not None:  # The current Node already holds NodeData
            self.add_child(direction=data_position)
            self_data_location = self.frame.find_location(point=self.data.position)
            if self_data_location == data_position:
                # Delegation
                candidate_node.data = self.data
                self.data = None
            candidate_node.insert(node_data=node_data)
            return
        if candidate_node is None:
            self.add_child(direction=data_position)
        candidate_node.insert(node_data=node_data)
        return

        # # Has Data
        # if self.children[data_position] is None:
        #
        #     self.divide_direction(direction=data_position)
        #     return
        #
        # # Also has a child in this direction
        # self.children[data_position].insert(node=node_data)

    # def search(self, node: Node):
    #     node_location = self.frame.find_location(point=node.position)
    #
    #     if self.children[node_location] is None:
    #         return None
    #
    #     if self.node.position == node.position:
    #         return self


class Quadtree:

    root: Node

    def __init__(self):
        self.root = Node(frame=Frame(top_left=Point(x=0.0, y=1.0),
                                     bottom_right=Point(x=1.0,y=0.0)))
    def insert_data(self, data: Song = None):
        node_data = NodeData(position=Point(x=data.mood_vec.energy, y=data.mood_vec.valence), data=data)
        self.root.insert(node_data=node_data)




