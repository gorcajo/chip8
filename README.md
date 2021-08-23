# CHIP-8 Interpreter

## 1. Description

This is my own CHIP-8 interpreter. Written in Python with Pygame.

![](demo.gif)

## 2. Install

You'll need pipenv:

```bash
pipenv install --ignore-pipfile
```

## 3. Test ROMs

### 3.1. IBM logo test

```bash
./run.sh test-roms/1-ibm-logo.ch8
```

It should draw the IBM logo in a few instructions and then freeze in an endless jump. Only needs 6 instructions to work, so this is the first test I executed when I was developing the interpreter.


### 3.2. BC test

```bash
./run.sh test-roms/2-bc-test.ch8
```

If there is a failing test an error code will be drawn in the display:

- `E 01`: `3XNN`, verify that the jump condition is fair.
- `E 02`: `5XY0`, verify that the jump condition is fair.
- `E 03`: `4XNN`, verify that the jump condition is fair.
- `E 04`: `7XNN`, check the result of the addition.
- `E 05`: `8XY5`, verify that `VF` is set to `0` when there is a borrow.
- `E 06`: `8XY5`, verify that `VF` is set to `1` when there is no borrow.
- `E 07`: `8XY7`, verify that `VF` is set to `0` when there is a borrow.
- `E 08`: `8XY7`, verify that `VF` is set to `1` when there is no borrow.
- `E 09`: `8XY1`, check the result of the `OR` operation.
- `E 10`: `8XY2`, check the result of `AND` operation.
- `E 11`: `8XY3`, check the result of the `XOR` operation.
- `E 12`: `8XYE`, verify that `VF` is set to the `MSB` before the shift and `VF` does not take value `0` every time.
- `E 13`: `8XYE`, verify that `VF` is set to the `MSB` before the shift and `VF` does not take value `1` every time.
- `E 14`: `8XY6`, verify that `VF` is set to the `LSB` before the shift and `VF` does not take value `0` every time.
- `E 15`: `8XY6`, verify that `VF` is set to the `LSB` before the shift and `VF` does not take value `1` every time.
- `E 16`: `FX55` and `FX65`, verify that these two opcodes are implemented. The error may come from one or the other or both are defects.
- `E 17`: `FX33`, calculating the binary representation is mistaken or the result is poorly stored into memory or poorly poped (`FX65` or `FX1E`).

More info at <https://github.com/daniel5151/AC8E/blob/master/roms/bc_test.txt>.

### 3.3. Opcode test

```bash
./run.sh test-roms/3-test-opcode.ch8
```

It should pass every test with "OK".

More info at <https://github.com/corax89/chip8-test-rom>.

## 4. Run a game

```bash
./run.sh games/pong.ch8
```

## 5. Instruction set

I made an alternative to the assembly language shown in the Cowgod's reference. It's based on CHIP-8's instruction set, I used it just for debugging with the memory viewer.

An assembly instruction is composed by a mnemonic and by zero to three operands. An operand can be:

- `I`: Index register.
- `VX`: Register at the position `X` in the opcode.
- `VY`: Register at the position `Y` in the opcode.
- `#N`: Hexadecimal literal `N`.
- `#NN`: Hexadecimal literal `NN`.
- `#NNN`: Hexadecimal literal `NNN`.

There is no labels, named constants, expresions or anything else. In fact, there is no assembler at all (I only made a simple disassembler for the memory viewer).

### 5.1. Display

| Opcode | Assembly        | Description                                                           |
| :----: | :-------------- | :-------------------------------------------------------------------- |
| `00E0` | `CLR`           | Clears screen                                                         |
| `DXYN` | `DRAW VX VY #N` | Draws the sprite pointed by `I` at (`X`, `Y`) with `N` bits of height |

### 5.2. Unconditional jumps

| Opcode | Assembly     | Description         |
| :----: | :----------- | :------------------ |
| `1NNN` | `JMP #NNN`   | Jumps to `NNN`      |
| `BNNN` | `JMPV0 #NNN` | Jumps to `NNN + V0` |

### 5.3. Subroutines

| Opcode | Assembly    | Description               |
| :----: | :---------- | :------------------------ |
| `2NNN` | `CALL #NNN` | Calls subroutine at `NNN` |
| `00EE` | `RET`       | Returns from subroutine   |

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

## 6. Info

- CHIP-8 references:
  - Wikipedia: <https://en.wikipedia.org/wiki/CHIP-8>
  - Cowgod's tech reference: <http://devernay.free.fr/hacks/chip8/C8TECH10.HTM>
- ROMs:
  - CHIP-8 Archive: <https://johnearnest.github.io/chip8Archive/?sort=platform>
  - CHIP-8 Website (Web Archive): <https://web.archive.org/web/20130903155600/http://chip8.com/?page=109>
- Guide on CHIP-8 development: <https://tobiasvl.github.io/blog/write-a-chip-8-emulator/>

## 7. To Do List

- Improve keyboard controls.
- Try to reduce display flickering.
- Highlight pressed keys.
- Highlight recently changed register, timer, memory address, etc.
- Graphical buttons for play/pause, step and reset.
- Load ROM from UI.
- Prettier UI.
