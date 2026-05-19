# Pico 2W Web-to-LCD Controller 📶📟

Transform your **Raspberry Pi Pico 2W** into a standalone Wi-Fi portal. This project configures the Pico 2W as an **Access Point (AP)** and hosts a web server that allows any connected device (phone or laptop) to send custom text directly to a **12x2 I2C LCD**.

## 📺 Demo

The Pico 2W initializing the Access Point and displaying the interactive status on the LCD:

<p align="center">
  <img width="30%" alt="Pico 2W Setup" src="https://github.com/user-attachments/assets/0ed2e352-bb12-403d-b683-6a354213e8a4" />
  <img width="30%" alt="LCD Initialization" src="https://github.com/user-attachments/assets/0e002eed-9a45-4f22-90c6-6425acd68c2c" />
  <img width="30%" alt="Web Interface Active" src="https://github.com/user-attachments/assets/f1bc4d39-c55b-421e-95d9-057960119977" />
</p>

## 🚀 Features
- **Standalone Access Point:** Hosts its own 2.4GHz Wi-Fi network using the RP2350 wireless driver.
- **Interactive Web Server:** Serves an HTML page with an input field to update the LCD remotely.
- **I2C LCD Integration:** Optimized for 12x2 character displays.
- **Live Status:** The LCD shows the SSID and the IP address (`192.168.4.1`) so users know where to connect.

## 🛠 Hardware Setup

| LCD Pin | Pico 2W Pin | Function |
| :--- | :--- | :--- |
| **VCC** | **VBUS (5V)** | Power |
| **GND** | **GND** | Ground |
| **SDA** | **GP0** | I2C0 SDA |
| **SCL** | **GP1** | I2C0 SCL |

## ⚙️ Configuration

In your `main.py`, you can customize the network name and security:

```python
# --- CONFIGURATION ---
SSID = "Pico2W_LCD_Control"
PASSWORD = "password123"  # Minimum 8 characters
IP_ADDRESS = "192.168.4.1"

