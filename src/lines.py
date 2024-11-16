
from dataclasses import dataclass
from collections.abc import Callable, Sequence


@dataclass
class Line:
    min_width: int
    content: Callable[[int], str]

    @staticmethod
    def fixed(content: str):
        return Line(len(content), lambda _: content)

    @staticmethod
    def space_between(part1: str, part2: str, min_space: int = 2):
        return Line(len(part1) + min_space + len(part2), lambda w: part1 + ' ' * (w - len(part1) - len(part2)) + part2)


def print_box(lines: Sequence[Line], *, indent: int = 0, padding: int = 2):
    width = max(l.min_width for l in lines)
    print(' ' * indent + '┌' + '─' * (width + padding) + '┐')
    for line in lines:
        print(' ' * indent + '│' + line.content(width).center(width + padding) + '│')
    print(' ' * indent + '└' + '─' * (width + padding) + '┘')
