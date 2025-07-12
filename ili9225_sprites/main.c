#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "ili9225.h"
#include "dma_graphics.h"

// Your RGB565 sprite sheet
extern const uint16_t test_image[]; // 48x48 pixels

#define TILE_WIDTH 16
#define TILE_HEIGHT 16
#define IMAGE_WIDTH 48

// Temporary buffer for a single tile
static uint16_t tile_buffer[TILE_WIDTH * TILE_HEIGHT];

void extract_tile(uint8_t tile_x, uint8_t tile_y)
{
    // Top-left pixel offset of tile
    uint16_t start_x = tile_x * TILE_WIDTH;
    uint16_t start_y = tile_y * TILE_HEIGHT;

    for (uint8_t y = 0; y < TILE_HEIGHT; y++) {
        uint32_t row_offset = (start_y + y) * IMAGE_WIDTH;
        memcpy(
            &tile_buffer[y * TILE_WIDTH],
            &test_image[row_offset + start_x],
            TILE_WIDTH * sizeof(uint16_t)
        );
    }
}

int main()
{
    stdio_init_all();
    sleep_ms(500); // Optional serial warm-up

    ili9225_init();         // LCD init
    dma_graphics_init();    // DMA init

    // Step 1: clear screen to black
    dma_fill_rect(0, 0, ILI9225_WIDTH, ILI9225_HEIGHT, 0x0000); // Black
    sleep_ms(100);

    // Step 2: extract tile (0,0) from sprite sheet
    extract_tile(0, 0); // Top-left tile

    // Step 3: draw tile in a 13x11 grid
    for (uint8_t row = 0; row < 11; row++) {
        for (uint8_t col = 0; col < 13; col++) {
            uint16_t xpos = col * TILE_WIDTH;
            uint16_t ypos = row * TILE_HEIGHT;
            dma_draw_image(xpos, ypos, TILE_WIDTH, TILE_HEIGHT, tile_buffer);
        }
    }

    while (true) {
        tight_loop_contents(); // Idle
    }
}
