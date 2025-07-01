# main.py

from machine import Pin, PWM
import LCD
import tilemap_renderer
import hud_renderer
import time

# === SETUP LCD ===
bl = PWM(Pin(13))
bl.freq(1000)
bl.duty_u16(32768)
lcd = LCD.LCD_1inch3()

hud_renderer.draw_static_hud(lcd, "hud0.bin")
lcd.show()

# === RENDER SCREEN ===
tilemap_renderer.render_tilemap(
    lcd=lcd,
    map_file="map4.bin",
    tileset_file="tiles2.bin",
    map_width=9,
    map_height=8,
    tileset_width=160,
    tileset_height=113
)

# === MAIN LOOP ===
while True:
    time.sleep(1)
