import time
from micropython import const
import ustruct as struct

# --- Command constants ---
ST77XX_SWRESET = const(0x01)
ST77XX_SLPIN   = const(0x10)
ST77XX_SLPOUT  = const(0x11)
ST77XX_NORON   = const(0x13)
ST77XX_INVOFF  = const(0x20)
ST77XX_INVON   = const(0x21)
ST77XX_CASET   = const(0x2A)
ST77XX_RASET   = const(0x2B)
ST77XX_RAMWR   = const(0x2C)
ST77XX_COLMOD  = const(0x3A)
ST77XX_DISPON  = const(0x29)

# --- MADCTL for rotation/mirroring ---
ST7789_MADCTL      = const(0x36)
ST7789_MADCTL_MY   = const(0x80)
ST7789_MADCTL_MX   = const(0x40)
ST7789_MADCTL_MV   = const(0x20)
ST7789_MADCTL_BGR  = const(0x08)

# --- Color mode ---
ColorMode_65K    = const(0x50)
ColorMode_16bit  = const(0x05)

# --- Common colors ---
BLACK   = const(0x0000)
BLUE    = const(0x001F)
RED     = const(0xF800)
GREEN   = const(0x07E0)
CYAN    = const(0x07FF)
MAGENTA = const(0xF81F)
YELLOW  = const(0xFFE0)
WHITE   = const(0xFFFF)

# --- Format constants ---
_ENCODE_PIXEL = ">H"
_ENCODE_POS   = ">HH"
_BUFFER_SIZE  = const(256)

# --- Delay helper ---
def delay_ms(ms):
    time.sleep_ms(ms)

# --- RGB helper ---
def color565(r, g=0, b=0):
    try:
        r, g, b = r
    except TypeError:
        pass
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3

# --- Base ST77xx Class ---
class ST77xx:
    def __init__(self, spi, width, height, reset, dc, cs=None, backlight=None,
                 xstart=0, ystart=0):
        self.width = width
        self.height = height
        self.spi = spi
        self.reset = reset
        self.dc = dc
        self.cs = cs
        self.backlight = backlight
        self.xstart = xstart
        self.ystart = ystart

    def dc_low(self):  self.dc.off()
    def dc_high(self): self.dc.on()
    def cs_low(self):  self.cs.off() if self.cs else None
    def cs_high(self): self.cs.on() if self.cs else None
    def reset_low(self):  self.reset.off() if self.reset else None
    def reset_high(self): self.reset.on() if self.reset else None

    def write(self, command=None, data=None):
        self.cs_low()
        if command is not None:
            self.dc_low()
            self.spi.write(bytes([command]))
        if data is not None:
            self.dc_high()
            self.spi.write(data)
        self.cs_high()

    def hard_reset(self):
        self.cs_low()
        self.reset_high()
        delay_ms(50)
        self.reset_low()
        delay_ms(50)
        self.reset_high()
        delay_ms(150)
        self.cs_high()

    def soft_reset(self):
        self.write(ST77XX_SWRESET)
        delay_ms(150)

    def sleep_mode(self, value):
        self.write(ST77XX_SLPIN if value else ST77XX_SLPOUT)

    def inversion_mode(self, value):
        self.write(ST77XX_INVON if value else ST77XX_INVOFF)

    def _set_color_mode(self, mode):
        self.write(ST77XX_COLMOD, bytes([mode & 0x77]))

    def _set_mem_access_mode(self, rotation, vert_mirror, horz_mirror, is_bgr):
        rotation &= 7
        value = {
            0: 0,
            1: ST7789_MADCTL_MX,
            2: ST7789_MADCTL_MY,
            3: ST7789_MADCTL_MX | ST7789_MADCTL_MY,
            4: ST7789_MADCTL_MV,
            5: ST7789_MADCTL_MV | ST7789_MADCTL_MX,
            6: ST7789_MADCTL_MV | ST7789_MADCTL_MY,
            7: ST7789_MADCTL_MV | ST7789_MADCTL_MX | ST7789_MADCTL_MY,
        }[rotation]
        if is_bgr:
            value |= ST7789_MADCTL_BGR
        self.write(ST7789_MADCTL, bytes([value]))

    def _encode_pos(self, x, y):
        return struct.pack(_ENCODE_POS, x + self.xstart, y + self.ystart)

    def _encode_pixel(self, color):
        return struct.pack(_ENCODE_PIXEL, color)

    def _set_columns(self, start, end):
        self.write(ST77XX_CASET, self._encode_pos(start, end))

    def _set_rows(self, start, end):
        self.write(ST77XX_RASET, self._encode_pos(start, end))

    def set_window(self, x0, y0, x1, y1):
        self._set_columns(x0, x1)
        self._set_rows(y0, y1)
        self.write(ST77XX_RAMWR)

    def pixel(self, x, y, color):
        self.set_window(x, y, x, y)
        self.write(None, self._encode_pixel(color))

    def fill_rect(self, x, y, w, h, color):
        self.set_window(x, y, x + w - 1, y + h - 1)
        chunks, rest = divmod(w * h, _BUFFER_SIZE)
        pixel = self._encode_pixel(color)
        self.dc_high()
        if chunks:
            data = pixel * _BUFFER_SIZE
            for _ in range(chunks):
                self.write(None, data)
        if rest:
            self.write(None, pixel * rest)

    def fill(self, color):
        self.fill_rect(0, 0, self.width, self.height, color)

    def blit_buffer(self, buffer, x, y, width, height):
        self.set_window(x, y, x + width - 1, y + height - 1)
        self.write(None, buffer)

    def text(self, font, text, x, y, color):
        for char in text:
            self.char(font, char, x, y, color)
            x += font.WIDTH

    def char(self, font, char, x, y, color):
        code = ord(char)
        index = code - font.start
        if index < 0 or index >= len(font.data):
            return  # skip unsupported character
        data = font.data[index]
        for row, byte in enumerate(data):
            for col in range(font.WIDTH):
                if byte & (1 << (7 - col)):
                    self.pixel(x + col, y + row, color)

# --- ST7789 subclass ---
class ST7789(ST77xx):
    def init(self, *, color_mode=ColorMode_65K | ColorMode_16bit):
        self.hard_reset()
        self.soft_reset()
        self.sleep_mode(False)
        self._set_color_mode(color_mode)
        delay_ms(50)
        self._set_mem_access_mode(3, False, False, False) # Try diff ints and T/F for different orientations
        self.inversion_mode(True)
        delay_ms(10)
        self.write(ST77XX_NORON)
        delay_ms(10)
        self.fill(0)
        self.write(ST77XX_DISPON)
        delay_ms(500)
