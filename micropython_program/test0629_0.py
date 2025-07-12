# Import necessary modules
from machine import Pin, PWM           # Hardware pin and PWM control
import LCD                             # LCD driver module (assumed to be custom)
import framebuf                        # MicroPython graphics buffer
import time                            # Timing utilities
import array                           # Efficient array handling
import gc                              # Garbage collector control

# === CONFIGURATION CONSTANTS ===
TILE_SIZE = 16                         # Each tile is 16x16 pixels
MAP_WIDTH = 17                         # Number of tiles horizontally
MAP_HEIGHT = 15                        # Number of tiles vertically
IMG_WIDTH = 160                        # Width of tileset image in pixels
IMG_HEIGHT = 113                       # Height of tileset image
MAP_FILE = "map3.bin"                  # Tilemap file: stores tile ID layout
TILESET_FILE = "tiles2.bin"           # Tileset file: raw RGB565 binary image
CACHE_LIMIT = 20                       # Max number of tiles cached in RAM

# === INITIALIZE LCD SCREEN ===
bl = PWM(Pin(13))                      # Backlight pin for LCD
bl.freq(1000)                          # Set backlight PWM frequency
bl.duty_u16(32768)                     # Set brightness (range: 0–65535)
lcd = LCD.LCD_1inch3()                 # Instantiate the LCD driver

# === TILE CACHING & MANAGEMENT CLASS ===
class TileManager:
    """
    Loads tile data from a tileset file, converts it to a framebuffer,
    and caches it for reuse using a least-recently-used (LRU) strategy.
    """
    def __init__(self, tileset_file, img_w, img_h, tile_size, cache_limit):
        self.tileset = tileset_file
        self.img_w = img_w
        self.img_h = img_h
        self.tile_size = tile_size
        self.cache = {}               # Maps tile_id → framebuffer
        self.cache_usage = {}         # Maps tile_id → last used timestamp
        self.limit = cache_limit
        self.tiles_per_row = img_w // tile_size

    def _load_tile_data(self, tx, ty):
        """
        Loads tile pixel data from the tileset using tile coordinates (tx, ty).
        Returns an array of RGB565 16-bit integers.
        """
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
        """
        Converts tile pixel data into a FrameBuffer for use with blit().
        """
        buf = array.array('H', tile_data)
        return framebuf.FrameBuffer(buf, self.tile_size, self.tile_size, framebuf.RGB565)

    def _evict_if_needed(self):
        """
        Removes the least-recently-used tile from cache if it exceeds the limit.
        """
        if len(self.cache) >= self.limit:
            oldest = min(self.cache_usage, key=self.cache_usage.get)
            del self.cache[oldest]
            del self.cache_usage[oldest]

    def get_tile_fb(self, tile_id):
        """
        Returns the FrameBuffer associated with a given tile ID.
        Loads it from the tileset and caches it if not already cached.
        """
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

# === LOAD TILEMAP LAYOUT ===
def load_tilemap(filename, width, height):
    """
    Reads a binary tilemap file and returns a 2D list of tile IDs.
    Each tile ID is 1 byte (uint8).
    """
    with open(filename, "rb") as f:
        data = f.read(width * height)
        return [array.array('B', data[i * width : (i + 1) * width]) for i in range(height)]

# === DRAW TILEMAP TO SCREEN ===
def draw_tilemap(tilemap, tile_manager):
    """
    Uses the TileManager to fetch and blit tiles based on the tilemap layout.
    """
    for row_idx, row in enumerate(tilemap):
        for col_idx, tile_id in enumerate(row):
            tile_fb = tile_manager.get_tile_fb(tile_id)
            lcd.blit(tile_fb, col_idx * TILE_SIZE, row_idx * TILE_SIZE)
        gc.collect()  # Free memory between rows to avoid fragmentation

# === OPTIONAL: BENCHMARK TILE BLITTING SPEED ===
def benchmark_draw(tile_manager):
    """
    Measures time to blit one tile and prints memory stats.
    """
    tile_fb = tile_manager.get_tile_fb(0)
    start = time.ticks_us()
    lcd.blit(tile_fb, 0, 0)
    lcd.show()
    elapsed = time.ticks_diff(time.ticks_us(), start)
    print("Blit time (µs):", elapsed)
    print("Free memory:", gc.mem_free())

# === MAIN PROGRAM LOOP ===
if __name__ == "__main__":
    lcd.fill(0x0000)                          # Clear screen to black
    lcd.show()

    tilemap = load_tilemap(MAP_FILE, MAP_WIDTH, MAP_HEIGHT)  # Load layout
    manager = TileManager(TILESET_FILE, IMG_WIDTH, IMG_HEIGHT, TILE_SIZE, CACHE_LIMIT)

    draw_tilemap(tilemap, manager)            # Draw the full scene
    lcd.show()                                # Push final frame to LCD

    # Uncomment to measure tile blitting performance
    # benchmark_draw(manager)

    while True:
        time.sleep(1)  # Keep program alive (idle loop)

