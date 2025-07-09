# pico-st7789-display
#  Raspberry Pi Pico W + ST7789 1.3" 240x240 IPS LCD MicroPython Display

This project demonstrates how to use a Raspberry Pi Pico W with a 1.3-inch 240x240 ST7789 IPS LCD display to:
- Display a "Hello World" message
- Show a countdown from 10 to 0

## 🔧 Hardware Used

- **Raspberry Pi Pico W**
- **ST7789 1.3" 240x240 IPS LCD** (SPI interface)
- Jumper wires

## 📌 Pin Wiring

| ST7789 Pin | Pico W Pin | Function                   |
|------------|-------------|---------------------------|
| GND        | GND         | Ground                    |
| VCC        | 3.3V (OUT)  | Power                     |
| SCL        | GP10        | SPI1 SCK                  |
| SDA        | GP11        | SPI1 MOSI                 |
| RES / RST  | GP12        | Reset (Output)            |
| DC         | GP13        | Data/Command              |
| CS         | GP9         | Chip Select               |
| BLK        | 3.3V (tie high) | Backlight (always on) |

> Ensure your display uses **3.3V logic** (most ST7789 do).

## 📂 File List

- `main.py`: Runs the display logic (hello + countdown)
- `st7789.py`: Low-level display driver
- `vga1_8x8.py`: 8x8 bitmap font for ASCII characters

## ▶️ Running the Code

1. Flash your Pico W with **MicroPython** (from https://micropython.org/download/rp2-pico-w/)
2. Use **Thonny IDE** to:
   - Open `main.py`, `st7789.py`, and `vga1_8x8.py`
   - Save all files to the **Pico** filesystem
3. Click **Run** ▶️ on `main.py`

## 🖥️ Output

- Screen Background Displays in chosen colors
- Displays: Hello World! other text plus a countdown
