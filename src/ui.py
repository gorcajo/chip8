from typing import List, Tuple

import pygame

import chip8
from constants import *


class Drawable:

    def __init__(self, screen: pygame.Surface, x: int = None, y: int = None, w: int = None, h: int = None) -> None:
        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h


    @property
    def top(self) -> int:
        return self.y


    @property
    def right(self) -> int:
        return self.x + self.w


    @property
    def bottom(self) -> int:
        return self.y + self.h


    @property
    def left(self) -> int:
        return self.x


    def draw(self) -> None:
        raise NotImplementedError()


class Panel(Drawable):

    def __init__(self, screen: pygame.Surface, chip8: chip8.Chip8) -> None:
        super().__init__(screen)

        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

        self.drawables: List[Drawable] = []

        games_creen = GameScreen(screen=screen, x=MARGIN, y=MARGIN, pixel_size=PIXEL_SIZE, chip8_display=chip8.display)
        self.drawables.append(games_creen)

        memory_view = MemoryView(
            screen=screen,
            x=games_creen.right + MARGIN,
            y=games_creen.top,
            font=self.font,
            chip8_memory=chip8.memory,
            chip8_pc=chip8.pc)
        self.drawables.append(memory_view)

        index_view = IndexView(
            screen=screen,
            x=memory_view.right + MARGIN,
            y=games_creen.top,
            font=self.font,
            chip8_index=chip8.index)
        self.drawables.append(index_view)

        delay_timer_view = TimerView(
            screen=screen,
            x=memory_view.right + MARGIN,
            y=index_view.bottom + MARGIN,
            font=self.font,
            name='Delay Timer',
            chip8_timer=chip8.delay_timer)
        self.drawables.append(delay_timer_view)

        sound_timer_view = TimerView(
            screen=screen,
            x=memory_view.right + MARGIN,
            y=delay_timer_view.bottom + MARGIN,
            font=self.font,
            name='Sound Timer',
            chip8_timer=chip8.delay_timer)
        self.drawables.append(sound_timer_view)

        registers_view = RegistersView(
            screen=screen,
            x=memory_view.right + MARGIN,
            y=sound_timer_view.bottom + MARGIN,
            font=self.font,
            chip8_registers=chip8.registers)
        self.drawables.append(registers_view)

        stack_view = StackView(
            screen=screen,
            x=memory_view.right + MARGIN,
            y=registers_view.bottom + MARGIN,
            font=self.font,
            chip8_stack=chip8.stack,
            length=memory_view.h - registers_view.bottom)
        self.drawables.append(stack_view)

        help_text = HelpText(
            screen=screen,
            x=MARGIN,
            y=games_creen.bottom + MARGIN,
            font=self.font)
        self.drawables.append(help_text)


    def draw(self) -> None:
        for drawable in self.drawables:
            drawable.draw()


class GameScreen(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, pixel_size: int, chip8_display: chip8.Display) -> None:
        super().__init__(screen, x, y, chip8_display.pixels_width * pixel_size, chip8_display.pixels_height * pixel_size)
        self.pixel_size = pixel_size
        self.chip8_display = chip8_display


    def draw(self) -> None:
        for y in range(self.chip8_display.pixels_height):
            for x in range(self.chip8_display.pixels_width):
                rect = pygame.Rect(
                    self.x + x * self.pixel_size,
                    self.y + y * self.pixel_size,
                    self.pixel_size,
                    self.pixel_size)

                color = PIXEL_ON_COLOR if self.chip8_display.get_pixel_at(x, y) else PIXEL_OFF_COLOR

                pygame.draw.rect(self.screen, color, rect)

        rect = pygame.Rect(
            self.x,
            self.y,
            self.chip8_display.pixels_width * self.pixel_size,
            self.chip8_display.pixels_height * self.pixel_size)

        pygame.draw.rect(self.screen, PRIMARY_COLOR, rect, 1)


class MemoryView(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, font: pygame.font, chip8_memory: chip8.Memory, chip8_pc: chip8.ProgramCounter) -> None:
        super().__init__(screen, x, y, 320, 532)

        self.font = font
        self.chip8_memory = chip8_memory
        self.chip8_pc = chip8_pc

        self.addresses_to_show = 64


    def draw(self) -> None:
        lines = []
        lines.append('  ADDR  DATA  MNEMONIC        ')

        for i in range(-self.addresses_to_show // 2 + 2, self.addresses_to_show // 2, 2):
            address = self.chip8_pc.address + i

            if address < 0:
                address += self.chip8_memory.size

            first_byte = self.chip8_memory .get_data_at(address)
            second_byte = self.chip8_memory .get_data_at(address + 1)

            marker = '→' if i == 0 else ' '
            lines.append(f'{marker}  {to_hex(address, 3)}  {to_hex(first_byte, 2)}{to_hex(second_byte, 2)}')
        
        for i, line in enumerate(lines):
            color = HIGHLIGHT_COLOR if '→' in line else PRIMARY_COLOR

            self.screen.blit(
                self.font.render(line, False, color),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        pygame.draw.rect(self.screen, PRIMARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class IndexView(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, font: pygame.font, chip8_index: chip8.IndexRegister) -> None:
        super().__init__(screen, x, y, 160, 52)

        self.font = font
        self.chip8_index = chip8_index


    def draw(self) -> None:
        lines = [
            'Index register',
            f' {to_hex(self.chip8_index.address, 4)}',
        ]
        
        for i, line in enumerate(lines):
            self.screen.blit(
                self.font.render(line, False, PRIMARY_COLOR),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        pygame.draw.rect(self.screen, PRIMARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class TimerView(Drawable):

    def __init__(
        self,
        screen: pygame.Surface,
        x: int,
        y: int,
        font: pygame.font,
        name: str,
        chip8_timer: chip8.DelayTimer) -> None:

        super().__init__(screen, x, y, 160, 52)

        self.font = font
        self.name = name
        self.chip8_timer = chip8_timer


    def draw(self) -> None:
        lines = [
            self.name,
            f' {to_hex(self.chip8_timer.value, 2)}',
        ]
        
        for i, line in enumerate(lines):
            self.screen.blit(
                self.font.render(line, False, PRIMARY_COLOR),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        pygame.draw.rect(self.screen, PRIMARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class StackView(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, font: pygame.font, chip8_stack: chip8.Stack, length: int) -> None:
        super().__init__(screen, x, y, 160, length)

        self.font = font
        self.chip8_stack = chip8_stack


    def draw(self) -> None:
        lines = []
        lines.append('Stack')

        for i in range(len(self.chip8_stack)):
            lines.append(f' {to_hex(self.chip8_stack[i], 2)}')
        
        for i, line in enumerate(lines):
            self.screen.blit(
                self.font.render(line, False, PRIMARY_COLOR),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        pygame.draw.rect(self.screen, PRIMARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class RegistersView(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, font: pygame.font, chip8_registers: chip8.Registers) -> None:
        super().__init__(screen, x, y, 160, 164)

        self.font = font
        self.chip8_registers = chip8_registers


    def draw(self) -> None:
        lines = []
        lines.append('Registers')

        for i in range(len(self.chip8_registers) // 2):
            j = i + len(self.chip8_registers) // 2

            line = f' V{to_hex(i, 1)} {to_hex(self.chip8_registers[i], 2)}'
            line += f'   V{to_hex(j, 1)} {to_hex(self.chip8_registers[j], 2)}'

            lines.append(line)
        
        for i, line in enumerate(lines):
            self.screen.blit(
                self.font.render(line, False, PRIMARY_COLOR),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        pygame.draw.rect(self.screen, PRIMARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class HelpText(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, font: pygame.font) -> None:
        super().__init__(screen, x, y)
        self.font = font
        self.lines = [
            'Game controls',
            '',
            '+---+---+---+---+        +---+---+---+---+',
            '| 1 | 2 | 3 | C |   →    | 1 | 2 | 3 | 4 |',
            '+---+---+---+---+        +---+---+---+---+',
            '| 4 | 5 | 6 | D |   →    | Q | W | E | R |',
            '+---+---+---+---+        +---+---+---+---+',
            '| 7 | 8 | 9 | E |   →    | A | S | D | F |',
            '+---+---+---+---+        +---+---+---+---+',
            '| A | 0 | B | F |   →    | Z | X | C | V |',
            '+---+---+---+---+        +---+---+---+---+',
        ]


    def draw(self) -> None:
        for i, line in enumerate(self.lines):
            self.screen.blit(
                self.font.render(line, False, PRIMARY_COLOR),
                (MARGIN + self.x, MARGIN + self.y + i * FONT_SIZE))

        longest_line = max(self.lines, key=len)
        longest_line_length = len(longest_line)

        rect = pygame.Rect(
            self.x,
            self.y,
            longest_line_length * FONT_WIDTH + 2 * MARGIN,
            len(self.lines) * FONT_SIZE + 2 * MARGIN)

        pygame.draw.rect(self.screen, PRIMARY_COLOR, rect, 1)


def to_hex(num: int, min_digits: int) -> str:
    return ('0' * min_digits + format(num, 'x'))[-min_digits:].upper()


def get_view_size(lines: List[str]) -> Tuple[int, int]:
    longest_line = max(lines, key=len)
    longest_line_length = len(longest_line)
    width = longest_line_length * FONT_WIDTH + 2 * MARGIN
    height = len(lines) * FONT_SIZE + 2 * MARGIN
    return (width, height)
