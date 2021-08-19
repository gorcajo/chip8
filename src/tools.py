from typing import List, Tuple

from constants import *


def to_hex(num: int, digits: int) -> str:
    return ('0' * digits + format(num, 'x'))[-digits:].upper()


def get_view_size(lines: List[str]) -> Tuple[int, int]:
    longest_line = max(lines, key=len)
    longest_line_length = len(longest_line)
    width = longest_line_length * FONT_WIDTH + 2 * MARGIN
    height = len(lines) * FONT_SIZE + 2 * MARGIN
    return (width, height)
