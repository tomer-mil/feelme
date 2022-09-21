from sources.db.quadtree.Point import Point


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
        self.north_edge, self.south_edge = cy - h/2, cy + h/2

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
