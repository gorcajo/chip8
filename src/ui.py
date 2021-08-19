from typing import List

import pygame

import chip8
from constants import *
from tools import *


class Drawable:

    def __init__(self, screen: pygame.Surface, font: pygame.font = None, x: int = None, y: int = None, w: int = None, h: int = None) -> None:
        self.screen = screen
        self.font = font
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


    def draw_text(self, lines: List[str], x_offset=0, y_offset=0, highlights: List[int] = None) -> None:
        highlights = [] if highlights is None else highlights

        for i, line in enumerate(lines):
            color = HIGHLIGHT_COLOR if i in highlights else PRIMARY_COLOR

            self.screen.blit(
                self.font.render(line, False, color),
                (MARGIN + self.x + x_offset, MARGIN + self.y + i * FONT_SIZE + y_offset))


    def draw_frame(self) -> None:
        pygame.draw.rect(self.screen, SECONDARY_COLOR, pygame.Rect(self.x, self.y, self.w, self.h), 1)


class Panel(Drawable):

    def __init__(self, screen: pygame.Surface, chip8: chip8.Chip8) -> None:
        super().__init__(screen)
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)
        self.drawables: List[Drawable] = []

        # Game screen:

        game_screen = GameScreen(screen=screen, x=MARGIN, y=MARGIN, pixel_size=PIXEL_SIZE, chip8_display=chip8.display)
        self.drawables.append(game_screen)

        # CHIP-8 inspection:

        memory_view = MemoryView(
            screen=screen,
            font=self.font,
            x=game_screen.right + MARGIN,
            y=game_screen.top,
            w=320,
            h=532,
            chip8_memory=chip8.memory,
            chip8_pc=chip8.pc)
        self.drawables.append(memory_view)

        index_view = IndexView(
            screen=screen,
            font=self.font,
            x=memory_view.right + MARGIN,
            y=game_screen.top,
            w=160,
            h=52,
            chip8_index=chip8.index)
        self.drawables.append(index_view)

        delay_timer_view = TimerView(
            screen=screen,
            font=self.font,
            x=memory_view.right + MARGIN,
            y=index_view.bottom + MARGIN,
            w=160,
            h=52,
            name='Delay Timer',
            chip8_timer=chip8.delay_timer)
        self.drawables.append(delay_timer_view)

        sound_timer_view = TimerView(
            screen=screen,
            font=self.font,
            x=memory_view.right + MARGIN,
            y=delay_timer_view.bottom + MARGIN,
            w=160,
            h=52,
            name='Sound Timer',
            chip8_timer=chip8.delay_timer)
        self.drawables.append(sound_timer_view)

        registers_view = RegistersView(
            screen=screen,
            font=self.font,
            x=memory_view.right + MARGIN,
            y=sound_timer_view.bottom + MARGIN,
            w=160,
            h=164,
            chip8_registers=chip8.registers)
        self.drawables.append(registers_view)

        stack_view = StackView(
            screen=screen,
            font=self.font,
            x=memory_view.right + MARGIN,
            y=registers_view.bottom + MARGIN,
            w=160,
            h=memory_view.h - registers_view.bottom,
            chip8_stack=chip8.stack)
        self.drawables.append(stack_view)

        # Game controls label:

        text = ''
        text += 'Game controls\n'
        text += '\n'
        text += '+---+---+---+---+       +---+---+---+---+\n'
        text += '| 1 | 2 | 3 | C |   →   | 1 | 2 | 3 | 4 |\n'
        text += '+---+---+---+---+       +---+---+---+---+\n'
        text += '| 4 | 5 | 6 | D |   →   | Q | W | E | R |\n'
        text += '+---+---+---+---+       +---+---+---+---+\n'
        text += '| 7 | 8 | 9 | E |   →   | A | S | D | F |\n'
        text += '+---+---+---+---+       +---+---+---+---+\n'
        text += '| A | 0 | B | F |   →   | Z | X | C | V |\n'
        text += '+---+---+---+---+       +---+---+---+---+'

        game_controls_label = Label(
            screen=screen,
            font=self.font,
            x=MARGIN,
            y=game_screen.bottom + MARGIN,
            w=440,
            h=memory_view.bottom - game_screen.bottom - MARGIN,
            text=text)
        self.drawables.append(game_controls_label)

        # CHIP-8 interpreter controls label:

        text = ''
        text += 'CHIP-8 controls\n'
        text += '\n'
        text += ' F1:  Play/Pause\n'
        text += ' F2:  Step\n'
        text += ' F3:  Reset\n'
        text += ' ESC: Quit\n'

        interpreter_controls_label = Label(
            screen=screen,
            font=self.font,
            x=game_controls_label.right + MARGIN,
            y=game_screen.bottom + MARGIN,
            w=memory_view.left - 2*MARGIN - game_controls_label.right,
            h=memory_view.bottom - game_screen.bottom - MARGIN,
            text=text)
        self.drawables.append(interpreter_controls_label)


    def draw(self) -> None:
        for drawable in self.drawables:
            drawable.draw()


class GameScreen(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, pixel_size: int, chip8_display: chip8.Display) -> None:
        super().__init__(screen=screen, x=x, y=y, w=chip8_display.pixels_width * pixel_size, h=chip8_display.pixels_height * pixel_size)
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

        self.draw_frame()


class MemoryView(Drawable):

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font,
        x: int,
        y: int,
        w: int,
        h: int,
        chip8_memory: chip8.Memory,
        chip8_pc: chip8.ProgramCounter) -> None:

        super().__init__(screen, font, x, y, w, h)

        self.chip8_memory = chip8_memory
        self.chip8_pc = chip8_pc

        self.addresses_to_show = 64


    def draw(self) -> None:
        lines = []
        lines.append('  ADDR  DATA  MNEMONIC        ')

        for i in range(-self.addresses_to_show // 2 + 2, self.addresses_to_show // 2, 2):
            address = self.chip8_pc.value + i

            if address < 0:
                address += self.chip8_memory.size

            first_byte = self.chip8_memory[address]
            second_byte = self.chip8_memory[address + 1]

            marker = '→' if i == 0 else ' '
            lines.append(f'{marker}  {to_hex(address, 3)}  {to_hex(first_byte, 2)}{to_hex(second_byte, 2)}')

        self.draw_text(lines, highlights=[16])
        self.draw_frame()


class IndexView(Drawable):

    def __init__(self, screen: pygame.Surface, font: pygame.font, x: int, y: int, w: int, h: int, chip8_index: chip8.IndexRegister) -> None:
        super().__init__(screen, font, x, y, w, h)
        self.chip8_index = chip8_index


    def draw(self) -> None:
        lines = [
            'Index register',
            f' {to_hex(self.chip8_index.value, 4)}',
        ]

        self.draw_text(lines)
        self.draw_frame()


class TimerView(Drawable):

    def __init__(
        self,
        screen: pygame.Surface,
        font: pygame.font,
        x: int,
        y: int,
        w: int,
        h: int,
        name: str,
        chip8_timer: chip8.DelayTimer) -> None:

        super().__init__(screen, font, x, y, w, h)

        self.name = name
        self.chip8_timer = chip8_timer


    def draw(self) -> None:
        lines = [
            self.name,
            f' {to_hex(self.chip8_timer.value, 2)}',
        ]

        self.draw_text(lines)
        self.draw_frame()


class RegistersView(Drawable):

    def __init__(self, screen: pygame.Surface, font: pygame.font, x: int, y: int, w: int, h: int, chip8_registers: chip8.Registers) -> None:
        super().__init__(screen, font, x, y, w, h)
        self.chip8_registers = chip8_registers


    def draw(self) -> None:
        register_count = len(self.chip8_registers)
        lines = [f' V{to_hex(i, 1)} {to_hex(register, 2)}' for i, register in enumerate(self.chip8_registers)]
        
        self.draw_text(['Registers'])
        self.draw_text(lines[:register_count//2], y_offset=FONT_SIZE)
        self.draw_text(lines[register_count // 2:], x_offset=FONT_WIDTH*7, y_offset=FONT_SIZE)

        self.draw_frame()


class StackView(Drawable):

    def __init__(self, screen: pygame.Surface, font: pygame.font, x: int, y: int, w: int, h: int, chip8_stack: chip8.Stack) -> None:
        super().__init__(screen, font, x, y, w, h)
        self.chip8_stack = chip8_stack


    def draw(self) -> None:
        lines = [f' {to_hex(self.chip8_stack[i], 2)}' for i in range(len(self.chip8_stack))]

        self.draw_text(['Stack'])
        self.draw_text(lines[:8], y_offset=FONT_SIZE)
        self.draw_text(lines[8:16], x_offset=FONT_WIDTH*4, y_offset=FONT_SIZE)
        self.draw_text(lines[16:], x_offset=FONT_WIDTH*8, y_offset=FONT_SIZE)
        self.draw_frame()


class Label(Drawable):

    def __init__(self, screen: pygame.Surface, font: pygame.font, x: int, y: int, w: int, h: int, text: str) -> None:
        super().__init__(screen, font, x, y, w, h)
        self.lines = text.splitlines()


    def draw(self) -> None:
        self.draw_text(self.lines)
        self.draw_frame()
