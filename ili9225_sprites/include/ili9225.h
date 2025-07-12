#ifndef _ILI9225_H_
#define _ILI9225_H_

#include <stdint.h>
#include "hardware/gpio.h"
#include "hardware/spi.h"

// LCD dimensions
#define ILI9225_WIDTH  176
#define ILI9225_HEIGHT 220

// GPIO pin assignments (change as needed)
#define ILI9225_CS   5   // Chip Select
#define ILI9225_RST  6   // Reset
#define ILI9225_RS   7   // Register Select
#define ILI9225_LED  8   // Backlight control
#define ILI9225_SCK  2   // SPI Clock
#define ILI9225_SDI  3   // SPI MOSI

// SPI instance
#define ILI9225_SPI spi0

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Initializes the ILI9225 display:
 * - Sets up GPIOs and SPI interface
 * - Runs LCD reset and power-on sequences
 * - Applies display and gamma configuration
 */
void ili9225_init(void);

/**
 * Draws a single pixel at (x, y) with RGB565 color.
 *
 * @param x      Horizontal coordinate (0 to ILI9225_WIDTH - 1)
 * @param y      Vertical coordinate (0 to ILI9225_HEIGHT - 1)
 * @param color  RGB565 16-bit color value
 */
void ili9225_draw_pixel(uint16_t x, uint16_t y, uint16_t color);

/**
 * Fills the entire screen with a solid RGB565 color.
 *
 * @param color  RGB565 16-bit color value
 */
void ili9225_fill_screen(uint16_t color);

/**
 * Sends a command to the LCD controller via SPI.
 *
 * @param cmd  16-bit command value
 */
void ili9225_write_command(uint16_t cmd);

/**
 * Sends a data value to the LCD controller via SPI.
 *
 * @param data  16-bit data value
 */
void ili9225_write_data(uint16_t data);

/**
 * Sends a command followed by data (i.e. sets a register).
 *
 * @param reg   16-bit register address
 * @param data  16-bit data value to store in register
 */
void ili9225_write_reg(uint16_t reg, uint16_t data);

#ifdef __cplusplus
}
#endif

#endif // _ILI9225_H_
