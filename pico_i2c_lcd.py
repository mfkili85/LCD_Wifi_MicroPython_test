import utime
from lcd_api import LcdApi

# PCF8574 pin definitions
MASK_RS = 0x01
MASK_RW = 0x02
MASK_E  = 0x04
SHIFT_BACKLIGHT = 3
SHIFT_DATA = 4

class I2cLcd(LcdApi):
    def __init__(self, i2c, i2c_addr, num_lines, num_columns):
        self.i2c = i2c
        self.i2c_addr = i2c_addr
        self.i2c.writeto(self.i2c_addr, bytes([0]))
        utime.sleep_ms(20)
        self.hal_write_init_nibble(0x30)
        utime.sleep_ms(5)
        self.hal_write_init_nibble(0x30)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(0x30)
        utime.sleep_ms(1)
        self.hal_write_init_nibble(0x20)
        utime.sleep_ms(1)
        super().__init__(num_lines, num_columns)
        cmd = self.LCD_FUNCTION_SET | self.LCD_2LINE
        self.hal_write_command(cmd)
        self.hal_write_command(self.LCD_DISPLAY_CONTROL | self.LCD_DISPLAY_ON)
        self.clear()

    def hal_write_init_nibble(self, nibble):
        byte = ((nibble >> 4) << SHIFT_DATA) | MASK_E
        self.i2c.writeto(self.i2c_addr, bytes([byte | (1 << SHIFT_BACKLIGHT)]))
        self.i2c.writeto(self.i2c_addr, bytes([(byte & ~MASK_E) | (1 << SHIFT_BACKLIGHT)]))

    def hal_backlight_on(self):
        self.i2c.writeto(self.i2c_addr, bytes([1 << SHIFT_BACKLIGHT]))

    def hal_backlight_off(self):
        self.i2c.writeto(self.i2c_addr, bytes([0]))

    def hal_write_command(self, cmd):
        self.hal_write_8bits(cmd, 0)

    def hal_write_data(self, data):
        self.hal_write_8bits(data, MASK_RS)

    def hal_write_8bits(self, value, mode):
        byte = (1 << SHIFT_BACKLIGHT) | mode
        nibble_high = (value & 0xF0) | byte
        self.i2c.writeto(self.i2c_addr, bytes([nibble_high | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([nibble_high & ~MASK_E]))
        nibble_low = ((value << 4) & 0xF0) | byte
        self.i2c.writeto(self.i2c_addr, bytes([nibble_low | MASK_E]))
        self.i2c.writeto(self.i2c_addr, bytes([nibble_low & ~MASK_E]))
