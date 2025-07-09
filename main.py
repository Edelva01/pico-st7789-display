import st7789
from machine import Pin, SPI
import time
import vga1_8x8 as font  # Make sure this file is saved on your Pico

# Setup SPI interface (SPI1)
spi = SPI(1, baudrate=30000000, sck=Pin(10), mosi=Pin(11))

# Initialize display
display = st7789.ST7789(
    spi,
    240,  # width
    320,  # height
    reset=Pin(12, Pin.OUT),
    dc=Pin(13, Pin.OUT),
    cs=Pin(9, Pin.OUT),
)

# Start display
display.init()
display.fill(st7789.BLACK)

# Show Hello World message
display.text(font, "Hello World", 30, 110, st7789.WHITE)
time.sleep(2)
display.text(font, "My name is Eloi Delva", 30, 130, st7789.WHITE)
time.sleep(2)

# Countdown loop
for i in range(10, -1, -1):
    display.fill(st7789.RED)
    display.text(font, "Countdown:", 60, 90, st7789.CYAN)
    display.text(font, str(i), 110, 110, st7789.YELLOW)
    time.sleep(1)

# Final message
display.fill(st7789.BLACK)
display.text(font, "Done!", 90, 120, st7789.GREEN)
