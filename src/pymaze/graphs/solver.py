"""
Contains functions to wrap networkX algorithms to solve a maze
"""
import networkx as nx

from ..models.maze import Maze
from ..models.solution import Solution
from .converter import make_graph


def solve(maze: Maze) -> Solution | None:
    """
    Solves a maze and produces a solution to the given maze. If no solution can be found None is returned.
    """
    try:
        return Solution(
            squares=tuple(
                nx.shortest_path(
                    G=make_graph(maze=maze),
                    source=maze.entrance,
                    target=maze.exit
                )
            )
        )
    except nx.NetworkXException:
        return None
