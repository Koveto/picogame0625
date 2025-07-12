from machine import Pin, PWM
import LCD
import framebuf
import time
import array
import gc

# === CONFIGURATION ===
TILE_SIZE = 16                     # Internal tile size
SCALE = 2                          # Display scale factor (→ 32×32)
DISPLAY_TILE_SIZE = TILE_SIZE * SCALE
MAP_WIDTH = 9                      # Logical map size (tiles)
MAP_HEIGHT = 8
MAP_FILE = "map4.bin"             # New map file with 9x8 layout
TILESET_FILE = "tiles2.bin"
IMG_WIDTH = 160
IMG_HEIGHT = 113
CACHE_LIMIT = 20

# === SETUP LCD ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)
lcd = LCD.LCD_1inch3()

# === TILE MANAGER CLASS ===
class TileManager:
    def __init__(self, tileset_file, img_w, img_h, tile_size, cache_limit):
        self.tileset = tileset_file
        self.img_w = img_w
        self.img_h = img_h
        self.tile_size = tile_size
        self.cache = {}
        self.cache_usage = {}
        self.limit = cache_limit
        self.tiles_per_row = img_w // tile_size

    def _load_tile_data(self, tx, ty):
        tile_data = array.array('H')
        with open(self.tileset, "rb") as f:
            for row in range(self.tile_size):
                y = ty * self.tile_size + row
                if y >= self.img_h:
                    break
                offset = (y * self.img_w + tx * self.tile_size) * 2
                f.seek(offset)
                row_bytes = f.read(self.tile_size * 2)
                for i in range(0, len(row_bytes), 2):
                    pixel = (row_bytes[i] << 8) | row_bytes[i + 1]
                    tile_data.append(pixel)
        return tile_data

    def _create_framebuffer(self, tile_data):
        buf = array.array('H', tile_data)
        return framebuf.FrameBuffer(buf, self.tile_size, self.tile_size, framebuf.RGB565)

    def _evict_if_needed(self):
        if len(self.cache) >= self.limit:
            oldest = min(self.cache_usage, key=self.cache_usage.get)
            del self.cache[oldest]
            del self.cache_usage[oldest]

    def get_tile_fb(self, tile_id):
        self.cache_usage[tile_id] = time.ticks_ms()
        if tile_id in self.cache:
            return self.cache[tile_id]

        self._evict_if_needed()
        tx = tile_id % self.tiles_per_row
        ty = tile_id // self.tiles_per_row
        tile_data = self._load_tile_data(tx, ty)
        tile_fb = self._create_framebuffer(tile_data)
        self.cache[tile_id] = tile_fb
        return tile_fb

# === LOAD TILEMAP FROM FILE ===
def load_tilemap(filename, width, height):
    with open(filename, "rb") as f:
        data = f.read(width * height)
        return [array.array('B', data[i * width : (i + 1) * width]) for i in range(height)]

# === DRAW A SINGLE SCALED TILE TO THE SCREEN ===
def draw_scaled_tile(x, y, tile_fb):
    for dy in range(TILE_SIZE):
        for dx in range(TILE_SIZE):
            color = tile_fb.pixel(dx, dy)
            lcd.fill_rect(
                x + dx * SCALE,
                y + dy * SCALE,
                SCALE,
                SCALE,
                color
            )

# === DRAW THE FULL MAP ===
def draw_tilemap(tilemap, tile_manager):
    for row_idx, row in enumerate(tilemap):
        for col_idx, tile_id in enumerate(row):
            tile_fb = tile_manager.get_tile_fb(tile_id)
            draw_scaled_tile(
                col_idx * DISPLAY_TILE_SIZE,
                row_idx * DISPLAY_TILE_SIZE,
                tile_fb
            )
        gc.collect()

# === MAIN LOOP ===
if __name__ == "__main__":
    lcd.fill(0x0000)
    lcd.show()

    tilemap = load_tilemap(MAP_FILE, MAP_WIDTH, MAP_HEIGHT)
    manager = TileManager(TILESET_FILE, IMG_WIDTH, IMG_HEIGHT, TILE_SIZE, CACHE_LIMIT)

    draw_tilemap(tilemap, manager)
    lcd.show()

    while True:
        time.sleep(1)
