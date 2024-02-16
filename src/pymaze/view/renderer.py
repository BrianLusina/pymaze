"""
Handles SVG rendering
"""
from dataclasses import dataclass
from src.pymaze.models.maze import Maze
from src.pymaze.models.solution import Solution
from src.pymaze.models.square import Square
from src.pymaze.view.primitives import tag, Rect, Point
from src.pymaze.view.decomposer import decompose


def arrow_marker() -> str:
    """
    Renders an arror marker indicating an exit from the maze
    """
    return tag(
        "defs",
        tag(
            "marker",
            tag(
                "path",
                d="M 0,0 L 10,5 L 0,10 2,5 z",
                fill="red",
                fill_opacity="50%"
            ),
            id="arrow",
            viewBox="0 0 20 20",
            refX="2",
            refY="5",
            markerUnits="strokeWidth",
            markerWidth="10",
            markerHeight="10",
            orient="auto"
        )
    )


def background() -> str:
    """Draws a background"""
    return Rect().draw(width="100%", height="100%", fill="white")


@dataclass(frozen=True)
class SVG:
    """
    SVG element
    """
    xml_content: str


@dataclass(frozen=True)
class SVGRenderer:
    """
    A scalable vector graphics renderer will take the square size and line width in pixel coordinates as input
    parameters assuming sensible defaults
    """
    square_size: int = 100
    line_width: int = 6

    @property
    def offset(self) -> int:
        """
        The offset is the distance from the top and left edge of the drawing space, which takes your line width into
        account. Without it, a line starting in the top-left corner would be drawn at the very edge of the canvas and
        partially out of view.
        """
        return self.line_width // 2

    def render(self, maze: Maze, solution: Solution | None = None) -> SVG:
        """
        Renders a lightweight SVG object which wraps the textual XML content
        """
        margins = 2 * (self.offset + self.line_width)
        width = margins + maze.width * self.square_size
        height = margins + maze.height * self.square_size

        return SVG(
            tag(
                "svg",
                self._get_body(maze, solution),
                xmlns="http://www.w3.org/2000/svg",
                stroke_linejoin="round",
                width=width,
                height=height,
                viewBox=f"0 0 {width} {height}"
            )
        )

    def _get_body(self, maze: Maze, solution: Solution | None) -> str:
        """Retrieves the body from the maze and solution"""
        return "".join(
            [
                arrow_marker(),
                background(),
                *map(self._draw_square, maze),
                self._draw_solution(solution) if solution else ""
            ]
        )

    def _transform(self, square: Square, extra_offset: int = 0) -> Point:
        """Scales and transforms the square's coordinates using the desired square size and offset"""
        return Point(
            x=square.column * self.square_size,
            y=square.row * self.square_size,
        ).translate(
            x=self.offset + extra_offset,
            y=self.offset + extra_offset
        )

    def _draw_square(self, square: Square) -> str:
        top_left: Point = self._transform(square)
        tags = [self._draw_border(square, top_left)]
        return "".join(tags)

    def _draw_border(self, square: Square, top_left: Point) -> str:
        return decompose(square.border, top_left, self.square_size).draw(
            stroke_width=self.line_width,
            stroke="black",
            fill="none"
        )
