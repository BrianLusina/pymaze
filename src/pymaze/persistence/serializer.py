"""
Contains loading and saving routines
"""
import array
from typing import Tuple, List
import pathlib

from src.pymaze.models.maze import Maze
from src.pymaze.models.square import Square
from src.pymaze.models.border import Border
from src.pymaze.models.role import Role
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


def load(path: pathlib.Path) -> Maze:
    """Loads a file on the provided path with the mode set to read in binary mode & creates the header and body of the
    file before deserializes it with the deserializer utility function"""
    with path.open("rb") as file:
        header = FileHeader.read(file)
        if header.format_version != FORMAT_VERSION:
            raise ValueError("Unsupported file format version")
        body = FileBody.read(header, file)
    return deserialize(header, body)


def deserialize(header: FileHeader, body: FileBody) -> Maze:
    """Deserializes a header and body into a Maze
    Loops over the square values in the file body. To keep track of the current square index, it enumerates the values
    and calculates their row and column based on metadata in the header. Each bit field gets decompressed into the
    relevant Border and Role, which the square’s class constructor requires.
    """
    squares: List[Square] = []
    for index, square_value in enumerate(body.square_values):
        row, column = divmod(index, header.width)
        border, role = decompress(square_value)
        squares.append(Square(index, row, column, border, role))
    return Maze(tuple(squares))


def decompress(square_value: int) -> Tuple[Border, Role]:
    """Decompresses a square value into a tuple of a border and its Role"""
    return Border(square_value & 0xf), Role(square_value >> 4)


def compress(square: Square) -> int:
    """
    Returns the corresponding Role and Border values encoded as a compound bit field. It uses bitwise operators to
    compress the two values into a single number.
    """
    return (square.role << 4) | square.border.value
