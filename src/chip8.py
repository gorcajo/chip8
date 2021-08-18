class Chip8:

    def __init__(self) -> None:
        self.ram = Memory(4096)
        self.display = Display()
        self.pc = ProgramCounter()
        self.i = IndexRegister()
        self.stack = Stack()
        self.delay_timer = DelayTimer()
        self.sound_timer = SoundTimer()
        self.registers = Registers()


    def run(self):
        pass


class Memory:

    def __init__(self, size: int) -> None:
        self.addresses: bytes = [0] * size


    def __len__(self):
        return len(self.addresses)


class Display:

    def __init__(self) -> None:
        pass


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

    def __init__(self) -> None:
        self.registers = [0 for i in range(16)]


    def __getitem__(self, i) -> int:
        return self.registers[i]


    @property
    def flag_register(self) -> int:
        return self.registers[-1]
