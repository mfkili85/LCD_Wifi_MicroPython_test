import network
import socket
import time
import machine
from machine import Pin, I2C
from pico_i2c_lcd import I2cLcd

# --- CONFIGURATION ---
SSID = "Pico2W_LCD_Control"
PASSWORD = "password123"  # Minimum 8 characters

# I2C Setup (GP0 = SDA, GP1 = SCL)
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

# Scan for LCD address
try:
    I2C_ADDR = i2c.scan()[0]
    lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)
except IndexError:
    print("LCD not found. Check wiring!")
    machine.reset()

# --- ACCESS POINT SETUP ---
def setup_ap():
    ap = network.WLAN(network.AP_IF)
    ap.config(essid=SSID, password=PASSWORD)
    ap.active(True)
    
    while not ap.active():
        pass
    
    status = ap.ifconfig()
    print('Access Point Active')
    print('SSID:', SSID)
    print('IP Address:', status[0]) # Usually 192.168.4.1
    
    lcd.clear()
    lcd.putstr("SSID: " + SSID)
    lcd.move_to(0, 1)
    lcd.putstr(status[0])
    return status[0]

# --- HTML TEMPLATE ---
def web_page(current_text):
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Pico 2 W LCD</title>
        <style>
            body {{ font-family: Arial; text-align: center; padding-top: 50px; }}
            input[type=text] {{ padding: 10px; width: 80%; font-size: 18px; }}
            input[type=submit] {{ padding: 10px 20px; font-size: 18px; margin-top: 10px; background: #007bff; color: white; border: none; }}
        </style>
    </head>
    <body>
        <h1>LCD Controller</h1>
        <p>Current: <strong>{current_text}</strong></p>
        <form action="/" method="get">
            <input type="text" name="msg" maxlength="16" placeholder="Enter text here...">
            <br>
            <input type="submit" value="Send to LCD">
        </form>
    </body>
    </html>
    """
    return html

# --- START SERVER ---
ip = setup_ap()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

current_msg = "Waiting..."

while True:
    try:
        conn, addr = s.accept()
        request = conn.recv(1024).decode('utf-8')
        
        # Parse the message from the URL
        if "GET /?msg=" in request:
            msg_start = request.find("?msg=") + 5
            msg_end = request.find(" HTTP", msg_start)
            raw_msg = request[msg_start:msg_end]
            
            # Simple URL decoding for spaces and common characters
            current_msg = raw_msg.replace('+', ' ').replace('%21', '!').replace('%3F', '?')
            
            # Update LCD
            lcd.clear()
            lcd.putstr(current_msg)

        response = web_page(current_msg)
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print("Error:", e)
        if 'conn' in locals():
            conn.close()
