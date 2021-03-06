from __future__ import annotations
import os
import random
from typing import List

from pygame import key

from instruction import Instruction, OperationType, OperandType
from tools import *


class Chip8:

    def __init__(self, rom: Rom) -> None:
        self.memory = Memory(4096, rom)
        self.display = Display(64, 32)
        self.pc = ProgramCounter(4096)
        self.index = IndexRegister()
        self.stack = Stack()
        self.delay_timer = Timer()
        self.sound_timer = Timer()
        self.registers = Registers(16)

        self.current_step = 0
        self.previous_keys_pressed: List[int] = []

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


    def step(self, keys_pressed: List[int] = None) -> None:
        # Keys:

        if keys_pressed is None:
            keys_pressed = []

        key_press_changes = keys_pressed != self.previous_keys_pressed

        # Fetch:

        address = self.pc.value
        self.pc.increment()

        # Decode:

        instruction = Instruction(self.memory[address], self.memory[address+1])

        # Execute:

        if instruction.type == OperationType.MACHINE_CODE:
            pass

        elif instruction.type == OperationType.CLEAR_SCREEN:
            self.display.clear()

        elif instruction.type == OperationType.RETURN_FROM_SUBROUTINE:
            address = self.stack.pop()

            if address is not None:
                self.pc.set_to(address)

        elif instruction.type == OperationType.ABSOLUTE_JUMP:
            self.pc.set_to(instruction.operands[0].value)

        elif instruction.type == OperationType.CALL_SUBROUTINE:
            self.stack.push(self.pc.value)
            self.pc.set_to(instruction.operands[0].value)

        elif instruction.type == OperationType.SKIP_IF_EQUALS:
            first_operand = instruction.operands[0]
            second_operand = instruction.operands[1]

            first_register = self.registers[first_operand.value]

            if second_operand.type == OperandType.LITERAL:
                if first_register.value == second_operand.value:
                    self.pc.increment()
            elif second_operand.type == OperandType.REGISTER:
                second_register = self.registers[second_operand.value]
                if first_register.value == second_register.value:
                    self.pc.increment()
            else:
                raise ValueError('Illegal instruction')

        elif instruction.type == OperationType.SKIP_IF_NOT_EQUALS:
            first_operand = instruction.operands[0]
            second_operand = instruction.operands[1]

            first_register = self.registers[first_operand.value]

            if second_operand.type == OperandType.LITERAL:
                if first_register.value != second_operand.value:
                    self.pc.increment()
            elif second_operand.type == OperandType.REGISTER:
                second_register = self.registers[second_operand.value]
                if first_register.value != second_register.value:
                    self.pc.increment()
            else:
                raise ValueError('Illegal instruction')

        elif instruction.type == OperationType.COPY:
            target = instruction.operands[0]
            source = instruction.operands[1]

            if target.type == OperandType.REGISTER:
                if source.type == OperandType.LITERAL:
                    self.registers[target.value].set_to(source.value)
                elif source.type == OperandType.REGISTER:
                    new_value = self.registers[source.value].value
                    self.registers[target.value].set_to(new_value)
                else:
                    raise ValueError('Illegal instruction')

            elif target.type == OperandType.INDEX and source.type == OperandType.LITERAL:
                self.index.set_to(source.value)

            else:
                raise ValueError('Illegal instruction')

        elif instruction.type == OperationType.ADD_WITHOUT_CARRY:
            target = instruction.operands[0]
            source = instruction.operands[1]

            if target.type == OperandType.REGISTER and source.type == OperandType.LITERAL:
                register_content = self.registers[target.value].value
                self.registers[target.value].set_to((register_content + source.value) & 0x00ff)
            elif target.type == OperandType.INDEX and source.type == OperandType.REGISTER:
                index_content = self.index.value
                register_content = self.registers[source.value].value
                self.index.set_to((index_content + register_content) & 0xffff)
            else:
                raise ValueError('Illegal instruction')

        elif instruction.type == OperationType.BITWISE_OR:
            target_register = self.registers[instruction.operands[0].value]
            other_register = self.registers[instruction.operands[1].value]
            target_register.set_to(target_register.value | other_register.value)

        elif instruction.type == OperationType.BITWISE_AND:
            target_register = self.registers[instruction.operands[0].value]
            other_register = self.registers[instruction.operands[1].value]
            target_register.set_to(target_register.value & other_register.value)

        elif instruction.type == OperationType.BITWISE_XOR:
            target_register = self.registers[instruction.operands[0].value]
            other_register = self.registers[instruction.operands[1].value]
            target_register.set_to(target_register.value ^ other_register.value)

        elif instruction.type == OperationType.ADD_WITH_CARRY:
            target_register = self.registers[instruction.operands[0].value]
            other_register = self.registers[instruction.operands[1].value]

            result = target_register.value + other_register.value
            target_register.set_to(result & 0x00ff)

            if result > 0x00ff:
                self.registers.turn_on_flag()

        elif instruction.type == OperationType.SUBTRACTION_DIRECT:
            first_register = self.registers[instruction.operands[0].value]
            second_register = self.registers[instruction.operands[1].value]

            if first_register.value >= second_register.value:
                self.registers.turn_on_flag()
            else:
                self.registers.turn_off_flag()

            result = first_register.value - second_register.value
            first_register.set_to(result & 0x00ff)

        elif instruction.type == OperationType.SHIFT_RIGHT:
            target_register = self.registers[instruction.operands[0].value]

            if target_register.value & 0x01 == 0x01:
                self.registers.turn_on_flag()
            else:
                self.registers.turn_off_flag()

            target_register.set_to((target_register.value >> 1) & 0x00ff)

        elif instruction.type == OperationType.SUBTRACTION_REVERSE:
            first_register = self.registers[instruction.operands[0].value]
            second_register = self.registers[instruction.operands[1].value]

            if first_register.value >= second_register.value:
                self.registers.turn_off_flag()
            else:
                self.registers.turn_on_flag()

            result = second_register.value - first_register.value
            first_register.set_to(result & 0x00ff)

        elif instruction.type == OperationType.SHIFT_LEFT:
            target_register = self.registers[instruction.operands[0].value]

            if target_register.value & 0x80 == 0x80:
                self.registers.turn_on_flag()
            else:
                self.registers.turn_off_flag()

            target_register.set_to((target_register.value << 1) & 0x00ff)

        elif instruction.type == OperationType.ABSOLUTE_JUMP_WITH_OFFSET:
            v0_register = self.registers[0x00]
            self.pc.set_to((instruction.operands[0].value + v0_register.value) & 0x00ff)

        elif instruction.type == OperationType.RANDOM_NUMBER:
            target_register = self.registers[instruction.operands[0].value]
            literal = instruction.operands[1].value

            random_value = random.randint(0, 0xff)
            result = random_value & literal
            target_register.set_to(random_value & literal)

        elif instruction.type == OperationType.DRAW:
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

        elif instruction.type == OperationType.SKIP_IF_KEY_PRESSED:
            key = self.registers[instruction.operands[0].value].value

            if key in keys_pressed:
                self.pc.increment()

        elif instruction.type == OperationType.SKIP_IF_KEY_NOT_PRESSED:
            key = self.registers[instruction.operands[0].value].value

            if key not in keys_pressed:
                self.pc.increment()

        elif instruction.type == OperationType.GET_DELAY_TIMER:
            register = self.registers[instruction.operands[0].value]
            register.set_to(self.delay_timer.value)

        elif instruction.type == OperationType.WAIT_FOR_KEY:
            if not key_press_changes:
                self.pc.set_to(self.pc.value - 2)
            else:
                if len(self.previous_keys_pressed) > len(keys_pressed):
                    key = list(set(self.previous_keys_pressed) - set(keys_pressed))[0]
                    self.registers[instruction.operands[0].value].set_to(key)
                else:
                    self.pc.set_to(self.pc.value - 2)

        elif instruction.type == OperationType.SET_DELAY_TIMER:
            value = self.registers[instruction.operands[0].value].value
            self.delay_timer.set_value(value)

        elif instruction.type == OperationType.SET_SOUND_TIMER:
            value = self.registers[instruction.operands[0].value].value
            self.sound_timer.set_value(value)

        elif instruction.type == OperationType.LOAD_FONT:
            character = self.registers[instruction.operands[0].value].value & 0x0f
            font_addr = self.memory.first_char + 5 * character
            self.index.set_to(font_addr)

        elif instruction.type == OperationType.BCD_CONVERSION:
            number = self.registers[instruction.operands[0].value].value

            units = number % 10
            tens = (number // 10) % 10
            hundreds = number // 100

            self.memory.set_address_to(self.index.value, hundreds)
            self.memory.set_address_to(self.index.value + 1, tens)
            self.memory.set_address_to(self.index.value + 2, units)

        elif instruction.type == OperationType.DUMP_REGISTERS_TO_MEMORY:
            last_register = instruction.operands[0].value & 0x0f

            for i in range(last_register + 1):
                number = self.registers[i].value
                self.memory.set_address_to(self.index.value + i, number)

        elif instruction.type == OperationType.LOAD_REGISTER_FROM_MEMORY:
            last_register = instruction.operands[0].value & 0x0f

            for i in range(last_register + 1):
                self.registers[i].set_to(self.memory[self.index.value + i])

        # Keys:

        self.previous_keys_pressed = keys_pressed

        # Timers

        if self.current_step % (CHIP8_STEPS_PER_SECOND // CHIP8_TIMER_UPDATES_PER_SECOND) == 0:
            self.delay_timer.decrement_if_greater_than_zero()
            self.sound_timer.decrement_if_greater_than_zero()

        self.current_step += 1


class Memory:

    def __init__(self, size: int, rom: Rom) -> None:
        self.size = size
        self.rom = rom

        self.addresses: List[int] = []

        self.bytes_reserved = 0x200
        self.first_char = 0x50
        self.char_size = 5

        self.clear()
        self.configure_font()
        self.load_rom()


    def clear(self) -> None:
        self.addresses = [0] * self.size


    def configure_font(self) -> None:
        fonts = [
            0xf0, 0x90, 0x90, 0x90, 0xf0, # 0x50: 0
            0x20, 0x60, 0x20, 0x20, 0x70, # 0x55: 1
            0xf0, 0x10, 0xf0, 0x80, 0xf0, # 0x5a: 2
            0xf0, 0x10, 0xf0, 0x10, 0xf0, # 0x5f: 3
            0x90, 0x90, 0xf0, 0x10, 0x10, # 0x64: 4
            0xf0, 0x80, 0xf0, 0x10, 0xf0, # 0x69: 5
            0xf0, 0x80, 0xf0, 0x90, 0xf0, # 0x6e: 6
            0xf0, 0x10, 0x20, 0x40, 0x40, # 0x73: 7
            0xf0, 0x90, 0xf0, 0x90, 0xf0, # 0x78: 8
            0xf0, 0x90, 0xf0, 0x10, 0xf0, # 0x7d: 9
            0xf0, 0x90, 0xf0, 0x90, 0x90, # 0x82: A
            0xe0, 0x90, 0xe0, 0x90, 0xe0, # 0x87: B
            0xf0, 0x80, 0x80, 0x80, 0xf0, # 0x8c: C
            0xe0, 0x90, 0x90, 0x90, 0xe0, # 0x91: D
            0xf0, 0x80, 0xf0, 0x80, 0xf0, # 0x96: E
            0xf0, 0x80, 0xf0, 0x80, 0x80, # 0x9b: F
        ]

        for i, byte in enumerate(fonts):
            self.addresses[i + self.first_char] = byte


    def get_addres_of_font(self, font: int) -> int:
        if font < 0 or font > 15:
            raise ValueError('a font must be between 0 and F in hexadecimal')

        return self.memory.first_char + self.char_size * font


    def load_rom(self) -> None:
        for i, byte in enumerate(self.rom.data):
            self.addresses[i + self.bytes_reserved] = byte


    def set_address_to(self, address: int, new_value: int) -> None:
        if new_value > 0xff:
            raise ValueError('value must fit in 1 byte')

        self.addresses[address % self.size] = new_value


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
        return self.pixels[y % self.height][x % self.width]


    def turn_on_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y % self.height][x % self.width] = True


    def turn_off_pixel_at(self, x: int, y: int) -> None:
        self.pixels[y % self.height][x % self.width] = False


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
        self._value = 0


    def set_value(self, new_value: int) -> None:
        self._value = new_value


    def decrement_if_greater_than_zero(self) -> None:
        if self._value > 0:
            self._value -= 1


    @property
    def value(self) -> None:
        return self._value


class Registers:

    def __init__(self, count: int) -> None:
        self.count = count
        self.registers: List[OneByteRegister] = None
        self.clear()


    def clear(self) -> None:
        self.registers = [OneByteRegister() for _ in range(self.count)]


    def turn_on_flag(self) -> None:
        self.registers[0xf].set_to(0x01)


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
