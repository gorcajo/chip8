from enum import Enum
import os
from typing import List
import sys

import pygame

import chip8
from constants import *
import ui


class Engine:

    def __init__(self, rom: chip8.Rom) -> None:
        pygame.init()
        pygame.font.init()

        self.screen = pygame.display.set_mode(SCREEN_GEOMETRY, 0, 32)
        pygame.display.set_caption('CHIP-8 Interpreter [PAUSED]')

        self.last_event: Key = None
        self.keys_pressed: List[Key] = []

        self.chip8 = chip8.Chip8(rom)
        self.panel = ui.Panel(self.screen, self.chip8)


    def run(self) -> None:
        clock = pygame.time.Clock()
        self.running = True

        steps_per_frame = CHIP8_STEPS_PER_SECOND // 60

        step = 0
        self.chip8_paused = True

        while self.running:
            self.manage_inputs()
            self.update()
            
            if step % steps_per_frame == 0:
                self.draw()

            clock.tick(CHIP8_STEPS_PER_SECOND)
            step += 1


    def manage_inputs(self) -> None:
        self.last_event: Key = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key in CONTROLS_MAP:
                    self.last_event = CONTROLS_MAP[event.key]

        self.keys_pressed = []

        for key in CONTROLS_MAP.keys():
            if pygame.key.get_pressed()[key] == 1:
                if CONTROLS_MAP[key].value >= 0x00 and CONTROLS_MAP[key].value <= 0x0f:
                    self.keys_pressed.append(CONTROLS_MAP[key])


    def update(self) -> None:
        if self.last_event is not None:
            if self.last_event == Key.KEY_STEP and self.chip8_paused:
                self.chip8.step()
            elif self.last_event == Key.KEY_RESET:
                self.chip8_paused = True
                self.chip8.reset()
                pygame.display.set_caption('CHIP-8 Interpreter [PAUSED]')
            elif self.last_event == Key.KEY_PLAY_PAUSE:
                self.chip8_paused = not self.chip8_paused

                if self.chip8_paused:
                    pygame.display.set_caption('CHIP-8 Interpreter [PAUSED]')
                else:
                    pygame.display.set_caption('CHIP-8 Interpreter [RUNNING]')

        if not self.chip8_paused:
            self.chip8.step([k.value for k in self.keys_pressed])


    def draw(self) -> None:
        self.screen.fill(BACKGROUND_COLOR)
        self.panel.draw()
        pygame.display.update()


class Key(Enum):
    KEY_0 = 0
    KEY_1 = 1
    KEY_2 = 2
    KEY_3 = 3
    KEY_4 = 4
    KEY_5 = 5
    KEY_6 = 6
    KEY_7 = 7
    KEY_8 = 8
    KEY_9 = 9
    KEY_A = 10
    KEY_B = 11
    KEY_C = 12
    KEY_D = 13
    KEY_E = 14
    KEY_F = 15
    KEY_PLAY_PAUSE = 16
    KEY_STEP = 17
    KEY_RESET = 18
    
CONTROLS_MAP = {
    pygame.K_F1: Key.KEY_PLAY_PAUSE,
    pygame.K_F2: Key.KEY_STEP,
    pygame.K_F3: Key.KEY_RESET,
    pygame.K_x: Key.KEY_0,
    pygame.K_1: Key.KEY_1,
    pygame.K_2: Key.KEY_2,
    pygame.K_3: Key.KEY_3,
    pygame.K_q: Key.KEY_4,
    pygame.K_w: Key.KEY_5,
    pygame.K_e: Key.KEY_6,
    pygame.K_a: Key.KEY_7,
    pygame.K_s: Key.KEY_8,
    pygame.K_d: Key.KEY_9,
    pygame.K_z: Key.KEY_A,
    pygame.K_c: Key.KEY_B,
    pygame.K_4: Key.KEY_C,
    pygame.K_r: Key.KEY_D,
    pygame.K_f: Key.KEY_E,
    pygame.K_v: Key.KEY_F,
}


if __name__ == '__main__':
    rom_filepath = sys.argv[1] if len(sys.argv) > 1 else None
    rom = chip8.Rom(rom_filepath)

    engine = Engine(rom)
    engine.run()
