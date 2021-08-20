from __future__ import annotations
import os
from typing import List

from instruction import Instruction, Mnemonic, OperandType
from tools import *


class Chip8:

    def __init__(self, rom: Rom) -> None:
        self.memory = Memory(4096, rom)
        self.display = Display(64, 32)
        self.pc = ProgramCounter(4096)
        self.index = IndexRegister()
        self.stack = Stack()
        self.delay_timer = DelayTimer()
        self.sound_timer = SoundTimer()
        self.registers = Registers(16)

        self.reset()


    def reset(self) -> None:
        self.memory.configure_font()
        self.memory.load_rom()

        self.display.clear()
        self.pc.set_to(self.memory.bytes_reserved)
        self.index.set_to(0)
        self.stack.clear()
        self.delay_timer.set_value(0)
        self.sound_timer.set_value(0)
        self.registers.clear()


    def step(self) -> None:
        # Fetch:

        address = self.pc.value
        self.pc.increment()

        # Decode:

        instruction = Instruction(self.memory[address], self.memory[address+1])

        # Execute:

        if instruction.mnemonic == Mnemonic.MCH:
            pass

        elif instruction.mnemonic == Mnemonic.CLR:
            self.display.clear()

        elif instruction.mnemonic == Mnemonic.JMP:
            self.pc.set_to(instruction.operands[0].value)

        elif instruction.mnemonic == Mnemonic.CALL:
            self.stack.push(self.pc.value)
            self.pc.set_to(instruction.operands[0].value)

        elif instruction.mnemonic == Mnemonic.RET:
            address = self.stack.pop()

            if address is not None:
                self.pc.set_to(address)

        elif instruction.mnemonic == Mnemonic.MOV:
            target = instruction.operands[0]
            source = instruction.operands[1]

            if target.type == OperandType.REGISTER:
                if source.type == OperandType.LITERAL:
                    self.registers[target.value].set_to(source.value)
                elif source.type == OperandType.REGISTER:
                    pass # TODO
                else:
                    raise ValueError('Illegal instruction')

            elif target.type == OperandType.INDEX and source.type == OperandType.LITERAL:
                self.index.set_to(source.value)

            else:
                raise ValueError('Illegal instruction')

        elif instruction.mnemonic == Mnemonic.ADDNC:
            target = instruction.operands[0]
            source = instruction.operands[1]

            if target.type == OperandType.REGISTER and source.type == OperandType.LITERAL:
                register_content = self.registers[target.value].value
                self.registers[target.value].set_to((register_content + source.value) & 0x00ff)
            elif target.type == OperandType.INDEX and source.type == OperandType.REGISTER:
                pass # TODO
            else:
                raise ValueError('Illegal instruction')

        elif instruction.mnemonic == Mnemonic.DRAW:
            vx = instruction.operands[0]
            vy = instruction.operands[1]
            literal_n = instruction.operands[2]

            x = self.registers[vx.value].value % self.display.width
            y = self.registers[vy.value].value % self.display.height
            height = literal_n.value

            self.registers.turn_off_flag()

            for row in range(height):
                byte = self.memory[self.index.value + row]
                bits = byte_to_bool_list(byte)

                for col, bit in enumerate(bits):
                    if bit:
                        if self.display.get_pixel_at(x + col, y + row):
                            self.display.turn_off_pixel_at(x + col, y + row)
                            self.registers.turn_on_flag()
                        else:
                            self.display.turn_on_pixel_at(x + col, y + row)

                    if (x + col) >= self.display.width:
                        break

                if (y + row) >= self.display.height:
                    break


class Memory:

    def __init__(self, size: int, rom: Rom) -> None:
        self.size = size
        self.rom = rom

        self.bytes_reserved = 0x200

        self.clear()
        self.configure_font()
        self.load_rom()


    def clear(self) -> None:
        self.addresses = [0] * self.size


    def configure_font(self) -> None:
        fonts = [
            0xf0, 0x90, 0x90, 0x90, 0xf0, # 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 1
            0xf0, 0x10, 0xf0, 0x80, 0xf0, # 2
            0xf0, 0x10, 0xf0, 0x10, 0xf0, # 3
            0x90, 0x90, 0xf0, 0x10, 0x10, # 4
            0xf0, 0x80, 0xf0, 0x10, 0xf0, # 5
            0xf0, 0x80, 0xf0, 0x90, 0xf0, # 6
            0xf0, 0x10, 0x20, 0x40, 0x40, # 7
            0xf0, 0x90, 0xf0, 0x90, 0xf0, # 8
            0xf0, 0x90, 0xf0, 0x10, 0xf0, # 9
            0xf0, 0x90, 0xf0, 0x90, 0x90, # A
            0xe0, 0x90, 0xe0, 0x90, 0xe0, # B
            0xf0, 0x80, 0x80, 0x80, 0xf0, # C
            0xe0, 0x90, 0x90, 0x90, 0xe0, # D
            0xf0, 0x80, 0xf0, 0x80, 0xf0, # E
            0xf0, 0x80, 0xf0, 0x80, 0x80, # F
        ]

        for i, byte in enumerate(fonts):
            self.addresses[i + 0x50] = byte


    def load_rom(self) -> None:
        for i, byte in enumerate(self.rom.data):
            self.addresses[i + self.bytes_reserved] = byte


    def __len__(self):
        return len(self.addresses)


    def __getitem__(self, address) -> int:
        return self.addresses[address % self.size]


class Display:

    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
        self.pixels: List[List[bool]] = None

        self.clear()


    def clear(self) -> None:
        self.pixels = [[False for i in range(self.width)] for i in range(self.height)]


    def get_pixel_at(self, x: int, y: int) -> bool:
        return self.pixels[y][x]


    def turn_on_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y][x] = True


    def turn_off_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y][x] = False


class Register:

    def __init__(self) -> None:
        self._value: int = 0


    @property
    def value(self) -> int:
        return self._value


    def set_to(self, new_value: int) -> int:
        raise NotImplementedError()


class TwoBytesRegister(Register):

    def set_to(self, new_value: int) -> int:
        if new_value > 2**16:
            raise ValueError('value cannot fit in 2 bytes')

        self._value = new_value


class OneByteRegister(Register):

    def set_to(self, new_value: int) -> int:
        if new_value > 2**8:
            raise ValueError('value cannot fit in 1 byte')

        self._value = new_value


class ProgramCounter(TwoBytesRegister):

    def __init__(self, memory_size: int) -> None:
        super().__init__()
        self.memory_size = memory_size

    def increment(self) -> int:
        self._value += 2
        self._value %= self.memory_size


class IndexRegister(TwoBytesRegister):
    pass


class Stack:

    def __init__(self) -> None:
        self._elements: List[int] = None
        self.clear()


    def push(self, element: int) -> None:
        self._elements.append(element)


    def pop(self) -> int:
        if len(self._elements) == 0:
            return None

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
        self.registers: List[OneByteRegister] = None
        self.clear()


    def clear(self) -> None:
        self.registers = [OneByteRegister() for _ in range(self.count)]


    def turn_on_flag(self) -> None:
        self.registers[0xf].set_to(0xff)


    def turn_off_flag(self) -> None:
        self.registers[0xf].set_to(0x00)


    def __getitem__(self, i) -> OneByteRegister:
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
