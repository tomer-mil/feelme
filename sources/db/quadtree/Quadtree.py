from copy import deepcopy
from typing import Any
from numpy import hypot as distance
from items.Song import Song


################
# Inspiration from:
# - https://www.geeksforgeeks.org/quad-tree/
# - https://scipython.com/blog/quadtrees-2-implementation-in-python/
# - https://geidav.wordpress.com/2017/12/02/advanced-octrees-4-finding-neighbor-nodes/ (https://github.com/geidav/quadtree-neighbor-finding/blob/b5fc4527271b4420eaf8cfb4ec66926f08cb881f/neighbors.py)
#
# Visualization Example: https://ericandrewlewis.github.io/how-a-quadtree-works/
################


class Direction:
    NW = 0
    NE = 1
    SE = 2
    SW = 3

    neighboring = {
        "N": (SE, SW),
        "S": (NE, NW),
        "W": (NE, SE),
        "E": (NW, SW)
    }

    @staticmethod
    def opposite_of(direction: int | str, relative_to: str = None):
        if isinstance(direction, int):
            assert isinstance(relative_to, str)
            is_horizontal = relative_to in {"N", "S"}
            if is_horizontal:
                return 3 - direction
            match direction:
                case Direction.NW: return Direction.NE
                case Direction.NE: return Direction.NW
                case Direction.SE: return Direction.SW
                case Direction.SW: return Direction.SE

        match direction:
            case "N": return "S"
            case "S": return "N"
            case "W": return "E"
            case "E": return "W"


    @staticmethod
    def split_direction(direction: str) -> tuple:
        assert isinstance(direction, str)
        assert direction in {"N", "S", "W", "E"}

        match direction:
            case "N":
                return Direction.NW, Direction.NE
            case "S":
                return Direction.SW, Direction.SE
            case "W":
                return Direction.NW, Direction.SW
            case "E":
                return Direction.NE, Direction.SE

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

    def find_location_in_frame(self, point: Point) -> int:
        is_south = self.bottom_right.y <= point.y < ((self.bottom_right.y + self.top_left.y) / 2)
        is_west = self.top_left.x <= point.x < ((self.top_left.x + self.bottom_right.x) / 2)

        if is_south:
            return Direction.SW if is_west else Direction.SE
        return Direction.NW if is_west else Direction.NE

    def find_frame_relative_direction(self, point: Point) -> list[str]:
        directions = []

        if self.bottom_right.y > point.y:  # is the frame to the North
            directions.append("N")
        if self.top_left.y < point.y:  # is the frame to the South
            directions.append("S")
        if self.top_left.x > point.x:  # is the frame to the East
            directions.append("E")
        if self.bottom_right.x < point.x:  # is the frame to the West
            directions.append("W")

        return directions

    def generate_subframe(self, direction: int):
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
            case Direction.NW:
                bottom_right.x -= x_step
                bottom_right.y += y_step
            case Direction.NE:
                top_left.x += x_step
                bottom_right.y += y_step
            case Direction.SE:
                top_left.x += x_step
                top_left.y -= y_step
            case Direction.SW:
                top_left.y -= y_step
                bottom_right.x -= x_step

        return Frame(top_left=top_left, bottom_right=bottom_right)

    def draw(self, ax, c='k', lw=1, **kwargs):
        top_left = Point(x=self.top_left.x, y=self.top_left.y)
        bottom_left = Point(x=self.top_left.x, y=self.bottom_right.y)

        bottom_right = Point(x=self.bottom_right.x, y=self.bottom_right.y)
        top_right = Point(x=self.bottom_right.x, y=self.top_left.y)

        ax.plot([top_left.x, top_right.x, bottom_right.x, bottom_left.x, top_left.x],
                [top_left.y, top_right.y, bottom_right.y, bottom_left.y, top_left.y])


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

    def __init__(self, frame: Frame = None, depth: int = 0):
        self.frame = frame

        self.data = None
        self.children = [None] * 4
        self.parent = None
        self.is_divided = False

        self.depth = depth
        self.external_point = None

    def __repr__(self):
        has_nw = self.children[Direction.NW] is not None
        has_ne = self.children[Direction.NE] is not None
        has_se = self.children[Direction.SE] is not None
        has_sw = self.children[Direction.SW] is not None

        has_data = "No Data" if self.data is None else self.data

        return f"Data: {has_data} | NW: {has_nw}, NE: {has_ne}, SE: {has_se}, SW: {has_sw}"

    def __str__(self):
        data = self.data if not None else "No Data"
        return f"Depth: {self.depth}; Frame: {self.frame}; Data: {data}"

    def is_leaf(self):
        return self.children == [None] * 4

    def add_child(self, direction: int, is_dummy: bool = False):
        child_node = Node(depth=self.depth + 1)
        child_node.parent = self
        child_node.frame = self.frame.generate_subframe(direction=direction)

        if not is_dummy:
            self.is_divided = True
            self.children[direction] = child_node

        return child_node

    def insert(self, node_data):

        assert isinstance(node_data, NodeData)

        # Current NodeData's position is not in the current Node's frame
        if not self.frame.contains(point=node_data.position):
            print("Not in frame!")
            return

        # Node is not divided
        if not self.is_divided:
            # Node has no data
            if self.data is None:  # Stop Condition
                self.data = node_data
                return

            # Node has data
            else:
                nd_direction = self.frame.find_location_in_frame(point=node_data.position)
                data_direction = self.frame.find_location_in_frame(point=self.data.position)

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
            nd_direction = self.frame.find_location_in_frame(point=node_data.position)
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
                    data_direction = self.frame.find_location_in_frame(point=self.data.position)
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

    def find_containing_node(self, point: Point):
        point_direction = self.frame.find_location_in_frame(point=point)
        if self.children[point_direction]:
            return self.children[point_direction].find_containing_node(point=point)
        return self

    def find_neighbors(self, children_directions: list[tuple]):

        neighbors_directions = []
        directions_to_filter = set()
        #  TODO: extract to method {
        for child_direction in children_directions:
            directions_to_filter.update(*child_direction[1])

        for direction in Direction.neighboring.keys():
            if direction not in directions_to_filter:
                neighbors_directions.append(direction)
        #  }
        neighbors = []
        for direction in neighbors_directions:
            neighbors.extend(self.find_neighbors_in_direction(direction=direction))

        return neighbors

    def get_relative_direction_of_children_to_point(self, point: Point) -> list[tuple]:
        assert isinstance(self.external_point, Point)

        child_and_directions_list = []

        for child_direction, child in enumerate(self.children):
            if child is not None:
                child_and_directions_list.append((child_direction, child.frame.find_frame_relative_direction(point=point)))
        return child_and_directions_list

    def find_candidates(self) -> list:
        children_directions = self.get_relative_direction_of_children_to_point(point=self.external_point)
        neighbors_candidates = self.find_neighbors(children_directions=children_directions)
        descendants_candidates = self.find_relevant_descendants(children_directions=children_directions)

        return ([*descendants_candidates, *neighbors_candidates, self] if self.data is not None
                else [*descendants_candidates, *neighbors_candidates])

    def get_neighbor_of_greater_or_equal_size(self, direction: str):
        mirrored_directions = Direction.neighboring[direction]

        if self.parent is None:  # Reached root?
            return None

        if self.parent.children[mirrored_directions[0]] == self:
            return (self.parent.children[Direction.opposite_of(direction=mirrored_directions[0], relative_to=direction)]
                    if self.parent.children[Direction.opposite_of(direction=mirrored_directions[0], relative_to=direction)] is not None
                    else self.parent)

        if self.parent.children[mirrored_directions[1]] == self:
            return (self.parent.children[Direction.opposite_of(direction=mirrored_directions[1], relative_to=direction)]
                    if self.parent.children[Direction.opposite_of(direction=mirrored_directions[1], relative_to=direction)] is not None
                    else self.parent)

        node = self.parent.get_neighbor_of_greater_or_equal_size(direction=direction)
        if node is None or node.is_leaf():
            return node

        if self.parent.children[Direction.opposite_of(direction=mirrored_directions[1], relative_to=direction)] == self:
            if node.children[mirrored_directions[1]] is None and node.data is not None:
                dummy_node = node.add_child(direction=mirrored_directions[1], is_dummy=True)
                dummy_node.data = deepcopy(self.data)
                return dummy_node
            return node.children[mirrored_directions[1]]

        if node.children[mirrored_directions[1]] is None and node.data is not None:
            dummy_node = node.add_child(direction=mirrored_directions[1], is_dummy=True)
            dummy_node.data = deepcopy(self.data)
            return dummy_node

        return node.children[mirrored_directions[0]]

    def find_neighbors_of_smaller_size(self, neighbor, direction: str) -> list:
        candidates = [] if neighbor is None else [neighbor]
        neighbors = []

        while len(candidates) > 0:
            if candidates[0] is not None:
                if candidates[0].data is not None:
                    data_direction = candidates[0].frame.find_location_in_frame(point=candidates[0].data.position)
                    if data_direction in Direction.neighboring[direction]:
                        neighbors.append(candidates[0])

                if not candidates[0].is_leaf():
                    counter_direction = Direction.opposite_of(direction=direction)
                    if not candidates[0].has_children_in_direction(direction=counter_direction):
                        candidates.append(candidates[0].children[Direction.neighboring[counter_direction][0]])
                        candidates.append(candidates[0].children[Direction.neighboring[counter_direction][1]])
                    else:
                        candidates.append(candidates[0].children[Direction.neighboring[direction][0]])
                        candidates.append(candidates[0].children[Direction.neighboring[direction][1]])

            candidates.remove(candidates[0])

        return neighbors

    def find_neighbors_in_direction(self, direction: str) -> list:
        neighbor = self.get_neighbor_of_greater_or_equal_size(direction=direction)
        return self.find_neighbors_of_smaller_size(neighbor=neighbor, direction=direction)

    def has_children_in_direction(self, direction: str | int) -> bool:
        if isinstance(direction, int):
            return self.children[direction] is not None

        split_direction = Direction.split_direction(direction=direction)

        return (self.children[split_direction[0]] is not None or
                self.children[split_direction[1]] is not None)

    def find_relevant_descendants(self, children_directions: list[tuple]):
        descendants = set()
        for i, directions in children_directions:
            for direction in directions:
                descendants.update(self.find_neighbors_of_smaller_size(direction=direction, neighbor=self))
            # if self.children[i].data is not None:
            #     descendants.add(self.children[i])
        return list(descendants)

    def draw(self, ax):
        """Draw a representation of the quadtree on Matplotlib Axes ax."""

        self.frame.draw(ax)
        if self.is_divided:
            for child in self.children:
                if child is not None:
                    child.draw(ax)


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

    def find_containing_node(self, point: Point) -> Node:
        containing_node = self.root.find_containing_node(point=point)
        containing_node.external_point = point
        return containing_node

    def find_nearest_song(self, point: Point) -> Any:
        point_node = self.find_containing_node(point=point)

        pass

    def find_nearest_nodedata(self, point: Point) -> NodeData:
        containing_node = self.find_containing_node(point=point)
        candidate_nodes = containing_node.find_candidates()

        # print(f"Number of candidates: {len(candidate_nodes)}")
        # print(*candidate_nodes, sep="\n")

        min_distance = (None, 1)
        for node in candidate_nodes:
            curr_distance = point.distance_to(other=node.data.position)
            min_distance = (node, curr_distance) if curr_distance < min_distance[1] else min_distance

        return min_distance[0].data

    def draw(self, ax):
        self.root.draw(ax=ax)
