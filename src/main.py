import datetime
from typing import List

import pygame

import chip8


PIXEL_SIZE = 10
PIXEL_ON_COLOR = (255, 255, 255)
PIXEL_OFF_COLOR = (0, 0, 0)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
MARGIN = 10
SCREEN_GEOMETRY = (SCREEN_WIDTH, SCREEN_HEIGHT)
BACKGROUND_COLOR = (40, 40, 40)
FONT_FAMILY = 'monospace'
FONT_SIZE = 12

CHIP8_STEPS_PER_SECOND = 720


class Engine:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        self.font = pygame.font.SysFont(FONT_FAMILY, FONT_SIZE)

        self.screen = pygame.display.set_mode(SCREEN_GEOMETRY, 0, 32)
        pygame.display.set_caption('CHIP-8 Interpreter')

        self.chip8 = chip8.Chip8()
        self.init_panel()


    def init_panel(self) -> None:
        self.drawables: List[Drawable] = []

        self.gamescreen = GameScreen(screen=self.screen, x=MARGIN, y=MARGIN, pixel_size=PIXEL_SIZE, chip8_display=self.chip8.display)
        self.drawables.append(self.gamescreen)


    def run(self) -> None:
        clock = pygame.time.Clock()
        self.running = True
        step = 0

        steps_per_frame = CHIP8_STEPS_PER_SECOND // 60

        while self.running:

            if step % steps_per_frame == 0:
                self.manage_inputs()
            
            self.update()
            
            if step % steps_per_frame == 0:
                self.draw()

            clock.tick(CHIP8_STEPS_PER_SECOND)
            step += 1


    def manage_inputs(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False


    def update(self) -> None:
        pass


    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)

        for drawable in self.drawables:
            drawable.draw()

        pygame.display.update()


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


if __name__ == '__main__':
    engine = Engine()
    engine.run()
