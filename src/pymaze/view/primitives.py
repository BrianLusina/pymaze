"""
Primitives that will be used to create XML tags for SVG graphics
"""
from typing import Protocol, NamedTuple, Tuple


class Primitive(Protocol):
    """
    Protocol or interface common to all primitives.
    Reference: https://docs.python.org/3/library/typing.html#typing.Protocol
    """

    def draw(self, **attributes) -> str:
        """method that is common on all primitives"""
        ...


class Point(NamedTuple):
    """
    Euclidean point comprising x and y coordinates. Note that named tuples are immutable and therefore the translate
    method will return a new Euclidean point.
    """

    x: int
    y: int

    def draw(self, **attributes) -> str:
        """draws and x and y point"""
        return f"{self.x},{self.y}"

    def translate(self, x=0, y=0) -> 'Point':
        """Translates x & y points into a new Euclidean point."""
        return Point(x=self.x + x, y=self.y + y)


class Line(NamedTuple):
    """
    Line segment that has a start and end points
    """
    start: Point
    end: Point

    def draw(self, **attributes) -> str:
        """Draws an SVG line primitive"""
        return tag(
            "line",
            x1=self.start.x,
            y1=self.start.y,
            x2=self.end.x,
            y2=self.end.y,
            **attributes
        )


class Polyline(Tuple[Point, ...]):
    """
    Tuple of 2 or more points where the points are connected, however, the first and last point are unconnected
    """

    def draw(self, **attributes) -> str:
        """Draws an SVG polyline primitive"""
        points = " ".join(point.draw() for point in self)
        return tag("polyline", points=points, **attributes)


class Polygon(Tuple[Point, ...]):
    """
    Tuple of 2 or more points where the points are connected with the first and last point connected
    """

    def draw(self, **attributes) -> str:
        """Draws an SVG polygon primitive"""
        points = " ".join(point.draw() for point in self)
        return tag("polygon", points=points, **attributes)


class DisjointLines(Tuple[Line, ...]):
    """
    Used to combine conveniently combine existing lines instead of individual points, especially when they don’t form a
    continuous polyline.
    """

    def draw(self, **attributes) -> str:
        """draws an SVG disjoint line primitive"""
        return "".join(line.draw(**attributes) for line in self)


def tag(name: str, value: str | None = None, **attributes) -> str:
    """
    Generic function that returns an XML tag with the given name, optional value and zero or more attributes
    Args:
        name(str): name of the XML tag.
        value(str): Optional value of an XML tag, defaulted to None
        attributes(dict): Key value pairs of attributes to add to the XML tag
    Return:
        str: XML tag as a string.
    """
    attrs = "" if not attributes else " " + " ".join(
        f'{key.replace("_", "-")}="{value}"'
        for key, value in attributes.items()
    )

    if value is None:
        return f"<{name}{attrs} />"
    return f"<{name}{attrs}>{value}</{name}>"
