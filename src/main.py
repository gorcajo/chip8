import datetime
from typing import List

import pygame

import chip8
from constants import *
import ui


class Engine:

    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(SCREEN_GEOMETRY, 0, 32)
        pygame.display.set_caption('CHIP-8 Interpreter')

        self.chip8 = chip8.Chip8()
        self.panel = ui.Panel(self.screen, self.chip8)


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
        self.panel.draw()
        pygame.display.update()


if __name__ == '__main__':
    engine = Engine()
    engine.run()
