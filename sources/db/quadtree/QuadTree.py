from enum import IntEnum
from numpy import hypot as distance
from items.Song import Song

################
# Thanks to these guys: https://www.geeksforgeeks.org/quad-tree/, https://scipython.com/blog/quadtrees-2-implementation-in-python/


class Point:
    """
    A Point item represents a point in a 2D space by (x,y).
    Each Point has a payload of a Song object.
    """

    def __init__(self, x: float = 0.00, y: float = 0.00, payload: Song = None):
        self.x, self.y = x, y
        self.payload = payload

    def __repr__(self):
        return f"({self.x}, {self.y}) | {repr(self.payload)}"

    def __str__(self):

        return f"<({self.x}, {self.y}) | {self.payload.title} by: {self.payload.artist}" if\
            self.payload is not None else f"({self.x}, {self.y})"

    def distance_to(self, other):
        try:
            other_x, other_y = other.x, other.y
        except AttributeError:
            raise AttributeError(f"Can't measure distance between Point and {type(other)}")

        return distance(self.x - other_x, self.y - other_y)


class Rect:
    """
        A rectangle frame defined by the following:
        cx - rectangle's center x value
        cy - rectangle's center y value
        w - width
        h - height
    """
    def __init__(self, cx: float, cy: float, w: float, h: float):
        self.cx, self.cy = cx, cy
        self.w, self.h = w, h

        self.west_edge, self.east_edge = cx - w/2, cx + w/2
        self.south_edge, self.north_edge = cy - h/2, cy + h/2

    def __repr__(self):
        return str((self.west_edge, self.east_edge,
                    self.north_edge, self.south_edge))

    def __str__(self):
        return f"({self.west_edge:.2f}, {self.east_edge:.2f}," \
               f"{self.north_edge:.2f}, {self.south_edge:.2f})"

    def contains(self, point: Point) -> bool:
        """
        The contains methods checks if the Rectangle contains a given point and returns a boolean indicates the answer.
        :param point: A Point object.
        :return: True if the point is inside the borders.
        """
        return (self.west_edge <= point.x < self.east_edge and
                self.south_edge <= point.y < self.north_edge)

    def intersects(self, other) -> bool:
        """
        The intersects function returns True if the two Rectangles intersect, False otherwise.

        :param other: Check if the other object is within the bounds of this object
        :return: A boolean value
        """
        return not (other.west_edge > self.east_edge or  # Actually, checking if the Rect is not outside.
                    other.east_edge < self.west_edge or
                    other.north_edge < self.south_edge or
                    other.south_edge > self.north_edge)


class QuadTree:

    """
    A class implementing a Quadtree data structure
    """
    class ChildDirection(IntEnum):
        nw = 0
        ne = 1
        se = 2
        sw = 3

    def __init__(self, boundary: Rect = Rect(cx=0.5, cy=0.5, w=1.0, h=1.0),
                 max_points: int = 4, depth: int = 0, children = None):
        """
        Initialize a new tree node that holds a number (`max_points`) of points (`self.points`) within
        a boundary (`self.boundary`).
        :param children: A list of this node's children
        :param boundary:Rect: a `Rect` object representing a frame. The points within it are in this node's `self.points` list.
        :param max_points:int: The maximum number of points a node can hold before being divided (default: 4)
        :param depth:int: How deep into the Quadtree this node lies.
        """

        self.boundary = boundary
        self.max_points = max_points
        self.depth = depth

        self.points = []
        self.is_divided = False

        self.parent = None
        self.children = []

        if children is not None:
            for child in children:
                self.add_child(child=child)

        # self.nw, self.ne, self.se, self.sw = None, None, None, None

    def __str__(self):
        seperator = " " * self.depth * 2
        boundary = f"{self.boundary}\n"
        boundary += seperator + ', '.join(str(point) for point in self.points)
        if not self.is_divided:  # It is a leaf
            return boundary
        return boundary + "\n" + "\n".join([
            f"{seperator} nw: {str(self.children[self.ChildDirection.nw])}",
            f"{seperator} ne: {str(self.children[self.ChildDirection.ne])}",
            f"{seperator} se: {str(self.children[self.ChildDirection.se])}",
            f"{seperator} sw: {str(self.children[self.ChildDirection.sw])}"
        ])

    def __len__(self):
        """
        Returns the number of points in this Quadtree
        :return: Number of points in this Quadtree
        """

        num_of_points = len(self.points)
        if self.is_divided:
            num_of_points += len(self.children[self.ChildDirection.nw]) \
                             + len(self.children[self.ChildDirection.ne]) \
                             + len(self.children[self.ChildDirection.se]) \
                             + len(self.children[self.ChildDirection.sw])
        return num_of_points

    def divide(self):
        """
        Divides this nodes into 4 new children nodes: \n
        - nw - Northwestern child (Top-Left)
        - ne - Northeastern child (Top-Right)|
        - se - Southeastern child (Bottom-Right)|
        - sw - Southwestern child (Bottom-Left)
        :return: None.
        """
        cx, cy = self.boundary.cx, self.boundary.cy
        w, h = self.boundary.w, self.boundary.h

        self.nw = QuadTree(boundary=Rect(cx=(cx - w / 2), cy=(cy - h / 2), h=h, w=w), max_points=self.max_points,
                           depth=(self.depth + 1))

        self.ne = QuadTree(boundary=Rect(cx=(cx + w / 2), cy=(cy - h / 2), h=h, w=w), max_points=self.max_points,
                           depth=(self.depth + 1))

        self.se = QuadTree(boundary=Rect(cx=(cx + w / 2), cy=(cy + h / 2), h=h, w=w), max_points=self.max_points,
                           depth=(self.depth + 1))

        self.sw = QuadTree(boundary=Rect(cx=(cx - w / 2), cy=(cy + h / 2), h=h, w=w), max_points=self.max_points,
                           depth=(self.depth + 1))

        self.is_divided = True

    def add_child(self, child):
        assert isinstance(child, QuadTree)
        child.parent = self
        self.children.append(child)

    def insert_point(self, point: Point):
        """
        The insert function takes a point as an argument and returns True if the
        point is successfully inserted into the Quadtree, if not: False.
        The function first checks to see if the point lies within the boundary of this node's boundary rectangle.
        If so, then we check to see if we have reached our maximum capacity for points in this node (`max_points`).
        If not, then we add that point to our list of points. Otherwise, since there are no more spots left in this node,
        we divide the current node with the `divide()` function and try to insert the point to each of the new children.

        :param point:Point: Insert the point into the quadtree
        :return: A boolean value indicating the insertion success
        """

        if not self.boundary.contains(point=point):
            return False

        if len(self.points) < self.max_points:
            self.points.append(point)
            return True

        if not self.is_divided:
            self.divide()

        return (self.nw.insert_point(point=point) or
                self.ne.insert_point(point=point) or
                self.se.insert_point(point=point) or
                self.sw.insert_point(point=point))

    def query(self, boundary: Rect, found_points: list[Point]) -> list[Point] | bool:
        """
        The query function takes a boundary and returns all points within that boundary.
        The query function is recursive, so it calls itself on the four subquadrants of the
        current quadrant if they intersect with the given boundary.

        :param boundary:Rect: The frame in which the function queries for points.
        :param found_points:list[Point]: Store the points that are found by the query function. FIRST CALL REQUIRES AN EMPTY LIST.
        :return: A list of points that are in the boundary
        """

        if not self.boundary.intersects(other=boundary):
            return False

        for point in self.points:
            if boundary.contains(point=point):
                found_points.append(point)

        if self.is_divided:
            self.nw.query(boundary=boundary, found_points=found_points)
            self.ne.query(boundary=boundary, found_points=found_points)
            self.se.query(boundary=boundary, found_points=found_points)
            self.sw.query(boundary=boundary, found_points=found_points)

        return found_points

    def query_circle(self, boundary: Rect, centre: Point, radius: float,
                     found_points: list[Point]) -> list[Point] | bool:
        """
        The query_circle function finds the points in the quadtree that lies within a radius of centre.
        The functions takes a `Rect` object that bounds the search circle. There is no need to call this
        function directly, call `radius_query()` instead.

        :param boundary:Rect: A frame that bounds the circle in which we are querying
        :param centre:Point: Specify the centre of the circle
        :param radius:float: Specify the radius of the circle
        :param found_points:list[Point]: Store the points that are found in the query_circle function
        :return: A list of points that lie within the circle
        """

        if not self.boundary.intersects(other=boundary):
            return False

        for point in self.points:
            if (boundary.contains(point=point) and
                    point.distance_to(other=centre) <= radius):
                found_points.append(point)

        if self.is_divided:
            self.nw.query_circle(boundary=boundary, found_points=found_points, centre=centre, radius=radius)
            self.ne.query_circle(boundary=boundary, found_points=found_points, centre=centre, radius=radius)
            self.se.query_circle(boundary=boundary, found_points=found_points, centre=centre, radius=radius)
            self.sw.query_circle(boundary=boundary, found_points=found_points, centre=centre, radius=radius)

        return found_points

    def radius_query(self, centre: Point, radius: float, found_points: list[Point]) -> list[Point] | bool:
        """
        The radius_query function takes a centre point and a radius, and returns all points within that radius of the
        centre point.
        :param centre:Point: Specify the centre of the circle
        :param radius:float: Define the radius of the circle
        :param found_points:list[Point]: Store the points that are found during the search. FIRST CALL REQUIRES AN EMPTY LIST.
        :return: A list of points that lie within the specified circle.
        """
        boundary = Rect(cx=centre.x, cy=centre.y, h=2*radius, w=2*radius)
        return self.query_circle(boundary=boundary, centre=centre, radius=radius,
                                 found_points=found_points)

    def nearest_point(self, point: Point) -> Point:
        found_points = []
        radius = 0.01
        while len(found_points) < 1:
            found_points = self.radius_query(centre=point, radius=radius, found_points=found_points)
            radius += 0.01
            print("had a search radius raise")
        if len(found_points) == 1:
            return found_points[0]

        nearest_song_index = found_points.index(min([point.distance_to(other=p) for p in found_points]))

        return found_points[nearest_song_index]
