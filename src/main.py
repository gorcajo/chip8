from enum import Enum
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

        self.last_event: Event = None

        self.chip8 = chip8.Chip8()
        self.panel = ui.Panel(self.screen, self.chip8)


    def run(self) -> None:
        clock = pygame.time.Clock()
        self.running = True
        step = 0

        steps_per_frame = CHIP8_STEPS_PER_SECOND // 60

        while self.running:
            self.manage_inputs()
            self.update()
            
            if step % steps_per_frame == 0:
                self.draw()

            clock.tick(CHIP8_STEPS_PER_SECOND)
            step += 1


    def manage_inputs(self) -> None:
        self.last_event: Event = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in CONTROLS_MAP:
                    self.last_event = CONTROLS_MAP[event.key]


    def update(self) -> None:
        if self.last_event is not None:
            print(self.last_event)


    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.panel.draw()
        pygame.display.update()


class Event(Enum):
    KEY_PLAY_PAUSE = 0
    KEY_STEP = 1
    KEY_RESET = 2
    KEY_0 = 3
    KEY_1 = 4
    KEY_2 = 5
    KEY_3 = 6
    KEY_4 = 7
    KEY_5 = 8
    KEY_6 = 9
    KEY_7 = 10
    KEY_8 = 11
    KEY_9 = 12
    KEY_A = 13
    KEY_B = 14
    KEY_C = 15
    KEY_D = 16
    KEY_E = 17
    KEY_F = 18
    
CONTROLS_MAP = {
    pygame.K_F1: Event.KEY_PLAY_PAUSE,
    pygame.K_F2: Event.KEY_STEP,
    pygame.K_F3: Event.KEY_RESET,
    pygame.K_x: Event.KEY_0,
    pygame.K_1: Event.KEY_1,
    pygame.K_2: Event.KEY_2,
    pygame.K_3: Event.KEY_3,
    pygame.K_q: Event.KEY_4,
    pygame.K_w: Event.KEY_5,
    pygame.K_e: Event.KEY_6,
    pygame.K_a: Event.KEY_7,
    pygame.K_s: Event.KEY_8,
    pygame.K_d: Event.KEY_9,
    pygame.K_z: Event.KEY_A,
    pygame.K_c: Event.KEY_B,
    pygame.K_4: Event.KEY_C,
    pygame.K_r: Event.KEY_D,
    pygame.K_f: Event.KEY_E,
    pygame.K_v: Event.KEY_F,
}


if __name__ == '__main__':
    engine = Engine()
    engine.run()
