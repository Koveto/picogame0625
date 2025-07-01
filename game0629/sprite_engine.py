# sprite_engine.py

def draw_sprite(lcd, filename, x, y, tile_x, tile_y, transparent=0xce01, sheet_width=128, sheet_height=16):
    """
    Streams and draws a single 16x16 sprite from a binary sprite sheet.

    Args:
        lcd         – The LCD object (must support fill_rect).
        filename    – Path to sprite sheet (RGB565 format).
        x, y        – Screen coordinates to draw the sprite (top-left).
        tile_x/y    – Sprite index in the sheet (in tiles, not pixels).
        transparent – Color value treated as transparent (default: 462).
        sheet_width – Width of sprite sheet in pixels.
        sheet_height– Height of sprite sheet in pixels.
    """
    SPRITE_SIZE = 16
    SCALE = 2
    start_x = tile_x * SPRITE_SIZE
    start_y = tile_y * SPRITE_SIZE

    with open(filename, "rb") as f:
        for dy in range(SPRITE_SIZE):
            sy = start_y + dy
            if sy >= sheet_height:
                break
            offset = (sy * sheet_width + start_x) * 2
            f.seek(offset)
            row = f.read(SPRITE_SIZE * 2)

            for dx in range(SPRITE_SIZE):
                i = dx * 2
                color = (row[i] << 8) | row[i + 1]
                if color != transparent:
                    lcd.fill_rect(
                        x + dx * SCALE,
                        y + dy * SCALE,
                        SCALE,
                        SCALE,
                        color
                    )
