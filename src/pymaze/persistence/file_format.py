"""
File format will contain file header and body
"""
from typing import BinaryIO
from dataclasses import dataclass
import struct

MAGIC_NUMBER: bytes = b"MAZE"


@dataclass(frozen=True)
class FileHeader:
    """
    Defines the file header of the file.
    """
    format_version: int
    width: int
    height: int

    def write(self, file: BinaryIO) -> None:
        """writes content into a supplied binary file"""
        file.write(MAGIC_NUMBER)
        # B stands for unsigned byte, which works with the expected version field
        file.write(struct.pack("B", self.format_version))
        # The less than symbol (<) indicates a little-endian byte order. The number that follows communicates how many
        # consecutive values of the same type you’re going to provide. Finally, the uppercase letter 'I' denotes a
        # 32-bit unsigned integer type.
        #
        # So, the string <2I means two unsigned integers, one after the other, in little-endian order. It makes sense
        # to group as many fields together as possible to limit the number of expensive system calls that write a block
        # of data to the file.
        file.write(struct.pack("<2I", self.width, self.height))

    @classmethod
    def read(cls, file: BinaryIO) -> 'FileHeader':
        """reads contents from a supplied file to create a file header"""
        assert (file.read(len(MAGIC_NUMBER)) == MAGIC_NUMBER, "Unknown file type")
        # struct.unpack() always returns a tuple, hence the need to add a comma(,).
        format_version, = struct.unpack("B", file.read(1))
        width, height = struct.unpack("<2I", file.read(2 * 4))
        return cls(format_version=format_version, width=width, height=height)
