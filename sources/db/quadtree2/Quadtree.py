from enum import IntEnum

from numpy import hypot as distance
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


class Quadtree:

    def __init__(self, frame: Frame = Frame()):
        self.frame = frame

        self.node_data = None
        self.children = [None] * 4
        self.parent = None
        self.is_divided = False

    def add_child_in_direction(self, child, direction: int):
        assert (isinstance(child, Quadtree) and 0 <= direction < 4)
        child.parent = self
        self.children[direction] = child

    def divide_direction(self, direction: ChildDirection):
        """
        Divides this nodes into 4 new children nodes: \n
        - nw - Northwestern child (Top-Left)
        - ne - Northeastern child (Top-Right)|
        - se - Southeastern child (Bottom-Right)|
        - sw - Southwestern child (Bottom-Left)
        :return: None.
        """
        top_left = self.frame.top_left
        bottom_right = self.frame.bottom_right

        x_step = self.frame.bottom_right.x - self.frame.top_left.x / 2
        y_step = self.frame.bottom_right.y - self.frame.top_left.y / 2

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

        frame = Frame(top_left=top_left, bottom_right=bottom_right)

        child = Quadtree(frame=frame)
        child.insert(node=self.node_data)

        self.children[direction] = child
        if child.node_data is not None:
            self.node_data = None

        self.is_divided = True

    def insert(self, node):

        assert isinstance(node, Quadtree)

        # Current the node is not in the current Quad's frame
        if not self.frame.contains(point=node.position):
            return

        if self.node_data is None and not self.is_divided:
            self.node_data = node
            return

        node_location = self.frame.find_location(point=node.position)

        if self.children[node_location] is None:
            self.divide_direction(direction=node_location)
            return

        self.children[node_location].insert(node=node)

    # def search(self, node: Node):
    #     node_location = self.frame.find_location(point=node.position)
    #
    #     if self.children[node_location] is None:
    #         return None
    #
    #     if self.node.position == node.position:
    #         return self






