from machine import Pin, PWM
import LCD
import time

# === CONFIG ===
TILE_SIZE = 16        # pixels per tile
SCALE = 1             # 2x2 block per tile pixel
PIXEL_SIZE = SCALE    # convenience alias
DISPLAY_WIDTH = 240
DISPLAY_HEIGHT = 320

# === DISPLAY SETUP ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)
lcd = LCD.LCD_1inch3()

# === UTILS ===
def generate_tile_list(filename, img_width, img_height):
    """Loads all tiles from the spritesheet into a list."""
    tiles = []
    tiles_x = img_width // 16
    tiles_y = img_height // 16
    for ty in range(tiles_y):
        for tx in range(tiles_x):
            tile = load_tile_from_binary(filename, tx, ty, img_width, img_height)
            tiles.append(tile)
    return tiles
    
def draw_tilemap(tilemap, tiles, x_offset=0, y_offset=0):
    for row in range(len(tilemap)):
        for col in range(len(tilemap[0])):
            tile_id = tilemap[row][col]
            tile = tiles[tile_id]
            draw_tile_scaled(x_offset + col * 16, y_offset + row * 16, tile)

def load_tilemap(filename, width, height):
    with open(filename, "rb") as f:
        raw = f.read(width * height)
        return [list(raw[i * width:(i + 1) * width]) for i in range(height)]

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
    lcd.fill(0x0000)  # beige background
    lcd.show()

    #tile = load_tile_from_binary("tiles1.bin", tile_x=0, tile_y=0, img_width=160, img_height=113)
    tilemap = load_tilemap("map3.bin", 17, 15)
    tiles = generate_tile_list("tiles2.bin", 160, 113)
    draw_tilemap(tilemap, tiles)
    lcd.show()

    while True:
        #draw_tile_scaled(0, 0, tile)
        #lcd.show()
        time.sleep(10)
