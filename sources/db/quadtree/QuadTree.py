from sources.db.quadtree.Point import Point
from sources.db.quadtree.Rect import Rect


class QuadTree:
    """
    A class implementing a Quadtree data structure
    """

    def __init__(self, boundary: Rect, max_points: int = 4, depth: int = 0):
        """
        Initialize a new tree node that holds a number (`max_points`) of points (`self.points`) within
        a boundary (`self.boundary`).

        :param boundary:Rect: a `Rect` object representing a frame. The points within it are in this node's `self.points` list.
        :param max_points:int: The maximum number of points a node can hold before being divided (default: 4)
        :param depth:int: How deep into the Quadtree this node lies.
        """

        self.boundary = boundary
        self.max_points = max_points
        self.depth = depth

        self.points = []
        self.is_divided = False

        self.nw, self.ne, self.se, self.sw = None, None, None, None

    def __str__(self):
        seperator = " " * self.depth * 2
        boundary = f"{self.boundary}\n"
        boundary += seperator + ', '.join(str(point) for point in self.points)
        if not self.is_divided:  # It is a leaf
            return boundary
        return boundary + "\n" + "\n".join([
            f"{seperator} nw: {str(self.nw)}",
            f"{seperator} ne: {str(self.ne)}",
            f"{seperator} se: {str(self.se)}",
            f"{seperator} sw: {str(self.sw)}"
        ])

    def __len__(self):
        """
        Returns the number of points in this Quadtree
        :return: Number of points in this Quadtree
        """

        num_of_points = len(self.points)
        if self.is_divided:
            num_of_points += len(self.nw) + len(self.ne) + len(self.se) + len(self.sw)
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

        self.nw = QuadTree(boundary=Rect(cx=(cx - w/2), cy=(cy - h/2), h=h, w=w),
                           max_points=self.max_points, depth=(self.depth + 1))

        self.ne = QuadTree(boundary=Rect(cx=(cx + w/2), cy=(cy - h/2), h=h, w=w),
                           max_points=self.max_points, depth=(self.depth + 1))

        self.se = QuadTree(boundary=Rect(cx=(cx + w/2), cy=(cy + h/2), h=h, w=w),
                           max_points=self.max_points, depth=(self.depth + 1))

        self.sw = QuadTree(boundary=Rect(cx=(cx - w/2), cy=(cy + h/2), h=h, w=w),
                           max_points=self.max_points, depth=(self.depth + 1))

        self.is_divided = True

    def insert(self, point: Point):
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

        return (self.nw.insert(point=point) or
                self.ne.insert(point=point) or
                self.se.insert(point=point) or
                self.sw.insert(point=point))

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
                    point.distance_to(point=centre) <= radius):
                found_points.append(point)

        if self.is_divided:
            self.nw.query_circle(boundary=boundary, found_points=found_points)
            self.ne.query_circle(boundary=boundary, found_points=found_points)
            self.se.query_circle(boundary=boundary, found_points=found_points)
            self.sw.query_circle(boundary=boundary, found_points=found_points)

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


