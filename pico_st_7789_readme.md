# Smart Display with Raspberry Pi Pico and ST7789 LCD

This project demonstrates how to display text, countdown, and messages on a 240x240 1.3" ST7789 IPS LCD using MicroPython and a Raspberry Pi Pico or Pico W.

---

## 🔍 What's in this Project?
- `main.py` - The main program that shows text and countdown.
- `st7789.py` - The display driver that controls the ST7789 LCD.
- `vga1_8x8.py` - A simple 8x8 pixel font used to draw characters.

---

## 🧰 What You Need
- Raspberry Pi Pico or Pico W
- ST7789 1.3" 240x240 SPI LCD (with 7 pins)
- Jumper wires
- Breadboard or soldered connection
- Thonny (recommended) or another MicroPython IDE

---

## 🔌 Wiring Diagram
| ST7789 LCD Pin       | Connect to Pico    |
|----------------------|--------------------|
| GND                  | GND                |
| VCC                  | 3.3V OUT           |
| SCL (or SCK)         | GP10 (SPI1 SCK)    |
| SDA (or MOSI)        | GP11 (SPI1 MOSI)   |
| RES (RESET)          | GP12               |
| DC (Data/Command)    | GP13               |
| CS (Chip Select)     | GP9                |
| BLK (Backlight)      | 3.3V OUT           |

> **Note:** Some displays use the terms SCL/SDA instead of SCK/MOSI. They are functionally the same for SPI.

---

## 🔧 How to Set It Up

### 1. Install MicroPython on Your Pico
- Open Thonny
- Go to **Tools > Options > Interpreter**
- Select **MicroPython (Raspberry Pi Pico)**
- Click **Install or update firmware** if needed

### 2. Copy the Files
- Download and copy the following files into your Pico:
  - `main.py`
  - `st7789.py`
  - `vga1_8x8.py`

### 3. Run the Program
- Open `main.py` in Thonny
- Click the **green Run button**
- Your display should show:
  - "Hello World"
  - Your name
  - A countdown from 10 to 0
  - A final "Done!" message

---

## 🧠 How It Works
- The `st7789.py` driver initializes the display and provides functions to draw pixels and text.
- The `vga1_8x8.py` font file contains pixel data for each character.
- The `main.py` file:
  - Starts the screen
  - Displays text
  - Runs a countdown
  - Updates the display with each number

---

## 🛠 Troubleshooting
- **Nothing on screen:** Check all wiring. Make sure `BLK` and `VCC` are both connected to 3.3V.
- **Text is unreadable or mirrored:** Change the rotation setting or edit the `init()` method in `st7789.py` to fix orientation.
- **White screen only:** You might need to adjust the pin assignments in `main.py` to match your wiring.

---

## 📦 Example Output
- Hello World
- My name is Eloi Delva
- Countdown from 10 to 0
- Done!

---

Feel free to modify the text or display layout to suit your own projects!

