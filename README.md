# CHIP-8 Interpreter

## 1. Description

This is my own CHIP-8 interpreter. Written in Python with Pygame.

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

2. BC test:

```bash
./run.sh test-roms/2-bc-test.ch8
```

3. Opcode test:

```bash
./run.sh test-roms/3-test-opcode.ch8
```

## 4. Run a game

```bash
./run.sh relative/path/to/your/game.ch8
```

## 5. Assembly

I made my own assembly language based on CHIP-8's instruction set. I used it just for debugging:

### 5.1. Display

| Opcode | Assembly       | Description                                                           |
| :----: | :------------- | :-------------------------------------------------------------------- |
| `00E0` | `CLR`          | Clears screen                                                         |
| `DXYN` | `DRAW VX VY N` | Draws the sprite pointed by `I` at (`X`, `Y`) with `N` bits of height |

### 5.2. Unconditional jumps

| Opcode | Assembly    | Description               |
| :----: | :---------- | :------------------------ |
| `00EE` | `RET`       | Returns from subroutine   |
| `1NNN` | `JMP NNN`   | Jumps to `NNN`            |
| `2NNN` | `CALL NNN`  | Calls subroutine at `NNN` |
| `BNNN` | `JMPV0 NNN` | Jumps to `NNN + V0`       |

### 5.3. Conditional jumps

| Opcode | Assembly     | Description                          |
| :----: | :----------- | :----------------------------------- |
| `3XNN` | `JEQ X NN`   | Skips next instruction if `VX == NN` |
| `4XNN` | `JNEQ X NN`  | Skips next instruction if `VX != NN` |
| `5XY0` | `JEQ X Y`    | Skips next instruction if `VX == VY` |
| `9XY0` | `JNEQ VX VY` | Skips next instruction if `VX != VY` |

### 5.4. Assignments

| Opcode | Assembly    | Description |
| :----: | :---------- | :---------- |
| `6XNN` | `MOV VX NN` | `VX = NN`   |
| `8XY0` | `MOV X Y`   | `VX = VY`   |
| `ANNN` | `MOV I NNN` | `I = NNN`   |

### 5.5. Arithemetics

| Opcode | Assembly     | Description               |
| :----: | :----------- | :------------------------ |
| `7XNN` | `ADDNC X NN` | `VX = VX + NN`, no carry  |
| `8XY1` | `OR X Y`     | `VX = VX or VY`, bitwise  |
| `8XY2` | `AND X Y`    | `VX = VX and VY`, bitwise |
| `8XY3` | `XOR X Y`    | `VX = VX xor VY`, bitwise |
| `8XY4` | `ADD VX VY`  | `VX = VX + VY`            |
| `8XY5` | `SUB VX VY`  | `VX = VX - VY`            |
| `8XY6` | `RSH VX`     | `VX = VX >> 1`            |
| `8XY7` | `SUBR VX VY` | `Vx = VY - VX`            |
| `8XYE` | `LSH VX`     | `VX = VX << 1`            |
| `CXNN` | `RND VX NN`  | `VX = rand() & NN`        |
| `FX1E` | `ADDNC I VX` | `I = VX`, no carry        |

### 5.6. Input

| Opcode | Assembly   | Description                                                     |
| :----: | :--------- | :-------------------------------------------------------------- |
| `FX0A` | `WKEY VX`  | Waits until key press, then sets `VX` to the value of the key   |
| `EX9E` | `JKEY VX`  | Skips next instruction if the key stored in `VX` is pressed     |
| `EXA1` | `JNKEY VX` | Skips next instruction if the key stored in `VX` is not pressed |

### 5.7. Timers

| Opcode | Assembly  | Description                               |
| :----: | :-------- | :---------------------------------------- |
| `FX07` | `GDLY VX` | Sets `VX` to the value of the delay timer |
| `FX15` | `SDLY VX` | Sets the value of the delay timer to `VX` |
| `FX18` | `SSND VX` | Sets the value of the sound timer to `VY` |

### 5.8. Misc

| Opcode | Assembly  | Description                                                           |
| :----: | :-------- | :-------------------------------------------------------------------- |
| `0NNN` | `MCH NNN` | Executes machine code `NNN`                                           |
| `FX29` | `FONT VX` | Sets `I` to the location of the sprite for the character in `VX`      |
| `FX33` | `BCD VX`  | Stores `VX` as BCD at `I*`, `(I+1)*` and `(I+2)*`                     |
| `FX55` | `DUMP VX` | Dumps `V0` to `VX` (inclusive) to memory addresses starting at `I*`   |
| `FX65` | `LOAD VX` | Loads `V0` to `VX` (inclusive) from memory addresses starting at `I*` |

## 6. Extras

- Info on CHIP-8: <https://en.wikipedia.org/wiki/CHIP-8>
- ROMs: <https://johnearnest.github.io/chip8Archive/?sort=platform>
