from machine import PWM, Pin
import LCD
import time

import tilemap_renderer
import hud_renderer
import input_controller
import player

# === LCD SETUP ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)
lcd = LCD.LCD_1inch3()

# === CONSTANTS ===
MAP_FILE = "map4.bin"
TILESET_FILE = "tiles2.bin"
HUD_FILE = "hud0.bin"
MAP_WIDTH = 9
MAP_HEIGHT = 8
TILESET_WIDTH = 160
TILESET_HEIGHT = 113

FRAME_DURATION = 33  # ~30 FPS

# === LOAD MAP AND RENDER STATIC BACKGROUND ===
tilemap, tile_manager = tilemap_renderer.render_tilemap(
    lcd=lcd,
    map_file=MAP_FILE,
    tileset_file=TILESET_FILE,
    map_width=MAP_WIDTH,
    map_height=MAP_HEIGHT,
    tileset_width=TILESET_WIDTH,
    tileset_height=TILESET_HEIGHT
)

hud_renderer.draw_static_hud(lcd, HUD_FILE)

# === SETUP PLAYER ===
link = player.Player(x=4 * 32, y=3 * 32)

# === GAME LOOP ===
last_frame = time.ticks_ms()

while True:
    now = time.ticks_ms()
    if time.ticks_diff(now, last_frame) < FRAME_DURATION:
        continue
    last_frame = now

    # Poll joystick
    direction = input_controller.read_direction()

    # Update logic
    link.update(direction)

    # Clear the previous sprite position (redraw tiles underneath)
    link.clear_prev(lcd, tilemap, tile_manager)

    # Draw the player
    link.draw(lcd)

    # Push changes to screen
    lcd.show()
