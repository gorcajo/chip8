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
        self.nnn = (self.x << 8) | lsb

        self.type: OperationType = None
        self.operands: List[Operand] = []

        self.decode()


    def decode(self) -> None:
        self.type = OperationType.UNKNOWN
        self.operands = []

        if self.k == 0x0:
            if self.x == 0x0 and self.y == 0xe and self.n == 0x0:
                self.type = OperationType.CLEAR_SCREEN
            elif self.x == 0x0 and self.y == 0xe and self.n == 0xe:
                self.type = OperationType.RETURN_FROM_SUBROUTINE
            else:
                self.type = OperationType.MACHINE_CODE
                self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x1:
            self.type = OperationType.ABSOLUTE_JUMP
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x2:
            self.type = OperationType.CALL_SUBROUTINE
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0x3:
            self.type = OperationType.SKIP_IF_EQUALS
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x4:
            self.type = OperationType.SKIP_IF_NOT_EQUALS
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x5 and self.n == 0x0:
            self.type = OperationType.SKIP_IF_EQUALS
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
        elif self.k == 0x6:
            self.type = OperationType.COPY
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x7:
            self.type = OperationType.ADD_WITHOUT_CARRY
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0x8:
            if self.n == 0x0:
                self.type = OperationType.COPY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x1:
                self.type = OperationType.BITWISE_OR
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x2:
                self.type = OperationType.BITWISE_AND
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x3:
                self.type = OperationType.BITWISE_XOR
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x4:
                self.type = OperationType.ADD_WITH_CARRY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x5:
                self.type = OperationType.SUBTRACTION_DIRECT
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0x6:
                self.type = OperationType.SHIFT_RIGHT
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.n == 0x7:
                self.type = OperationType.SUBTRACTION_REVERSE
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
                self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            elif self.n == 0xe:
                self.type = OperationType.SHIFT_LEFT
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
        elif self.k == 0x9 and self.n == 0x0:
            self.type = OperationType.SKIP_IF_NOT_EQUALS
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
        elif self.k == 0xa:
            self.type = OperationType.COPY
            self.operands.append(Operand(OperandType.INDEX))
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0xb:
            self.type = OperationType.ABSOLUTE_JUMP_WITH_OFFSET
            self.operands.append(Operand(OperandType.LITERAL, self.nnn, 3))
        elif self.k == 0xc:
            self.type = OperationType.RANDOM_NUMBER
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.nn, 2))
        elif self.k == 0xd:
            self.type = OperationType.DRAW
            self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            self.operands.append(Operand(OperandType.REGISTER, self.y, 1))
            self.operands.append(Operand(OperandType.LITERAL, self.n, 1))
        elif self.k == 0xe:
            if self.y == 0x9 and self.n == 0xe:
                self.type = OperationType.SKIP_IF_KEY_PRESSED
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0xa and self.n == 0x1:
                self.type = OperationType.SKIP_IF_KEY_NOT_PRESSED
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
        elif self.k == 0xf:
            if self.y == 0x0 and self.n == 0x7:
                self.type = OperationType.GET_DELAY_TIMER
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0x5:
                self.type = OperationType.SET_DELAY_TIMER
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0x8:
                self.type = OperationType.SET_SOUND_TIMER
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x1 and self.n == 0xe:
                self.type = OperationType.ADD_WITHOUT_CARRY
                self.operands.append(Operand(OperandType.INDEX))
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x0 and self.n == 0xa:
                self.type = OperationType.WAIT_FOR_KEY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x2 and self.n == 0x9:
                self.type = OperationType.LOAD_FONT
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x3 and self.n == 0x3:
                self.type = OperationType.BCD_CONVERSION
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x5 and self.n == 0x5:
                self.type = OperationType.DUMP_REGISTERS_TO_MEMORY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))
            elif self.y == 0x6 and self.n == 0x5:
                self.type = OperationType.LOAD_REGISTER_FROM_MEMORY
                self.operands.append(Operand(OperandType.REGISTER, self.x, 1))


    @property
    def hex(self) -> str:
        return f'{to_hex(self.k, 1)}{to_hex(self.x, 1)}{to_hex(self.y, 1)}{to_hex(self.n, 1)}'


    @property
    def asm(self) -> str:
        operands: List[str] = []

        for operand in self.operands:
            if operand.type == OperandType.LITERAL:
                operands.append(f'#{operand.hex.upper()}')
            elif operand.type == OperandType.REGISTER:
                operands.append(f'V{operand.hex.upper()}')
            elif operand.type == OperandType.INDEX:
                operands.append(f'I')
            else:
                raise ValueError()

        mnemonic: str = '???'

        if self.type == OperationType.MACHINE_CODE:
            mnemonic = 'SYS'
        elif self.type == OperationType.CLEAR_SCREEN:
            mnemonic = 'CLS'
        elif self.type == OperationType.RETURN_FROM_SUBROUTINE:
            mnemonic = 'RET'
        elif self.type == OperationType.ABSOLUTE_JUMP:
            mnemonic = 'JP'
        elif self.type == OperationType.CALL_SUBROUTINE:
            mnemonic = 'CALL'
        elif self.type == OperationType.SKIP_IF_EQUALS:
            mnemonic = 'SE'
        elif self.type == OperationType.SKIP_IF_NOT_EQUALS:
            mnemonic = 'SNE'
        elif self.type == OperationType.COPY:
            mnemonic = 'LD'
        elif self.type == OperationType.ADD_WITHOUT_CARRY:
            mnemonic = 'ADD'
        elif self.type == OperationType.BITWISE_OR:
            mnemonic = 'OR'
        elif self.type == OperationType.BITWISE_AND:
            mnemonic = 'AND'
        elif self.type == OperationType.BITWISE_XOR:
            mnemonic = 'XOR'
        elif self.type == OperationType.ADD_WITH_CARRY:
            mnemonic = 'ADD'
        elif self.type == OperationType.SUBTRACTION_DIRECT:
            mnemonic = 'SUB'
        elif self.type == OperationType.SHIFT_RIGHT:
            mnemonic = 'SHR'
        elif self.type == OperationType.SHIFT_LEFT:
            mnemonic = 'SHL'
        elif self.type == OperationType.SUBTRACTION_REVERSE:
            mnemonic = 'SUBN'
        elif self.type == OperationType.ABSOLUTE_JUMP_WITH_OFFSET:
            mnemonic = 'JP'
            operands.insert(0, 'V0')
        elif self.type == OperationType.RANDOM_NUMBER:
            mnemonic = 'RND'
        elif self.type == OperationType.DRAW:
            mnemonic = 'DRW'
        elif self.type == OperationType.SKIP_IF_KEY_PRESSED:
            mnemonic = 'SKP'
        elif self.type == OperationType.SKIP_IF_KEY_NOT_PRESSED:
            mnemonic = 'SKNP'
        elif self.type == OperationType.GET_DELAY_TIMER:
            mnemonic = 'LD'
            operands.append('DT')
        elif self.type == OperationType.WAIT_FOR_KEY:
            mnemonic = 'LD'
            operands.append('K')
        elif self.type == OperationType.SET_DELAY_TIMER:
            mnemonic = 'LD'
            operands.insert(0, 'DT')
        elif self.type == OperationType.SET_SOUND_TIMER:
            mnemonic = 'LD'
            operands.insert(0, 'ST')
        elif self.type == OperationType.LOAD_FONT:
            mnemonic = 'LD'
            operands.insert(0, 'F')
        elif self.type == OperationType.BCD_CONVERSION:
            mnemonic = 'LD'
            operands.insert(0, 'B')
        elif self.type == OperationType.DUMP_REGISTERS_TO_MEMORY:
            mnemonic = 'LD'
            operands.insert(0, '[I]')
        elif self.type == OperationType.LOAD_REGISTER_FROM_MEMORY:
            mnemonic = 'LD'
            operands.append('[I]')

        return " ".join([mnemonic, ", ".join(operands)])


    def __str__(self) -> str:
        return f'Instruction(0x{self.hex}, "{self.asm}")'


class OperationType(Enum):
    UNKNOWN = 0
    ABSOLUTE_JUMP = 1 # SYS addr
    ABSOLUTE_JUMP_WITH_OFFSET = 2 # CLS
    ADD_WITH_CARRY = 3 # CLS
    ADD_WITHOUT_CARRY = 4 # JP addr
    BCD_CONVERSION = 5 # CALL addr
    BITWISE_AND = 6 # SE Vx, byte - SE Vx, Vy
    BITWISE_OR = 7 # SNE Vx, byte - SE Vx, Vy
    BITWISE_XOR = 8 # LD Vx, byte - LD Vx, Vy - LD I, addr
    CALL_SUBROUTINE = 9  # ADD Vx, byte - ADD I, Vx
    CLEAR_SCREEN = 10 # OR Vx, Vy
    COPY = 11 # AND Vx, Vy
    DRAW = 12 # XOR Vx, Vy
    DUMP_REGISTERS_TO_MEMORY = 13 # ADD Vx, Vy
    GET_DELAY_TIMER = 14 # SUB Vx, Vy
    LOAD_FONT = 15 # SHR Vx
    LOAD_REGISTER_FROM_MEMORY = 16 # SHL Vx
    MACHINE_CODE = 17 # SUBN Vx, Vy
    RANDOM_NUMBER = 18 # JP V0, addr
    RETURN_FROM_SUBROUTINE = 19 # RND Vx, byte
    SET_DELAY_TIMER = 20 # DRW Vx, Vy, nibble
    SET_SOUND_TIMER = 21 # SKP Vx
    SHIFT_LEFT = 22 # SKNP Vs
    SHIFT_RIGHT = 23 # LD Vx, DT
    SKIP_IF_EQUALS = 24 # LD Vx, K
    SKIP_IF_KEY_NOT_PRESSED = 25 # LD DT, Vx
    SKIP_IF_KEY_PRESSED = 26 # LD ST, Vx
    SKIP_IF_NOT_EQUALS = 27 # LD F, Vx
    SUBTRACTION_DIRECT = 28 # LD B, Vx
    SUBTRACTION_REVERSE = 29 # LD [I], Vx
    WAIT_FOR_KEY = 30 # LD Vx, [I]


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
