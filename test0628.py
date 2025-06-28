from machine import Pin, PWM
import LCD
import time

# === CONFIG ===
TILE_SIZE = 16        # pixels per tile
SCALE = 2             # 2x2 block per tile pixel
PIXEL_SIZE = SCALE    # convenience alias
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

# === DISPLAY SETUP ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)
lcd = LCD.LCD_1inch3()

# === UTILS ===
def draw_tile_scaled(x0, y0, tile_data):
    """Draw a 16x16 tile scaled to 32x32 on the screen."""
    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            c = tile_data[y * TILE_SIZE + x]
            lcd.fill_rect(x0 + x * PIXEL_SIZE, y0 + y * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE, c)

def load_tile_from_binary(filename, tile_x, tile_y, img_width, img_height):
    """Load a 16x16 tile at (tile_x, tile_y) from a binary RGB565 tilesheet."""
    tile = []
    with open(filename, "rb") as f:
        for row in range(TILE_SIZE):
            y = tile_y * TILE_SIZE + row
            if y >= img_height:
                break
            offset = (y * img_width + tile_x * TILE_SIZE) * 2
            f.seek(offset)
            row_data = f.read(TILE_SIZE * 2)
            for i in range(0, len(row_data), 2):
                pixel = (row_data[i] << 8) | row_data[i + 1]  # Big-endian RGB565
                tile.append(pixel)
    return tile

# Optional: batch-load raw binary into a flat pixel list
def load_tile_grid_binary(filename):
    with open(filename, "rb") as f:
        raw = f.read()
        return [(raw[i] << 8) | raw[i + 1] for i in range(0, len(raw), 2)]

# === MAIN LOOP ===
if __name__ == "__main__":
    lcd.fill(0xf1ff)  # beige background
    lcd.show()

    tile = load_tile_from_binary("tiles0.bin", tile_x=2, tile_y=2, img_width=48, img_height=48)

    while True:
        draw_tile_scaled(0, 0, tile)
        lcd.show()
        time.sleep(10)
