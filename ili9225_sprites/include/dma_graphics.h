#ifndef _DMA_GRAPHICS_H_
#define _DMA_GRAPHICS_H_

#include <stdint.h>
#include "ili9225.h"       // For dimension constants and command helpers
#include "hardware/dma.h"
#include "hardware/spi.h"

#ifdef __cplusplus
extern "C" {
#endif

/**
 * Initialize the DMA subsystem and claim a channel.
 * Call once after ili9225_init() during startup.
 */
void dma_graphics_init(void);

/**
 * Transfers a block of RGB565 image data to the LCD using DMA.
 *
 * @param x       Starting X coordinate on screen (top-left corner).
 * @param y       Starting Y coordinate on screen.
 * @param width   Width of the image block.
 * @param height  Height of the image block.
 * @param data    Pointer to RGB565 packed pixel array (uint16_t[]).
 */
void dma_draw_image(uint16_t x, uint16_t y, uint16_t width, uint16_t height, const uint16_t *data);

/**
 * Fills a rectangular region with a solid RGB565 color using DMA.
 *
 * @param x       Starting X coordinate of rectangle.
 * @param y       Starting Y coordinate of rectangle.
 * @param width   Width of rectangle.
 * @param height  Height of rectangle.
 * @param color   RGB565 color to fill with.
 */
void dma_fill_rect(uint16_t x, uint16_t y, uint16_t width, uint16_t height, uint16_t color);

#ifdef __cplusplus
}
#endif

#endif // _DMA_GRAPHICS_H_
