# player.py

import time
import sprite_engine
import tilemap_renderer

class Player:
    def __init__(self, x, y, sprite_file="link1.bin"):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.speed = 10
        self.direction = "down"
        self.sprite_file = sprite_file
        self.frame = 0
        self.last_step_time = time.ticks_ms()
        self.frame_delay = 160
        self.width = 32
        self.height = 32

    def update(self, direction):
        now = time.ticks_ms()

        if direction and direction != self.direction:
            self.direction = direction
            self.frame = 0
            self.last_step_time = now

        self.prev_x = self.x
        self.prev_y = self.y

        if direction:
            if direction == "up":
                self.y = max(self.y - self.speed, 0)
            elif direction == "down":
                self.y = min(self.y + self.speed, 239 - self.height)
            elif direction == "left":
                self.x = max(self.x - self.speed, 0)
            elif direction == "right":
                self.x = min(self.x + self.speed, 287 - self.width)

            if time.ticks_diff(now, self.last_step_time) >= self.frame_delay:
                self.frame = (self.frame + 1) % 2
                self.last_step_time = now
        else:
            self.frame = 0

    def clear_prev(self, lcd, tilemap, tile_manager):
        tile_x = self.prev_x // 32
        tile_y = self.prev_y // 32

        for dy in range(2):
            for dx in range(2):
                gx = tile_x + dx
                gy = tile_y + dy
                if 0 <= gx < 9 and 0 <= gy < 8:
                    tile_id = tilemap[gy][gx]
                    tilemap_renderer.draw_tile(lcd, tile_id, gx, gy, tile_manager)

    def draw(self, lcd):
        sprite_indices = {
            "down":  (0, 1),
            "up":    (2, 3),
            "left":  (4, 5),
            "right": (6, 7)
        }
        tile_index = sprite_indices[self.direction][self.frame]
        tile_x = tile_index % 10
        tile_y = tile_index // 10

        sprite_engine.draw_sprite(
            lcd,
            filename=self.sprite_file,
            x=self.x,
            y=self.y,
            tile_x=tile_x,
            tile_y=tile_y
        )
