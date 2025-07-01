# input_controller.py

from machine import ADC

# === HARDWARE SETUP ===
vrx = ADC(27)  # X-axis
vry = ADC(26)  # Y-axis

# === JOYSTICK TUNING ===
CENTER = 32768
DEADZONE = 6000
THRESHOLD = 12000  # Min deviation from center to count as movement

def read_direction():
    """
    Returns one of: 'up', 'down', 'left', 'right', or None.
    Allows fluid sliding between directions. Prioritizes larger axis movement.
    """
    x = vrx.read_u16()
    y = vry.read_u16()

    dx = x - CENTER
    dy = y - CENTER

    abs_dx = abs(dx)
    abs_dy = abs(dy)

    # Must exceed threshold in at least one axis
    if abs_dx < THRESHOLD and abs_dy < THRESHOLD:
        return None

    # Prioritize dominant axis
    if abs_dy > abs_dx:
        return "up" if dy < -DEADZONE else "down"
    else:
        return "left" if dx < -DEADZONE else "right"
