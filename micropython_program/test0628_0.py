from machine import Pin, PWM
import LCD
import time

# === CONFIGURATION ===
TILE_SIZE = 16
MAP_WIDTH = 17    # tiles
MAP_HEIGHT = 15   # tiles
IMG_WIDTH = 160   # pixels in tileset
IMG_HEIGHT = 113

MAP_FILE = "map3.bin"
TILESET_FILE = "tiles2.bin"

# === SETUP LCD ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)

lcd = LCD.LCD_1inch3()

# === DRAW TILE ===
def draw_tile(x, y, data):
    """Draws a 16x16 tile at screen position (x, y) from a flat RGB565 list."""
    for dy in range(TILE_SIZE):
        for dx in range(TILE_SIZE):
            color = data[dy * TILE_SIZE + dx]
            lcd.pixel(x + dx, y + dy, color)

# === LOAD SINGLE TILE FROM BINARY FILE ===
def load_tile(filename, tx, ty, img_w, img_h):
    """Reads one tile from the tileset at tile position (tx, ty)."""
    tile = []
    with open(filename, "rb") as f:
        for row in range(TILE_SIZE):
            y = ty * TILE_SIZE + row
            if y >= img_h:
                break
            offset = (y * img_w + tx * TILE_SIZE) * 2
            f.seek(offset)
            row_bytes = f.read(TILE_SIZE * 2)
            for i in range(0, len(row_bytes), 2):
                pixel = (row_bytes[i] << 8) | row_bytes[i + 1]
                tile.append(pixel)
    return tile

# === LOAD TILEMAP DATA ===
def load_tilemap(filename, width, height):
    """Loads tile IDs as a 2D grid from map file (1 byte per tile)."""
    with open(filename, "rb") as f:
        data = f.read(width * height)
        return [list(data[i * width : (i + 1) * width]) for i in range(height)]

# === STREAM AND DRAW TILEMAP ===
def draw_tilemap(tilemap, tileset_file, img_w, img_h):
    """Draws a tilemap using streamed access from tileset_file."""
    tiles_per_row = img_w // TILE_SIZE
    for row_idx, row in enumerate(tilemap):
        for col_idx, tile_id in enumerate(row):
            tx = tile_id % tiles_per_row
            ty = tile_id // tiles_per_row
            tile = load_tile(tileset_file, tx, ty, img_w, img_h)
            draw_tile(col_idx * TILE_SIZE, row_idx * TILE_SIZE, tile)

# === MAIN LOOP ===
if __name__ == "__main__":
    lcd.fill(0x0000)
    lcd.show()

    tilemap = load_tilemap(MAP_FILE, MAP_WIDTH, MAP_HEIGHT)
    draw_tilemap(tilemap, TILESET_FILE, IMG_WIDTH, IMG_HEIGHT)
    lcd.show()

    while True:
        time.sleep(1)
