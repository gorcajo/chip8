from __future__ import annotations
import os
from typing import List

from tools import *


class Chip8:

    def __init__(self, rom: Rom) -> None:
        self.memory = Memory(4096, rom)
        self.display = Display(64, 32)
        self.pc = ProgramCounter()
        self.index = IndexRegister()
        self.stack = Stack()
        self.delay_timer = DelayTimer()
        self.sound_timer = SoundTimer()
        self.registers = Registers(16)

        self.reset()


    def reset(self) -> None:
        self.display.clear()
        self.pc.set_to(0)
        self.index.set_to(0)
        self.stack.clear()
        self.delay_timer.set_value(0)
        self.sound_timer.set_value(0)
        self.registers.clear()


    def step(self) -> None:
        address = self.pc.value
        instruction = Instruction(self.memory[address], self.memory[address+1])

        self.pc.increment()

        print(instruction) # TODO


class Instruction:

    def __init__(self, msb: int, lsb: int) -> None:
        self._k = msb >> 4
        self._x = msb & 0x0f
        self._y = lsb >> 4
        self._n = lsb & 0x0f


    @property
    def hex(self) -> str:
        return f'{to_hex(self._k, 1)}{to_hex(self._x, 1)}{to_hex(self._y, 1)}{to_hex(self._n, 1)}'


    @property
    def k(self) -> str:
        return f'{to_hex(self._k, 1)}'


    @property
    def x(self) -> str:
        return f'{to_hex(self._x, 1)}'


    @property
    def y(self) -> str:
        return f'{to_hex(self._y, 1)}'


    @property
    def n(self) -> str:
        return f'{to_hex(self._n, 1)}'


    @property
    def nn(self) -> str:
        return f'{to_hex(self._y, 1)}{to_hex(self._n, 1)}'


    @property
    def nnn(self) -> str:
        return f'{to_hex(self._x, 1)}{to_hex(self._y, 1)}{to_hex(self._n, 1)}'


    @property
    def asm(self) -> str:
        if self._k == 0x0:
            if self._x == 0x0 and self._y == 0xe and self._n == 0x0:
                return f'clr'
            elif self._x == 0x0 and self._y == 0xe and self._n == 0xe:
                return f'ret'
            else:
                return f'mch {self.nnn}'
        elif self._k == 0x1:
            return f'jmp {self.nnn}'
        elif self._k == 0x2:
            return f'call {self.nnn}'
        elif self._k == 0x3:
            return f'jeq v{self.x} {self.nn}'
        elif self._k == 0x4:
            return f'jneq v{self.x} {self.nn}'
        elif self._k == 0x5 and self._n == 0x0:
            return f'jeq v{self.x} v{self.y}'
        elif self._k == 0x6:
            return f'mov v{self.x} {self.nn}'
        elif self._k == 0x7:
            return f'addnc v{self.x} {self.nn}'
        elif self._k == 0x8:
            if self._n == 0x0:
                return f'mov v{self.x} v{self.y}'
            elif self._n == 0x1:
                return f'or v{self.x} v{self.y}'
            elif self._n == 0x2:
                return f'and v{self.x} v{self.y}'
            elif self._n == 0x3:
                return f'xor v{self.x} v{self.y}'
            elif self._n == 0x4:
                return f'add v{self.x} v{self.y}'
            elif self._n == 0x5:
                return f'sub v{self.x} v{self.y}'
            elif self._n == 0x6:
                return f'rsh v{self.x}'
            elif self._n == 0x7:
                return f'subr v{self.y} v{self.x}'
            elif self._n == 0xe:
                return f'lsh v{self.x}'
        elif self._k == 0x9 and self._n == 0x0:
            return f'jneq v{self.x} v{self.y}'
        elif self._k == 0xa:
            return f'mov I {self.nnn}'
        elif self._k == 0xb:
            return f'jmpv0 {self.nnn}'
        elif self._k == 0xc:
            return f'rnd v{self.x} {self.nn}'
        elif self._k == 0xd:
            return f'draw v{self.x} v{self.y} {self.n}'
        elif self._k == 0xe:
            if self._y == 0x9 and self._n == 0xe:
                return f'jkey {self.x}'
            elif self._y == 0xa and self._n == 0x1:
                return f'jnkey v{self.x}'
        elif self._k == 0xf:
            if self._y == 0x0 and self._n == 0x7:
                return f'gdly v{self.x}'
            elif self._y == 0x1 and self._n == 0x5:
                return f'sdly v{self.x}'
            elif self._y == 0x1 and self._n == 0x8:
                return f'ssdn v{self.x}'
            elif self._y == 0x1 and self._n == 0xe:
                return f'addnc I v{self.x}'
            elif self._y == 0x0 and self._n == 0xa:
                return f'wkey v{self.x}'
            elif self._y == 0x2 and self._n == 0x9:
                return f'font v{self.x}'
            elif self._y == 0x3 and self._n == 0x3:
                return f'bcd v{self.x}'
            elif self._y == 0x5 and self._n == 0x5:
                return f'dump v{self.x}'
            elif self._y == 0x6 and self._n == 0x5:
                return f'load v{self.x}'

        return '???'


    def __str__(self) -> str:
        return f'{self.hex}: {self.asm}'



class Memory:

    def __init__(self, size: int, rom: Rom) -> None:
        self.size = size
        self.load(rom)


    def clear(self) -> None:
        self.addresses = [0] * self.size


    def load(self, rom: Rom) -> None:
        self.clear()

        for i, byte in enumerate(rom.data):
            self.addresses[i] = byte


    def __len__(self):
        return len(self.addresses)


    def __getitem__(self, address) -> int:
        return self.addresses[address]


class Display:

    def __init__(self, pixels_width: int, pixels_height: int) -> None:
        self.pixels_width = pixels_width
        self.pixels_height = pixels_height
        self.pixels: List[List[bool]] = None

        self.clear()


    def clear(self) -> None:
        self.pixels = [[False for i in range(self.pixels_width)] for i in range(self.pixels_height)]


    def get_pixel_at(self, x: int, y: int) -> bool:
        return self.pixels[y][x]


    def turn_on_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y][x] = True


    def turn_off_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y][x] = False


class TwoBytesRegister:

    def __init__(self) -> None:
        self._value: int = 0


    @property
    def value(self) -> int:
        return self._value


    def set_to(self, new_value: int) -> int:
        if new_value > 2**16:
            raise ValueError('value cannot fit in 2 bytes')

        self._value = new_value


class ProgramCounter(TwoBytesRegister):

    def increment(self) -> int:
        self._value += 2


class IndexRegister(TwoBytesRegister):
    pass


class Stack:

    def __init__(self) -> None:
        self._elements: List[int] = None
        self.clear()


    def push(self, element: int) -> None:
        self._elements.append(element)


    def pop(self) -> int:
        return self._elements.pop()


    def clear(self) -> None:
        self._elements = []


    def __len__(self):
        return len(self._elements)


    def __getitem__(self, i) -> int:
        return self._elements[i]


class Timer:

    def __init__(self) -> None:
        self.register = 0


    def set_value(self, new_value: int) -> None:
        self.register = new_value


    @property
    def value(self) -> None:
        return self.register


class DelayTimer(Timer):
    pass


class SoundTimer(Timer):
    pass


class Registers:

    def __init__(self, count: int) -> None:
        self.count = count
        self.registers: List[int] = None
        self.clear()


    def clear(self) -> None:
        self.registers = [0 for i in range(self.count)]


    def __getitem__(self, i) -> int:
        return self.registers[i]


    def __len__(self):
        return len(self.registers)


    @property
    def flag_register(self) -> int:
        return self.registers[-1]


class Rom:

    def __init__(self, filepath: str) -> None:
        self.data: List[int] = []
        
        if filepath is None:
            return
        elif not os.path.isfile(filepath):
            filepath = None
            return
        else:
            with open(filepath, 'rb') as rom_file:
                self.data = []

                while byte := rom_file.read(1):
                    self.data.append(byte[0])
