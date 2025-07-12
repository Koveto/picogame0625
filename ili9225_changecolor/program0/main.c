// main.c
#include <stdio.h>
#include "pico/stdlib.h"
#include "ili9225.h"

int main()
{
    stdio_init_all();

    ili9225_init();

    // Test color fill: red, green, blue cycling
    while (true)
    {
        ili9225_fill_screen(0xF800); // Red
        sleep_ms(1000);
        ili9225_fill_screen(0x07E0); // Green
        sleep_ms(1000);
        ili9225_fill_screen(0x001F); // Blue
        sleep_ms(1000);
    }
    
    return 0;
    
}