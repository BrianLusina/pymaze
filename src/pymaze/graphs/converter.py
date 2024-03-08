"""
Contains a few functions that converts a maze into a graph
"""
import math
from typing import NamedTuple, TypeAlias, Set

import networkx as nx

from ..models.square import Square
from ..models.maze import Maze
from ..models.role import Role
from ..models.border import Border

Node: TypeAlias = Square


class Edge(NamedTuple):
    """
    Represents a connection between two nodes in a graph. In this case, a connection between two squares in a maze.
    This will represent a two way connection as we can traverse from one square to another and vice versa.
    """
    node1: Node
    node2: Node

    @property
    def distance(self) -> float:
        """
        Calculates the Euclidean distance(length of the line segment between them) between the nodes using math module,
        whose dist() function takes two points specified as sequences of coordinates. In this case, we provide tuples of
        the row and column indices of squares corresponding to the nodes. Note that you could define distance
        differently—for example, as the sum of absolute values of differences in the horizontal and vertical directions.
        """
        return math.dist(
            (self.node1.row, self.node1.column),
            (self.node2.row, self.node2.column)
        )


def get_nodes(maze: Maze) -> Set[Node]:
    """
    Retrieves a set of nodes from a given maze filtering out squares that are exteriors and ones that are walls.
    Args:
        maze (Maze): Maze to extract nodes from
    Returns:
        Set: set of nodes
    """
    nodes: Set[Node] = set()
    for square in maze:
        if square.role in (Role.EXTERIOR, Role.WALL):
            continue
        if square.role is not Role.NONE:
            nodes.add(square)
        if (
                square.border.intersection
                or square.border.dead_end
                or square.border.corner
        ):
            nodes.add(square)
    return nodes


def get_edges(maze: Maze, nodes: Set[Node]) -> Set[Edge]:
    """
    Retrieves a set of edges from a given maze and the nodes that were extracted from the maze.

    This looks for the immediate neighbors of each node supplied to the function. In this case, it moves east and south
     in the maze, but it could just as well follow the opposite directions, remembering to change the loop indexing and
     wall detection accordingly. It uses the bitwise AND operator (&) to check if a border around the current square has
      either the right or bottom side, indicating a wall that terminates the search in that direction.

    On the other hand, if it finds that a square located in the same row or column as the source node is also present
    in the set of nodes, and there’s no wall between them, then it creates an Edge instance and adds it to the set of
    edges.
    Args:
        maze (Maze): maze object
        nodes (set) of (Node): set of nodes extracted from maze
    Returns:
        set: set of edges connecting the squares
    """
    edges: Set[Edge] = set()

    for source_node in nodes:
        # follow the right node
        node = source_node

        for x in range(node.column + 1, maze.width):
            if node.border & Border.RIGHT:
                break
            node = maze.squares[node.row * maze.width + x]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break

        # follow down
        node = source_node
        for y in range(node.row + 1, maze.height):
            if node.border & Border.BOTTOM:
                break
            node = maze.squares[y * maze.width + node.column]
            if node in nodes:
                edges.add(Edge(source_node, node))
                break

    return edges


def make_graph(maze: Maze) -> nx.Graph:
    """
    Creates a NetworkX Graph object given a Maze object
    """
    nodes = get_nodes(maze=maze)
    edges = get_edges(maze=maze, nodes=nodes)
    return nx.Graph(incoming_graph_data=(edge.node1, edge.node2, {"weight": edge.distance} for edge in edges))
