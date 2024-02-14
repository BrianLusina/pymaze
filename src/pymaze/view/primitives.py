"""
Primitives that will be used to create XML tags for SVG graphics
"""
from typing import Protocol, NamedTuple


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
