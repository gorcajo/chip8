from enum import Enum

from tools import *


class Hexable:

    @property
    def hex(self) -> str:
        raise NotImplementedError()


class Instruction(Hexable):

    def __init__(self, msb: int, lsb: int) -> None:
        self._k = msb >> 4
        self._x = msb & 0x0f
        self._y = lsb >> 4
        self._n = lsb & 0x0f

        self._nn = lsb
        self._nnn = (self._x << 8) + lsb

        self.mnemonic: Mnemonic = None
        self.operands: List[Operand] = []

        self.decode()


    def decode(self) -> None:
        self.mnemonic = Mnemonic.UNKNOWN
        self.operands = []

        if self._k == 0x0:
            if self._x == 0x0 and self._y == 0xe and self._n == 0x0:
                self.mnemonic = Mnemonic.CLR
            elif self._x == 0x0 and self._y == 0xe and self._n == 0xe:
                self.mnemonic = Mnemonic.RET
            else:
                self.mnemonic = Mnemonic.MCH
                self.operands.append(Operand(OperandType.LITERAL, self._nnn))
        elif self._k == 0x1:
            self.mnemonic = Mnemonic.JMP
            self.operands.append(Operand(OperandType.LITERAL, self._nnn))
        elif self._k == 0x2:
            self.mnemonic = Mnemonic.CALL
            self.operands.append(Operand(OperandType.LITERAL, self._nnn))
        elif self._k == 0x3:
            self.mnemonic = Mnemonic.JEQ
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.LITERAL, self._nn))
        elif self._k == 0x4:
            self.mnemonic = Mnemonic.JNEQ
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.LITERAL, self._nn))
        elif self._k == 0x5 and self._n == 0x0:
            self.mnemonic = Mnemonic.JEQ
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.REGISTER, self._y))
        elif self._k == 0x6:
            self.mnemonic = Mnemonic.MOV
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.LITERAL, self._nn))
        elif self._k == 0x7:
            self.mnemonic = Mnemonic.ADDNC
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.LITERAL, self._nn))
        elif self._k == 0x8:
            if self._n == 0x0:
                self.mnemonic = Mnemonic.MOV
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x1:
                self.mnemonic = Mnemonic.OR
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x2:
                self.mnemonic = Mnemonic.AND
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x3:
                self.mnemonic = Mnemonic.XOR
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x4:
                self.mnemonic = Mnemonic.ADD
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x5:
                self.mnemonic = Mnemonic.SUB
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0x6:
                self.mnemonic = Mnemonic.RSH
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._n == 0x7:
                self.mnemonic = Mnemonic.SUBR
                self.operands.append(Operand(OperandType.REGISTER, self._x))
                self.operands.append(Operand(OperandType.REGISTER, self._y))
            elif self._n == 0xe:
                self.mnemonic = Mnemonic.LSH
                self.operands.append(Operand(OperandType.REGISTER, self._x))
        elif self._k == 0x9 and self._n == 0x0:
            self.mnemonic = Mnemonic.JNEQ
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.REGISTER, self._y))
        elif self._k == 0xa:
            self.mnemonic = Mnemonic.MOV
            self.operands.append(Operand(OperandType.INDEX))
            self.operands.append(Operand(OperandType.LITERAL, self._nnn))
        elif self._k == 0xb:
            self.mnemonic = Mnemonic.JMPV0
            self.operands.append(Operand(OperandType.LITERAL, self._nnn))
        elif self._k == 0xc:
            self.mnemonic = Mnemonic.RND
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.LITERAL, self._nn))
        elif self._k == 0xd:
            self.mnemonic = Mnemonic.DRAW
            self.operands.append(Operand(OperandType.REGISTER, self._x))
            self.operands.append(Operand(OperandType.REGISTER, self._y))
            self.operands.append(Operand(OperandType.LITERAL, self._n))
        elif self._k == 0xe:
            if self._y == 0x9 and self._n == 0xe:
                self.mnemonic = Mnemonic.JKEY
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0xa and self._n == 0x1:
                self.mnemonic = Mnemonic.JNKEY
                self.operands.append(Operand(OperandType.REGISTER, self._x))
        elif self._k == 0xf:
            if self._y == 0x0 and self._n == 0x7:
                self.mnemonic = Mnemonic.GDLY
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x1 and self._n == 0x5:
                self.mnemonic = Mnemonic.SDLY
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x1 and self._n == 0x8:
                self.mnemonic = Mnemonic.SSND
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x1 and self._n == 0xe:
                self.mnemonic = Mnemonic.ADDNC
                self.operands.append(Operand(OperandType.INDEX))
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x0 and self._n == 0xa:
                self.mnemonic = Mnemonic.WKEY
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x2 and self._n == 0x9:
                self.mnemonic = Mnemonic.FONT
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x3 and self._n == 0x3:
                self.mnemonic = Mnemonic.BCD
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x5 and self._n == 0x5:
                self.mnemonic = Mnemonic.DUMP
                self.operands.append(Operand(OperandType.REGISTER, self._x))
            elif self._y == 0x6 and self._n == 0x5:
                self.mnemonic = Mnemonic.LOAD
                self.operands.append(Operand(OperandType.REGISTER, self._x))


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
        assembly_line: str = None

        if self.mnemonic == Mnemonic.UNKNOWN:
            assembly_line = '???'
        else:
            assembly_line = self.mnemonic.name

        for operand in self.operands:
            if operand.type == OperandType.LITERAL:
                assembly_line += ' ' + operand.hex
            if operand.type == OperandType.REGISTER:
                assembly_line += ' V' + operand.hex
            if operand.type == OperandType.INDEX:
                assembly_line += ' I'
        
        return assembly_line.lower()


    def __str__(self) -> str:
        return f'Instruction({self.hex}, "{self.asm}")'


class Mnemonic(Enum):
    UNKNOWN = 0
    ADD = 1
    ADDNC = 2
    AND = 3
    BCD = 4
    CALL = 5
    CLR = 6
    DRAW = 7
    DUMP = 8
    FONT = 9
    GDLY = 10
    JEQ = 11
    JKEY = 12
    JMP = 13
    JMPV0 = 14
    JNEQ = 15
    JNKEY = 16
    LOAD = 17
    LSH = 18
    MCH = 19
    MOV = 20
    OR = 21
    RET = 22
    RND = 23
    RSH = 24
    SDLY = 25
    SSND = 26
    SUB = 27
    SUBR = 28
    WKEY = 29
    XOR = 30


class OperandType(Enum):
    LITERAL = 0
    REGISTER = 1
    INDEX = 2


class Operand(Hexable):

    def __init__(self, operand_type: OperandType, value: int = None) -> None:
        self.type = operand_type
        self.value = value


    @property
    def hex(self) -> str:
        if self.type == OperandType.INDEX:
            return ''

        if self.value < 16:
            return to_hex(self.value, 1)
        elif self.value < 256:
            return to_hex(self.value, 2)
        elif self.value < 4096:
            return to_hex(self.value, 4)
        else:
            raise ValueError('Operand is too large')
