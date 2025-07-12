#include "ili9225.h"
#include "pico/stdlib.h"
#include "hardware/spi.h"

void ili9225_init(void)
{
    // Initialize GPIOs
    gpio_init(ILI9225_CS);  gpio_set_dir(ILI9225_CS, GPIO_OUT);
    gpio_init(ILI9225_RST); gpio_set_dir(ILI9225_RST, GPIO_OUT);
    gpio_init(ILI9225_RS);  gpio_set_dir(ILI9225_RS, GPIO_OUT);
    gpio_init(ILI9225_LED); gpio_set_dir(ILI9225_LED, GPIO_OUT);
    gpio_put(ILI9225_LED, 1); // backlight on

    // SPI setup
    spi_init(ILI9225_SPI, 10 * 1000 * 1000); // 10 MHz default
    gpio_set_function(ILI9225_SCK, GPIO_FUNC_SPI);
    gpio_set_function(ILI9225_SDI, GPIO_FUNC_SPI);

    // Reset the display
    gpio_put(ILI9225_RST, 0); sleep_ms(10);
    gpio_put(ILI9225_RST, 1); sleep_ms(50);

    // Power-on sequence
    ili9225_write_reg(0x10, 0x0000);
    ili9225_write_reg(0x11, 0x0000);
    ili9225_write_reg(0x12, 0x0000);
    ili9225_write_reg(0x13, 0x0000);
    ili9225_write_reg(0x14, 0x0000); sleep_ms(40);

    ili9225_write_reg(0x11, 0x0018);
    ili9225_write_reg(0x12, 0x6121);
    ili9225_write_reg(0x13, 0x006F);
    ili9225_write_reg(0x14, 0x495F);
    ili9225_write_reg(0x10, 0x0800); sleep_ms(10);
    ili9225_write_reg(0x11, 0x103B); sleep_ms(50);

    // Display settings
    ili9225_write_reg(0x01, 0x011C);
    ili9225_write_reg(0x02, 0x0100);
    ili9225_write_reg(0x03, 0x1030);
    ili9225_write_reg(0x07, 0x0000);
    ili9225_write_reg(0x08, 0x0808);
    ili9225_write_reg(0x0B, 0x1100);
    ili9225_write_reg(0x0C, 0x0000);
    ili9225_write_reg(0x0F, 0x0D01);
    ili9225_write_reg(0x15, 0x0020);
    ili9225_write_reg(0x20, 0x0000);
    ili9225_write_reg(0x21, 0x0000);

    // GRAM configuration
    ili9225_write_reg(0x30, 0x0000);
    ili9225_write_reg(0x31, 0x00DB);
    ili9225_write_reg(0x32, 0x0000);
    ili9225_write_reg(0x33, 0x0000);
    ili9225_write_reg(0x34, 0x00DB);
    ili9225_write_reg(0x35, 0x0000);
    ili9225_write_reg(0x36, 0x00AF);
    ili9225_write_reg(0x37, 0x0000);
    ili9225_write_reg(0x38, 0x00DB);
    ili9225_write_reg(0x39, 0x0000);

    // Gamma settings
    ili9225_write_reg(0x50, 0x0000);
    ili9225_write_reg(0x51, 0x0808);
    ili9225_write_reg(0x52, 0x080A);
    ili9225_write_reg(0x53, 0x000A);
    ili9225_write_reg(0x54, 0x0A08);
    ili9225_write_reg(0x55, 0x0808);
    ili9225_write_reg(0x56, 0x0000);
    ili9225_write_reg(0x57, 0x0A00);
    ili9225_write_reg(0x58, 0x0710);
    ili9225_write_reg(0x59, 0x0710);

    // Turn on display
    ili9225_write_reg(0x08, 0x0012); sleep_ms(50);
    ili9225_write_reg(0x07, 0x1017);
}

void ili9225_draw_pixel(uint16_t x, uint16_t y, uint16_t color)
{
    if (x >= ILI9225_WIDTH || y >= ILI9225_HEIGHT) return;

    ili9225_write_reg(0x20, x); // X address
    ili9225_write_reg(0x21, y); // Y address
    ili9225_write_command(0x22); // GRAM write
    ili9225_write_data(color);    
}

void ili9225_fill_screen(uint16_t color)
{
    ili9225_write_reg(0x36, ILI9225_WIDTH - 1);
    ili9225_write_reg(0x37, 0);
    ili9225_write_reg(0x38, ILI9225_HEIGHT - 1);
    ili9225_write_reg(0x39, 0);

    ili9225_write_reg(0x20, 0);
    ili9225_write_reg(0x21, 0);
    ili9225_write_command(0x22);

    for (uint32_t i = 0; i < ILI9225_WIDTH * ILI9225_HEIGHT; i++)
    {
        ili9225_write_data(color);
    }
}

void ili9225_write_command(uint16_t cmd)
{
    gpio_put(ILI9225_RS, 0); // command mode
    gpio_put(ILI9225_CS, 0);
    uint8_t buf[2] = {cmd >> 8, cmd & 0xFF};
    spi_write_blocking(ILI9225_SPI, buf, 2);
    gpio_put(ILI9225_CS, 1);
}

void ili9225_write_reg(uint16_t reg, uint16_t data)
{
    ili9225_write_command(reg);
    ili9225_write_data(data);
}

void ili9225_write_data(uint16_t data)
{
    gpio_put(ILI9225_RS, 1); // data mode
    gpio_put(ILI9225_CS, 0);
    uint8_t buf[2] = {data >> 8, data & 0xFF};
    spi_write_blocking(ILI9225_SPI, buf, 2);
    gpio_put(ILI9225_CS, 1);
}
