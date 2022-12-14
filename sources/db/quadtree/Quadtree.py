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

            if relative_to in {"N", "S"}:
                return 3 - direction

            if relative_to == "center":
                match direction:
                    case Direction.NW: return Direction.SE
                    case Direction.NE: return Direction.SW
                    case Direction.SE: return Direction.NW
                    case Direction.SW: return Direction.NE

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
    def split_direction(direction: str | int) -> tuple:
        if isinstance(direction, str):
            assert direction in {"N", "S", "W", "E"}

            match direction:
                case "N": return Direction.NW, Direction.NE
                case "S": return Direction.SW, Direction.SE
                case "W": return Direction.NW, Direction.SW
                case "E": return Direction.NE, Direction.SE

        match direction:
            case Direction.NW: return "N", "W"
            case Direction.NE: return "N", "E"
            case Direction.SE: return "S", "E"
            case Direction.SW: return "S", "W"


    @staticmethod
    def concatenate_directions(dir1: str, dir2: str) -> int:
        assert isinstance(dir1, str)
        assert isinstance(dir2, str)

        if dir1 == Direction.opposite_of(direction=dir2):
            raise Exception("Opposite Directions")

        concatenated_direction = dir1 + dir2 if dir1 in {"N", "S"} else dir2 + dir1

        match concatenated_direction:
            case "NW": return Direction.NW
            case "NE": return Direction.NE
            case "SE": return Direction.SE
            case "SW": return Direction.SW

    @staticmethod
    def is_vertical(direction: str) -> bool:
        return direction in {"N", "S"}


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

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

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

    def nudge(self, direction: int | str):
        EPSILON = 0.001
        if isinstance(direction, int):
            match direction:
                case Direction.NW:
                    self.x -= EPSILON
                    self.y += EPSILON
                case Direction.NE:
                    self.x += EPSILON
                    self.y += EPSILON
                case Direction.SE:
                    self.x += EPSILON
                    self.y -= EPSILON
                case Direction.SW:
                    self.x -= EPSILON
                    self.y -= EPSILON
        else:
            match direction:
                case "N":
                    self.y += EPSILON
                case "S":
                    self.y -= EPSILON
                case "W":
                    self.x -= EPSILON
                case "E":
                    self.x += EPSILON


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

        # Debug method
        self.color = ""

    def __repr__(self):
        return f"TL: {str(self.top_left)}, BR: {str(self.bottom_right)}, Color: {self.color}"

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

    def get_top_right(self) -> Point:
        return Point(x=self.bottom_right.x, y=self.top_left.y)

    def get_bottom_left(self) -> Point:
        return Point(x=self.top_left.x, y=self.bottom_right.y)

    def get_corners(self) -> list[Point]:
        return [self.top_left, self.get_top_right(), self.bottom_right, self.get_bottom_left()]

    @staticmethod
    def convert_color_to_text(hex_color: str):
        match hex_color:
            case "#1f77b4": return "blue"
            case "#ff7f0e": return "orange"
            case "#2ca02c": return "green"
            case "#d62728": return "red"
            case "#9467bd": return "purple"
            case "#8c564b": return "brown"
            case "#e377c2": return "pink"
            case "#7f7f7f": return "grey"
            case "#bcbd22": return "yellow"
            case "#17becf": return "cyan"

    def draw(self, ax):
        top_left = Point(x=self.top_left.x, y=self.top_left.y)
        bottom_left = Point(x=self.top_left.x, y=self.bottom_right.y)

        bottom_right = Point(x=self.bottom_right.x, y=self.bottom_right.y)
        top_right = Point(x=self.bottom_right.x, y=self.top_left.y)

        p = ax.plot([top_left.x, top_right.x, bottom_right.x, bottom_left.x, top_left.x],
                    [top_left.y, top_right.y, bottom_right.y, bottom_left.y, top_left.y])

        self.color = Frame.convert_color_to_text(hex_color=p[-1].get_color())


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
        greater_neighbors = []

        for direction in neighbors_directions:
            greater_neighbor = self.get_neighbor_of_greater_or_equal_size(direction=direction)
            greater_neighbors.append((direction, greater_neighbor)) if greater_neighbor is not None else None
            neighbors.extend(self.find_neighbors_of_smaller_size(neighbor=greater_neighbor, direction=direction))

        neighbors.extend(self.find_diagonal_neighbors(greater_neighbors=greater_neighbors))

        return neighbors

    def get_relative_direction_of_children_to_point(self, point: Point) -> list[tuple]:
        assert isinstance(self.external_point, Point)

        child_and_directions_list = []

        for child_direction, child in enumerate(self.children):
            if child is not None:
                child_and_directions_list.append((child_direction, child.frame.find_frame_relative_direction(point=point)))
        return child_and_directions_list

    def is_corner(self, direction: int, neighbor1: tuple, neighbor2: tuple) -> bool:
        neighbor1_corners, neighbor2_corners = neighbor1[1].frame.get_corners(), neighbor2[1].frame.get_corners()

        neighbor1_corner = neighbor1_corners[Direction.opposite_of(direction=direction, relative_to=neighbor1[0])]
        neighbor2_corner = neighbor2_corners[Direction.opposite_of(direction=direction, relative_to=neighbor2[0])]

        return self.frame.get_corners()[direction] == neighbor1_corner == neighbor2_corner





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

        if self.parent.children[Direction.opposite_of(direction=mirrored_directions[0], relative_to=direction)] == self:
            if node.data is not None:
                if node.frame.find_location_in_frame(point=node.data.position) == mirrored_directions[0]:
                    dummy_node = node.add_child(direction=mirrored_directions[0], is_dummy=True)
                    dummy_node.data = deepcopy(node.data)
                    return dummy_node
            return node.children[mirrored_directions[0]]

        if self.parent.children[Direction.opposite_of(direction=mirrored_directions[1], relative_to=direction)] == self:
            if node.data is not None:
                if node.frame.find_location_in_frame(point=node.data.position) == mirrored_directions[1]:
                    dummy_node = node.add_child(direction=mirrored_directions[1], is_dummy=True)
                    dummy_node.data = deepcopy(node.data)
                    return dummy_node
            return node.children[mirrored_directions[1]]
        #
        # if node.children[mirrored_directions[1]] is None and node.data is not None:
        #     dummy_node = node.add_child(direction=mirrored_directions[1], is_dummy=True)
        #     dummy_node.data = deepcopy(self.data)
        #     return dummy_node

        return node.children[mirrored_directions[0]]

    def find_neighbors_of_smaller_size(self, neighbor, direction: str) -> list:
        candidates = [] if neighbor is None else [neighbor]
        neighbors = []
        counter_direction = Direction.opposite_of(direction=direction)  # CHANGES IN CASE OF DIAGONAL, TO SPLIT_DIRECTION

        while len(candidates) > 0:
            if candidates[0] is not None:

                if candidates[0].is_leaf():
                    neighbors.append(candidates[0])

                elif candidates[0].data is not None:
                    data_direction = candidates[0].frame.find_location_in_frame(point=candidates[0].data.position)
                    if data_direction in Direction.neighboring[direction]:  # CHANGES IN CASE OF DIAGONAL
                        neighbors.append(candidates[0])

                if ((not candidates[0].has_children_in_direction(direction=counter_direction))
                        and not candidates[0].has_data_in_direction(direction=counter_direction)):
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

    def find_diagonal_neighbors(self, greater_neighbors: list[tuple]):
        vertical_neighbors = []
        horizontal_neighbors = []
        for neighbor in greater_neighbors:
            if Direction.is_vertical(direction=neighbor[0]):
                vertical_neighbors.append(neighbor)
            else:
                horizontal_neighbors.append(neighbor)

        diagonal_neighbors = []

        if len(vertical_neighbors) > 0 and len(horizontal_neighbors) > 0:
            for v_neighbor in vertical_neighbors:
                for h_neighbor in horizontal_neighbors:

                    diagonal_direction = Direction.concatenate_directions(dir1=h_neighbor[0], dir2=v_neighbor[0])

                    if (self == self.parent.children[Direction.opposite_of(direction=diagonal_direction, relative_to="center")]
                            and self.parent.children[diagonal_direction]):

                        diagonal_neighbors.extend(self.parent.children[diagonal_direction].
                                                  find_diagonal_descendants(
                            direction=Direction.opposite_of(direction=diagonal_direction, relative_to="center")))

                    if self.is_corner(direction=diagonal_direction, neighbor1=v_neighbor, neighbor2=h_neighbor):
                        if v_neighbor[1].depth >= h_neighbor[1].depth:
                            diagonal_greater_neighbor = v_neighbor[1].get_neighbor_of_greater_or_equal_size(
                                direction=h_neighbor[0])
                        else:
                            diagonal_greater_neighbor = h_neighbor[1].get_neighbor_of_greater_or_equal_size(
                                direction=v_neighbor[0])

                        diagonal_neighbors.extend(diagonal_greater_neighbor.find_diagonal_descendants(
                            direction=Direction.opposite_of(direction=diagonal_direction, relative_to="center")))

        return diagonal_neighbors

    def find_diagonal_descendants(self, direction: int) -> list:
        corner_point = deepcopy(self.frame.get_corners()[direction])
        corner_point.nudge(direction=Direction.opposite_of(direction=direction, relative_to="center"))

        corner_node = self.find_containing_node(point=corner_point)

        if corner_node.is_leaf() or corner_node.has_data_in_direction(direction=direction):
            return [corner_node]

        dummy_node = corner_node.add_child(direction=direction, is_dummy=True)
        split_direction = Direction.split_direction(direction=direction)

        corner_nodes = []

        for s_direction in split_direction:
            counter_direction = Direction.opposite_of(direction=direction, relative_to=s_direction)
            if corner_node.children[counter_direction] is not None:
                corner_nodes.extend(dummy_node.find_neighbors_of_smaller_size(
                    neighbor=corner_node.children[counter_direction], direction=s_direction))

        return corner_nodes

    def has_children_in_direction(self, direction: str | int) -> bool:
        if isinstance(direction, int):
            return self.children[direction] is not None

        split_direction = Direction.split_direction(direction=direction)

        return (self.children[split_direction[0]] is not None or
                self.children[split_direction[1]] is not None)

    def has_data_in_direction(self, direction: str | int) -> bool:
        if self.data:
            data_location = self.frame.find_location_in_frame(point=self.data.position)

            if isinstance(direction, int):
                return data_location == direction

            split_direction = Direction.split_direction(direction=data_location)
            return direction == split_direction[0] or direction == split_direction[1]

        return False

    def find_relevant_descendants(self, children_directions: list[tuple]):
        descendants = set()
        for i, directions in children_directions:
            for direction in directions:
                descendants.update(self.find_neighbors_of_smaller_size(direction=Direction.opposite_of(direction=direction), neighbor=self))
            # if self.children[i].data is not None:
            #     descendants.add(self.children[i])
        return list(descendants)

    def draw(self, ax):
        """Draw a representation of the quadtree on Matplotlib Axes ax."""

        self.frame.draw(ax=ax)
        if self.is_divided:
            for child in self.children:
                if child is not None:
                    child.draw(ax=ax)


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

    def find_nearest_nodedata(self, point: Point, with_candidates: bool = False) -> NodeData:
        candidate_nodes = self.get_candidate_nodes(point=point)

        # print(f"Number of candidates: {len(candidate_nodes)}")
        # print(*candidate_nodes, sep="\n")

        min_distance = (None, 1)
        for node in candidate_nodes:
            curr_distance = point.distance_to(other=node.data.position)
            min_distance = (node, curr_distance) if curr_distance < min_distance[1] else min_distance

        return min_distance[0].data if not with_candidates else (min_distance[0].data, candidate_nodes)

    def get_candidate_nodes(self, point: Point):
        containing_node = self.find_containing_node(point=point)
        return containing_node.find_candidates()

    def draw(self, ax):
        self.root.draw(ax=ax)
