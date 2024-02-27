"""
Contains loading and saving routines
"""
import array
from typing import Tuple
import pathlib

from src.pymaze.models.maze import Maze
from src.pymaze.models.square import Square
from src.pymaze.persistence.file_format import FileBody, FileHeader

FORMAT_VERSION: int = 1


def dump(maze: Maze, path: pathlib.Path) -> None:
    """
    Serializes and dumps the maze into a given file on the path specified
    """
    header, body = serializer(maze)
    # writes the file in binary mode ensuring that Python writes the file as is without implicit conversions
    with path.open(mode="wb") as file:
        header.write(file)
        body.write(file)


def serializer(maze: Maze) -> Tuple[FileHeader, FileBody]:
    """
    Serializes a maze into a file header and body
    """
    header = FileHeader(FORMAT_VERSION, maze.width, maze.height)
    body = FileBody(array.array('B', map(compress, maze)))
    return header, body


def compress(square: Square) -> int:
    """
    Returns the corresponding Role and Border values encoded as a compound bit field. It uses bitwise operators to
    compress the two values into a single number.
    """
    return (square.role << 4) | square.border.value()
