from typing import List

import pygame

import chip8
from constants import *


class Drawable:

    def __init__(self, screen: pygame.Surface, x: int, y: int, w: int = 0, h: int = 0) -> None:
        self.screen = screen
        self.x = x
        self.y = y


    @property
    def width(self) -> int:
        raise NotImplementedError()


    @property
    def height(self) -> int:
        raise NotImplementedError()


    def draw(self) -> None:
        raise NotImplementedError()


class Panel(Drawable):

    def __init__(self, screen: pygame.Surface, chip8: chip8.Chip8) -> None:
        super().__init__(screen, 0, 0)

        self.drawables: List[Drawable] = []

        gamescreen = GameScreen(screen=screen, x=MARGIN, y=MARGIN, pixel_size=PIXEL_SIZE, chip8_display=chip8.display)
        self.drawables.append(gamescreen)


    def draw(self) -> None:
        for drawable in self.drawables:
            drawable.draw()


class GameScreen(Drawable):

    def __init__(self, screen: pygame.Surface, x: int, y: int, pixel_size: int, chip8_display: chip8.Display) -> None:
        super().__init__(screen, x, y)
        self.pixel_size = pixel_size
        self.chip8_display = chip8_display

        self.w = self.chip8_display.pixels_width * self.pixel_size
        self.h = self.chip8_display.pixels_height * self.pixel_size


    @property
    def width(self) -> int:
        return self.chip8_display.pixels_width * self.pixel_size


    @property
    def height(self) -> int:
        return self.chip8_display.pixels_height * self.pixel_size


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