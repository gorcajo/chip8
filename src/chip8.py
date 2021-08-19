from typing import List


class Chip8:

    def __init__(self, rom: List[int]) -> None:
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
        self.pc.increment()


class Memory:

    def __init__(self, size: int, rom: List[int]) -> None:
        self.size = size
        self.load(rom)


    def clear(self) -> None:
        self.addresses = [0] * self.size


    def load(self, data: List[int]) -> None:
        self.clear()

        for i, byte in enumerate(data):
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
