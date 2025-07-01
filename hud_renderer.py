# hud_renderer.py

def draw_static_hud(lcd, hud_file):
    """
    Streams and scales a 16x120 RGB565 HUD image from disk directly to the
    rightmost 32x240 display area without loading the entire image into RAM.
    """
    img_w = 16
    img_h = 120
    scale = 2
    x_offset = 288  # Rightmost tile column (9 tiles * 32px)

    with open(hud_file, "rb") as f:
        for y in range(img_h):
            row = f.read(img_w * 2)
            for x in range(img_w):
                i = x * 2
                color = (row[i] << 8) | row[i + 1]
                lcd.fill_rect(
                    x_offset + x * scale,
                    y * scale,
                    scale,
                    scale,
                    color
                )
