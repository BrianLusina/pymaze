"""
Contains a few functions that converts a maze into a graph
"""
from typing import NamedTuple, TypeAlias

from ..models.square import Square

Node: TypeAlias = Square


class Edge(NamedTuple):
    """
    Represents a connection between two nodes in a graph. In this case, a connection between two squares in a maze.
    This will represent a two way connection as we can traverse from one square to another and vice versa.
    """
    node1: Node
    node2: Node
