#include "dma_graphics.h"
#include "hardware/dma.h"
#include "hardware/spi.h"

// DMA channel handle
static int dma_chan;

void dma_graphics_init(void)
{
    // Claim a dedicated DMA channel for SPI transfers
    dma_chan = dma_claim_unused_channel(true);
}

void dma_draw_image(uint16_t x, uint16_t y, uint16_t width, uint16_t height, const uint16_t *data)
{
    if (x >= ILI9225_WIDTH || y >= ILI9225_HEIGHT) return;

    // Clamp if necessary
    if (x + width > ILI9225_WIDTH)  width  = ILI9225_WIDTH - x;
    if (y + height > ILI9225_HEIGHT) height = ILI9225_HEIGHT - y;

    // Set GRAM address window
    ili9225_write_reg(0x36, x + width - 1); // X end
    ili9225_write_reg(0x37, x);             // X start
    ili9225_write_reg(0x38, y + height - 1); // Y end
    ili9225_write_reg(0x39, y);              // Y start

    // Set address counter
    ili9225_write_reg(0x20, x);
    ili9225_write_reg(0x21, y);
    ili9225_write_command(0x22); // GRAM write

    // Cast to byte stream for DMA
    const uint8_t *byte_data = (const uint8_t *)data;
    size_t num_bytes = width * height * 2; // RGB565 = 2 bytes per pixel

    // Configure DMA
    dma_channel_config cfg = dma_channel_get_default_config(dma_chan);
    channel_config_set_transfer_data_size(&cfg, DMA_SIZE_8);
    channel_config_set_read_increment(&cfg, true);
    channel_config_set_write_increment(&cfg, false);
    channel_config_set_dreq(&cfg, spi_get_dreq(ILI9225_SPI, true)); // SPI TX DREQ

    dma_channel_configure(
        dma_chan,
        &cfg,
        &spi_get_hw(ILI9225_SPI)->dr, // SPI TX FIFO
        byte_data,                    // Source pixel data
        num_bytes,                    // Total bytes to send
        true                          // Start immediately
    );

    dma_channel_wait_for_finish_blocking(dma_chan);
}

void dma_fill_rect(uint16_t x, uint16_t y, uint16_t width, uint16_t height, uint16_t color)
{
    if (x >= ILI9225_WIDTH || y >= ILI9225_HEIGHT) return;

    // Clamp to bounds
    if (x + width > ILI9225_WIDTH)  width  = ILI9225_WIDTH - x;
    if (y + height > ILI9225_HEIGHT) height = ILI9225_HEIGHT - y;

    size_t pixel_count = width * height;
    static uint16_t color_buffer[176 * 220]; // Reusable scratch buffer

    if (pixel_count > sizeof(color_buffer) / sizeof(color_buffer[0])) return;

    for (size_t i = 0; i < pixel_count; i++) {
        color_buffer[i] = color;
    }

    dma_draw_image(x, y, width, height, color_buffer);
}
