from typing import List


class Chip8:

    def __init__(self) -> None:
        self.ram = Memory(4096)
        self.display = Display(64, 32)
        self.pc = ProgramCounter()
        self.i = IndexRegister()
        self.stack = Stack()
        self.delay_timer = DelayTimer()
        self.sound_timer = SoundTimer()
        self.registers = Registers(16)


class Memory:

    def __init__(self, size: int) -> None:
        self.addresses: bytes = [0] * size


    def __len__(self):
        return len(self.addresses)


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


class ProgramCounter:

    def __init__(self) -> None:
        pass


class IndexRegister:

    def __init__(self) -> None:
        pass


class Stack:

    def __init__(self) -> None:
        pass


class Timer:

    def __init__(self) -> None:
        self.register = 0


class DelayTimer(Timer):
    pass


class SoundTimer(Timer):
    pass


class Registers:

    def __init__(self, count: int) -> None:
        self.registers = [0 for i in range(count)]


    def __getitem__(self, i) -> int:
        return self.registers[i]


    @property
    def flag_register(self) -> int:
        return self.registers[-1]
