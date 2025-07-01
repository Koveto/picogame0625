# tilemap_renderer.py

import framebuf
import array
import gc
import time

TILE_SIZE = 16
SCALE = 2
DISPLAY_TILE_SIZE = TILE_SIZE * SCALE
CACHE_LIMIT = 20

class TileManager:
    def __init__(self, tileset_file, img_w, img_h):
        self.tileset = tileset_file
        self.img_w = img_w
        self.img_h = img_h
        self.tiles_per_row = img_w // TILE_SIZE
        self.cache = {}
        self.cache_usage = {}

    def _load_tile_data(self, tx, ty):
        tile_data = array.array('H')
        with open(self.tileset, "rb") as f:
            for row in range(TILE_SIZE):
                y = ty * TILE_SIZE + row
                if y >= self.img_h:
                    break
                offset = (y * self.img_w + tx * TILE_SIZE) * 2
                f.seek(offset)
                row_bytes = f.read(TILE_SIZE * 2)
                for i in range(0, len(row_bytes), 2):
                    pixel = (row_bytes[i] << 8) | row_bytes[i + 1]
                    tile_data.append(pixel)
        return tile_data

    def _create_framebuffer(self, tile_data):
        buf = array.array('H', tile_data)
        return framebuf.FrameBuffer(buf, TILE_SIZE, TILE_SIZE, framebuf.RGB565)

    def _evict_if_needed(self):
        if len(self.cache) >= CACHE_LIMIT:
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

def _load_tilemap(filename, width, height):
    with open(filename, "rb") as f:
        data = f.read(width * height)
        return [array.array('B', data[i * width : (i + 1) * width]) for i in range(height)]

def _draw_scaled_tile(lcd, x, y, tile_fb):
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

def render_tilemap(lcd, map_file, tileset_file, map_width, map_height, tileset_width, tileset_height):
    """
    Public API to render a tilemap to the screen.
    lcd: an LCD object with FrameBuffer methods (pixel, fill_rect)
    map_file: path to binary tilemap file (9×8 layout)
    tileset_file: path to RGB565 tile image data
    map_width, map_height: dimensions in tiles (typically 9×8)
    tileset_width, tileset_height: dimensions in pixels (e.g. 160×113)
    """
    lcd.show()

    tilemap = _load_tilemap(map_file, map_width, map_height)
    tile_manager = TileManager(tileset_file, tileset_width, tileset_height)

    for row_idx, row in enumerate(tilemap):
        for col_idx, tile_id in enumerate(row):
            tile_fb = tile_manager.get_tile_fb(tile_id)
            _draw_scaled_tile(
                lcd,
                col_idx * DISPLAY_TILE_SIZE,
                row_idx * DISPLAY_TILE_SIZE,
                tile_fb
            )
        gc.collect()

    lcd.show()
