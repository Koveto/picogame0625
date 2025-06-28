from machine import Pin, PWM, ADC, Timer
import LCD
import time

# Buttons
b1 = Pin(0, Pin.IN, Pin.PULL_UP)
b2 = Pin(1, Pin.IN, Pin.PULL_UP)
b3 = Pin(2, Pin.IN, Pin.PULL_UP)
b4 = Pin(3, Pin.IN, Pin.PULL_UP)

# QYF-860
vrx = ADC(27)
vry = ADC(26)
sw  = Pin(28, Pin.IN, Pin.PULL_UP)

# Create a PWM object on GPIO15
buzzer = PWM(Pin(15))

DEBOUNCE_DELAY_MS = 50
debounce_timer = Timer()
debounce_active = False

def play_zelda():
    play_tone(740, 0.15)  # Gb5
    play_tone(698, 0.15)  # F5
    play_tone(587, 0.15)  # D5
    play_tone(415, 0.15)  # Ab4
    play_tone(392, 0.15)  # G4
    play_tone(622, 0.15)  # Eb5
    play_tone(783, 0.15)  # G5
    play_tone(987, 0.3)   # B5

def debounce_callback(timer):
    global debounce_active
    debounce_active = False

def play_tone(frequency, duration):
    buzzer.freq(frequency)
    buzzer.duty_u16(32768)  # Midpoint duty cycle for audible sound
    time.sleep(duration)
    buzzer.duty_u16(0)  # Turn off the buzzer

def pin_irq_handler(pin):
    global debounce_active
    if debounce_active:
        return
    debounce_active = True
    play_zelda()
    debounce_timer.init(mode=Timer.ONE_SHOT, period=DEBOUNCE_DELAY_MS, callback=debounce_callback)

sw.irq(trigger=Pin.IRQ_FALLING, handler=pin_irq_handler)
b1.irq(trigger=Pin.IRQ_FALLING, handler=pin_irq_handler)
b2.irq(trigger=Pin.IRQ_FALLING, handler=pin_irq_handler)
b3.irq(trigger=Pin.IRQ_FALLING, handler=pin_irq_handler)
b4.irq(trigger=Pin.IRQ_FALLING, handler=pin_irq_handler)

if __name__ == "__main__":
    # ST7789V
    bl = PWM(Pin(13))
    bl.freq(1000)
    bl.duty_u16(32768)
    lcd = LCD.LCD_1inch3()
    lcd.fill(0xffff) #white
    lcd.show()
    
    while True:
        time.sleep(1)

"""
if __name__=='__main__':
    pwm = PWM(Pin(BL))
    pwm.freq(1000)
    pwm.duty_u16(32768)#max 65535

    LCD = LCD_1inch3()
    #color BRG
    LCD.fill(LCD.WHITE)
    LCD.show()
    
    LCD.fill(LCD.C)
    LCD.fill_rect(0,0,320,100,LCD.D)
    LCD.scroll(50,0)
    time.sleep(1)
    LCD.show()"""
"""while(1):
        time.sleep(1)
        LCD.show()
        #LCD.fill(c)
        #LCD.fill(LCD.D)
        #LCD.fill_rect(x,y,w,h,c)
        #LCD.fill_rect(0,0,320,24,LCD.D)
        #LCD.rect(x,y,w,h,c)
        #LCD.rect(0,0,320,24,LCD.A)
        #LCD.pixel(x,y,c)
        #LCD.pixel(100,100,LCD.A)
        #LCD.hline(x,y,w,c)
        #LCD.hline(10,10,100,LCD.C)
        #LCD.vline(x,y,h,c)
        #LCD.vline(10,10,100,LCD.C)
        #LCD.line(x1,y1,x2,y2,c)
        #LCD.line(0,0,100,100,LCD.C)
        #LCD.ellipse(x,y,xr,yr,c)
        #LCD.ellipse(100,100,100,100,LCD.C)
        #LCD.text("Test",10,10,LCD.C) #8x8 pixel
        
        LCD.fill_rect(0,0,320,100,LCD.D)
        LCD.scroll(100,100)"""
"""time.sleep(0.1)
        LCD.fill_rect(0,0,320,24,LCD.RED)
        LCD.rect(0,0,320,24,LCD.RED)
        LCD.text("Raspberry Pi Pico",2,8,LCD.WHITE)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,24,320,24,LCD.BLUE)
        LCD.rect(0,24,320,24,LCD.BLUE)
        LCD.text("PicoGo",2,32,LCD.WHITE)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,48,320,24,LCD.GREEN)
        LCD.rect(0,48,320,24,LCD.GREEN)
        LCD.text("Pico-LCD-2",2,54,LCD.WHITE)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,72,320,24,0X07FF)
        LCD.rect(0,72,320,24,0X07FF)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,96,320,24,0xF81F)
        LCD.rect(0,96,320,24,0xF81F)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,120,320,24,0x7FFF)
        LCD.rect(0,120,320,24,0x7FFF)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,144,320,24,0xFFE0)
        LCD.rect(0,144,320,24,0xFFE0)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,168,320,24,0XBC40)
        LCD.rect(0,168,320,24,0XBC40)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,192,320,24,0XFC07)
        LCD.rect(0,192,320,24,0XFC07)
        time.sleep(0.1)
        LCD.show()
        LCD.fill_rect(0,216,320,24,0X8430)
        LCD.rect(0,216,320,24,0X8430)
        time.sleep(0.1)
        LCD.show()
        LCD.fill(0xFFFF)
        time.sleep(0.1)
        LCD.show()"""
"""
    time.sleep(1)
    LCD.fill(0xFFFF)
"""

'''
LCD.rect(0,0,160,128,colour(0,0,255)) # Blue Frame
LCD.text("WaveShare", 44,10,colour(255,0,0))
LCD.text('Pico Display 1.8"', 10,24,colour(255,255,0))
LCD.text("160x128 SPI", 38,37,colour(0,255,0))
LCD.text("Tony Goodhew", 30,48,colour(100,100,100))
c = colour(255,240,0)
printstring("New Font - Size 1",14,65,1,0,0,c)
c = colour(255,0,255)
printstring("Now size 2",12,78,2,0,0,c)
c = colour(0,255,255)
printstring("Size 3",30,100,3,0,0,c)

LCD.pixel(0,0,0xFFFF)     # Left Top - OK
LCD.pixel(0,239,0xFFFF)   # Left Bottom - OK
LCD.pixel(319,0,0xFFFF)   # Right Top - OK
LCD.pixel(319,239,0xFFFF) # Right Bottom - OK
LCD.show()
utime.sleep(20)
'''