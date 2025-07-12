#pragma once
#include "pico/stdlib.h"
#include "hardware/spi.h"

// Display resolution
#define ILI9225_WIDTH  176
#define ILI9225_HEIGHT 220

// Pin Configuration
#define ILI9225_CS     17
#define ILI9225_RST    21
#define ILI9225_RS     20
#define ILI9225_SCK    18
#define ILI9225_SDI    19
#define ILI9225_LED    22

// SPI instance
#define ILI9225_SPI    spi0

void ili9225_init(void);
void ili9225_draw_pixel(uint16_t x, uint16_t y, uint16_t color);
void ili9225_fill_screen(uint16_t color);