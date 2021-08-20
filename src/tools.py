from typing import List, Tuple

from constants import *


def to_hex(num: int, digits: int) -> str:
    return ('0' * digits + format(num, 'x'))[-digits:].lower()


def byte_to_bool_list(num: int) -> List[bool]:
    if num > 256:
        raise ValueError()
    elif num < 0:
        raise ValueError()

    return [
        num & 0x80 != 0,
        num & 0x40 != 0,
        num & 0x20 != 0,
        num & 0x10 != 0,
        num & 0x08 != 0,
        num & 0x04 != 0,
        num & 0x02 != 0,
        num & 0x01 != 0,
    ]


def get_view_size(lines: List[str]) -> Tuple[int, int]:
    longest_line = max(lines, key=len)
    longest_line_length = len(longest_line)
    width = longest_line_length * FONT_WIDTH + 2 * MARGIN
    height = len(lines) * FONT_SIZE + 2 * MARGIN
    return (width, height)
