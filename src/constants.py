# UI:

SCREEN_WIDTH = 1240
SCREEN_HEIGHT = 550
SCREEN_GEOMETRY = (SCREEN_WIDTH, SCREEN_HEIGHT)

# Palette from https://www.colorion.co/palette/87411:
PALETTE_BLACK = (0x01, 0x01, 0x01)
PALETTE_LIGHTGRAY = (0xD8, 0xD8, 0xD8)
PALETTE_SPRINGGREEN = (0x56, 0xF5, 0x69)
PALETTE_DIMGRAY = (0x60, 0x60, 0x60)
PALETTE_DARKGRAY = (0xA3, 0xA9, 0xA4)

BACKGROUND_COLOR = PALETTE_BLACK
PRIMARY_COLOR = PALETTE_LIGHTGRAY
HIGHLIGHT_COLOR = PALETTE_SPRINGGREEN
SECONDARY_COLOR = PALETTE_DARKGRAY

FONT_FAMILY = 'monospace'
FONT_SIZE = 16
FONT_WIDTH = 10

MARGIN = 10

# CHIP-8:

CHIP8_STEPS_PER_SECOND = 720

# GameScreen:

PIXEL_SIZE = 10
PIXEL_ON_COLOR = PALETTE_SPRINGGREEN
PIXEL_OFF_COLOR = PALETTE_DIMGRAY
