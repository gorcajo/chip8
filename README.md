# CHIP-8 Interpreter

## 1. Description

This is my own CHIP-8 interpreter. Written in Python with Pygame.

![Demo](https://github.com/gorcajo/chip8/demo.gif)

## 2. Install

You'll need pipenv:

```bash
pipenv install --ignore-pipfile
```

## 3. Run test roms

1. IBM logo test:

```bash
./run.sh test-roms/1-ibm-logo.ch8
```

2. BC test (see <https://github.com/daniel5151/AC8E/blob/master/roms/bc_test.txt>):

```bash
./run.sh test-roms/2-bc-test.ch8
```

3. Opcode test (see <https://github.com/corax89/chip8-test-rom>):

```bash
./run.sh test-roms/3-test-opcode.ch8
```

## 4. Run a game

```bash
./run.sh relative/path/to/your/game.ch8
```

## 5. Instruction set

I made a simple assembly language based on CHIP-8's instruction set, just for debugging, classifying opcodes and organize my work. Although there is already another simple assembly language in the Cowgod's reference, in my humble opinion I think it's harder.

An assembly instruction is composed by a mnemonic and by zero to three operands. An operand can be:

- `I`: Index register.
- `VX`: Register at the position `X` in the opcode.
- `VY`: Register at the position `Y` in the opcode.
- `#N`: Hexadecimal literal `N`.
- `#NN`: Hexadecimal literal `NN`.
- `#NNN`: Hexadecimal literal `NNN`.

There is no labels, named constants, expresions or anything else (maybe in the future?). In fact, there is no assembler (only disassembler for the debugger).

### 5.1. Display

| Opcode | Assembly        | Description                                                           |
| :----: | :-------------- | :-------------------------------------------------------------------- |
| `00E0` | `CLR`           | Clears screen                                                         |
| `DXYN` | `DRAW VX VY #N` | Draws the sprite pointed by `I` at (`X`, `Y`) with `N` bits of height |

### 5.2. Unconditional jumps

| Opcode | Assembly     | Description               |
| :----: | :----------- | :------------------------ |
| `1NNN` | `JMP #NNN`   | Jumps to `NNN`            |
| `BNNN` | `JMPV0 #NNN` | Jumps to `NNN + V0`       |

### 5.3. Subroutines

| Opcode | Assembly     | Description               |
| :----: | :----------- | :------------------------ |
| `2NNN` | `CALL #NNN`  | Calls subroutine at `NNN` |
| `00EE` | `RET`        | Returns from subroutine   |

### 5.4. Conditional jumps

| Opcode | Assembly      | Description                          |
| :----: | :------------ | :----------------------------------- |
| `3XNN` | `JEQ VX #NN`  | Skips next instruction if `VX == NN` |
| `4XNN` | `JNEQ VX #NN` | Skips next instruction if `VX != NN` |
| `5XY0` | `JEQ VX VY`   | Skips next instruction if `VX == VY` |
| `9XY0` | `JNEQ VX VY`  | Skips next instruction if `VX != VY` |

### 5.5. Assignments

| Opcode | Assembly     | Description |
| :----: | :----------- | :---------- |
| `6XNN` | `MOV VX #NN` | `VX = NN`   |
| `8XY0` | `MOV VX VY`  | `VX = VY`   |
| `ANNN` | `MOV I #NNN` | `I = NNN`   |

### 5.6. Arithemetics

| Opcode | Assembly       | Description               |
| :----: | :------------- | :------------------------ |
| `7XNN` | `ADDNC VX #NN` | `VX = VX + NN`, no carry  |
| `8XY1` | `OR VX VY`     | `VX = VX or VY`, bitwise  |
| `8XY2` | `AND VX VY`    | `VX = VX and VY`, bitwise |
| `8XY3` | `XOR VX VY`    | `VX = VX xor VY`, bitwise |
| `8XY4` | `ADD VX VY`    | `VX = VX + VY`            |
| `8XY5` | `SUB VX VY`    | `VX = VX - VY`            |
| `8XY6` | `RSH VX`       | `VX = VX >> 1`            |
| `8XY7` | `SUBR VX VY`   | `Vx = VY - VX`            |
| `8XYE` | `LSH VX`       | `VX = VX << 1`            |
| `CXNN` | `RND VX #NN`   | `VX = rand() & NN`        |
| `FX1E` | `ADDNC I VX`   | `I = VX`, no carry        |

### 5.7. Input

| Opcode | Assembly   | Description                                                     |
| :----: | :--------- | :-------------------------------------------------------------- |
| `FX0A` | `WKEY VX`  | Waits until key press, then sets `VX` to the value of the key   |
| `EX9E` | `JKEY VX`  | Skips next instruction if the key stored in `VX` is pressed     |
| `EXA1` | `JNKEY VX` | Skips next instruction if the key stored in `VX` is not pressed |

### 5.8. Timers

| Opcode | Assembly  | Description                               |
| :----: | :-------- | :---------------------------------------- |
| `FX07` | `GDLY VX` | Sets `VX` to the value of the delay timer |
| `FX15` | `SDLY VX` | Sets the value of the delay timer to `VX` |
| `FX18` | `SSND VX` | Sets the value of the sound timer to `VY` |

### 5.9. Misc

| Opcode | Assembly   | Description                                                           |
| :----: | :--------- | :-------------------------------------------------------------------- |
| `0NNN` | `MCH #NNN` | Executes machine code `NNN`                                           |
| `FX29` | `FONT VX`  | Sets `I` to the location of the sprite for the character in `VX`      |
| `FX33` | `BCD VX`   | Stores `VX` as BCD at `I*`, `(I+1)*` and `(I+2)*`                     |
| `FX55` | `DUMP VX`  | Dumps `V0` to `VX` (inclusive) to memory addresses starting at `I*`   |
| `FX65` | `LOAD VX`  | Loads `V0` to `VX` (inclusive) from memory addresses starting at `I*` |

## 6. Extras

- Wikipedia: <https://en.wikipedia.org/wiki/CHIP-8>
- Cowgod's tech reference: <http://devernay.free.fr/hacks/chip8/C8TECH10.HTM>
- Guide on CHIP-8 development: <https://tobiasvl.github.io/blog/write-a-chip-8-emulator/>
- ROMs: <https://johnearnest.github.io/chip8Archive/?sort=platform>
- ROM pack: <https://web.archive.org/web/20130903155600/http://chip8.com/?page=109>

## 7. To Do List

### 7.1. UI

- Highlight recently changed register, memory address, etc.
- Buttons in UI, for play/pause, step and reset.
- Load ROM from UI.
- Prettier UI.
