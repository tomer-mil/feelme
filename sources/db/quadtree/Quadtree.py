from copy import deepcopy
from enum import IntEnum
from numpy import hypot as distance
from items.Song import Song

################
# Inspiration from::
# - https://www.geeksforgeeks.org/quad-tree/,
# - https://scipython.com/blog/quadtrees-2-implementation-in-python/
# - https://geidav.wordpress.com/2017/12/02/advanced-octrees-4-finding-neighbor-nodes/ (https://github.com/geidav/quadtree-neighbor-finding/blob/b5fc4527271b4420eaf8cfb4ec66926f08cb881f/neighbors.py)
#
# Visualization Example: https://ericandrewlewis.github.io/how-a-quadtree-works/
################


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

    def __init__(self, x: float = 0.00, y: float = 0.00):
        self.x, self.y = x, y

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
        is_south = self.bottom_right.y <= point.y < ((self.bottom_right.y + self.top_left.y) / 2)
        is_west = self.top_left.x <= point.x < ((self.top_left.x + self.bottom_right.x) / 2)

        if is_south:
            return ChildDirection.sw if is_west else ChildDirection.se
        return ChildDirection.nw if is_west else ChildDirection.ne

    def generate_subframe(self, direction: ChildDirection):
        """
        Divides this nodes into 4 new children nodes: \n
        - nw - Northwestern child (Top-Left)
        - ne - Northeastern child (Top-Right)|
        - se - Southeastern child (Bottom-Right)|
        - sw - Southwestern child (Bottom-Left)
        :return: None.
        """
        top_left = Point(x=self.top_left.x, y=self.top_left.y)
        bottom_right = Point(x=self.bottom_right.x, y=self.bottom_right.y)

        x_step = (bottom_right.x - top_left.x) / 2
        y_step = (top_left.y - bottom_right.y) / 2

        match direction:
            case ChildDirection.nw:
                bottom_right.x -= x_step
                bottom_right.y += y_step
            case ChildDirection.ne:
                top_left.x += x_step
                bottom_right.y += y_step
            case ChildDirection.se:
                top_left.x += x_step
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
        return f"<{str(self.position)} | {self.data.title} by: {self.data.artist}>"

    def __str__(self):
        return self.__repr__()

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, deepcopy(v, memo))
        return result


class Node:

    def __init__(self, frame: Frame = None):
        self.frame = frame

        self.data = None
        self.children = [None] * 4
        self.parent = None
        self.is_divided = False

    def __repr__(self):
        has_nw = self.children[ChildDirection.nw] is not None
        has_ne = self.children[ChildDirection.ne] is not None
        has_se = self.children[ChildDirection.se] is not None
        has_sw = self.children[ChildDirection.sw] is not None

        has_data = "No Data Found" if self.data is None else self.data

        return f"Data: {has_data} | NW: {has_nw}, NE: {has_ne}, SE: {has_se}, SW: {has_sw}"

    def add_child(self, direction: ChildDirection):
        child_node = Node()
        child_node.parent = self
        child_node.frame = self.frame.generate_subframe(direction=direction)

        self.is_divided = True
        self.children[direction] = child_node

        return self.children[direction]

    def insert(self, node_data):

        assert isinstance(node_data, NodeData)

        # Current NodeData's position is not in the current Node's frame
        if not self.frame.contains(point=node_data.position):
            self.parent.data = node_data if self.parent.data is None else self.parent.data
            return

        # Node is not divided
        if not self.is_divided:
            # Node has no data
            if self.data is None:  # Stop Condition
                self.data = node_data
                return

            # Node has data
            else:
                nd_direction = self.frame.find_location(point=node_data.position)
                data_direction = self.frame.find_location(point=self.data.position)

                child = self.add_child(direction=nd_direction)  # By reference?
                assert isinstance(child, Node)

                # Same direction
                if nd_direction == data_direction:
                    self.delegate_data(child=child)
                    child.insert(node_data=node_data)
                    return

                # New direction
                else:
                    child.data = node_data
                    return

        # Node is divided
        else:
            nd_direction = self.frame.find_location(point=node_data.position)
            candidate_child = self.children[nd_direction]

            # Node has data
            if self.data is not None:

                # Has a child with the same direction as node_data
                if candidate_child is not None:
                    assert isinstance(candidate_child, Node)
                    candidate_child.insert(node_data=node_data)
                    return

                # Does not have a child with the same direction as node_data
                else:
                    data_direction = self.frame.find_location(point=self.data.position)
                    child = self.add_child(direction=nd_direction)
                    assert isinstance(child, Node)

                    # The node's (self) data is in the same direction as node_data's direction
                    if nd_direction == data_direction:
                        self.delegate_data(child=child)
                        child.insert(node_data=node_data)
                        return

                    # Moves node_data to the new child
                    else:
                        child.data = node_data
                        return

            # Node does not have data
            else:

                # Does not have a child with the same direction as node_data
                if candidate_child is None:
                    self.data = node_data
                    return

                # Has a child with the same direction as node_data
                else:
                    candidate_child.insert(node_data=node_data)
                    return

    def delegate_data(self, child):
        child.data = deepcopy(self.data)
        self.data = None


class Quadtree:

    def __init__(self):
        self.root = Node(frame=Frame(top_left=Point(x=0.0, y=1.0),
                                     bottom_right=Point(x=1.0, y=0.0)))

        self.total_leaves = 0
        self.depth = 0

    def __repr__(self):
        return f"Data count: {self.total_leaves}"

    def insert_data(self, data: Song = None):
        node_data = NodeData(position=Point(x=data.mood_vec.energy, y=data.mood_vec.valence), data=data)
        self.root.insert(node_data=node_data)
        self.total_leaves += 1




