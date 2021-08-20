from enum import Enum

from tools import *


class Hexable:

    @property
    def hex(self) -> str:
        raise NotImplementedError()


class Instruction(Hexable):

    def __init__(self, msb: int, lsb: int) -> None:
        self.k = msb >> 4
        self.x = msb & 0x0f
        self.y = lsb >> 4
        self.n = lsb & 0x0f

        self.nn = lsb
        self.nnn = (self.x << 8) + lsb

        self.mnemonic: Mnemonic = None
        self.operands: List[Operand] = []

        self.decode()


    def decode(self) -> None:
        self.mnemonic = Mnemonic.UNKNOWN
        self.operands = []

        if self.k == 0x0:
            if self.x == 0x0 and self.y == 0xe and self.n == 0x0:
                self.mnemonic = Mnemonic.CLR
            elif self.x == 0x0 and self.y == 0xe and self.n == 0xe:
                self.mnemonic = Mnemonic.RET
            else:
                self.mnemonic = Mnemonic.MCH
                self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x1:
            self.mnemonic = Mnemonic.JMP
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x2:
            self.mnemonic = Mnemonic.CALL
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x3:
            self.mnemonic = Mnemonic.JEQ
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x4:
            self.mnemonic = Mnemonic.JNEQ
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x5 and self.n == 0x0:
            self.mnemonic = Mnemonic.JEQ
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
        elif self.k == 0x6:
            self.mnemonic = Mnemonic.MOV
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x7:
            self.mnemonic = Mnemonic.ADDNC
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x8:
            if self.n == 0x0:
                self.mnemonic = Mnemonic.MOV
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x1:
                self.mnemonic = Mnemonic.OR
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x2:
                self.mnemonic = Mnemonic.AND
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x3:
                self.mnemonic = Mnemonic.XOR
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x4:
                self.mnemonic = Mnemonic.ADD
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x5:
                self.mnemonic = Mnemonic.SUB
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x6:
                self.mnemonic = Mnemonic.RSH
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.n == 0x7:
                self.mnemonic = Mnemonic.SUBR
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0xe:
                self.mnemonic = Mnemonic.LSH
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
        elif self.k == 0x9 and self.n == 0x0:
            self.mnemonic = Mnemonic.JNEQ
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
        elif self.k == 0xa:
            self.mnemonic = Mnemonic.MOV
            self.operands.append(Operand(OperandType.INDEX))
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0xb:
            self.mnemonic = Mnemonic.JMPV0
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0xc:
            self.mnemonic = Mnemonic.RND
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0xd:
            self.mnemonic = Mnemonic.DRAW
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.n, 1))
        elif self.k == 0xe:
            if self.y == 0x9 and self.n == 0xe:
                self.mnemonic = Mnemonic.JKEY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0xa and self.n == 0x1:
                self.mnemonic = Mnemonic.JNKEY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
        elif self.k == 0xf:
            if self.y == 0x0 and self.n == 0x7:
                self.mnemonic = Mnemonic.GDLY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0x5:
                self.mnemonic = Mnemonic.SDLY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0x8:
                self.mnemonic = Mnemonic.SSND
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0xe:
                self.mnemonic = Mnemonic.ADDNC
                self.operands.append(Operand(OperandType.INDEX))
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x0 and self.n == 0xa:
                self.mnemonic = Mnemonic.WKEY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x2 and self.n == 0x9:
                self.mnemonic = Mnemonic.FONT
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x3 and self.n == 0x3:
                self.mnemonic = Mnemonic.BCD
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x5 and self.n == 0x5:
                self.mnemonic = Mnemonic.DUMP
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x6 and self.n == 0x5:
                self.mnemonic = Mnemonic.LOAD
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))


    @property
    def hex(self) -> str:
        return f'{to_hex(self.k, 1)}{to_hex(self.x, 1)}{to_hex(self.y, 1)}{to_hex(self.n, 1)}'


    @property
    def asm(self) -> str:
        assembly_line: str = None

        if self.mnemonic == Mnemonic.UNKNOWN:
            assembly_line = '???'
        else:
            assembly_line = self.mnemonic.name

        for operand in self.operands:
            if operand.type == OperandType.LITERAL:
                assembly_line += ' #' + operand.hex
            if operand.type == OperandType.REGISTER:
                assembly_line += ' V' + operand.hex
            if operand.type == OperandType.INDEX:
                assembly_line += ' I'
        
        return assembly_line.lower()


    def __str__(self) -> str:
        return f'Instruction(0x{self.hex}, "{self.asm}")'


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

    def __init__(self, operand_type: OperandType, value: int = None, nibbles: int = None) -> None:
        self.type = operand_type

        if value is None and nibbles is not None:
            raise ValueError('You must specify a value')
        elif value is not None and nibbles is None:
            raise ValueError('You must specify a nibble count')

        self.value = value
        self.nibbles = nibbles


    @property
    def hex(self) -> str:
        if self.type == OperandType.INDEX:
            return ''

        return to_hex(self.value, self.nibbles)
