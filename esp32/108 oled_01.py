from machine import Pin, SoftI2C
import eps32.ssd1306 as ssd1306
import time

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=20000)  # 降低 I2C 頻率

lcd = ssd1306.SSD1306_I2C(128, 64, i2c)

lcd.fill(0)  # 清空畫面
lcd.text("ESP32 OLED Test", 10, 20)

time.sleep(0.1)  # 等待 I2C 穩定
#lcd.show()  # 顯示畫面

print("畫面應該顯示正常文字，如果還有雜訊，請回報！")
