import network
import socket
import time
import urequests
from machine import Pin, I2C
from eps32.ssd1306 import SSD1306_I2C

# Wi-Fi 設定
SSID = "hahahahahahahahahahahaha"
PASSWORD = "1234567890987654321"
REMOTE_URL = "https://github.com/bosen-you/project"  # 替換成你的目標網址

# 連接 Wi-Fi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    
    print("Connecting to Wi-Fi...")
    while not wlan.isconnected():
        time.sleep(1)
    print("Connected! IP:", wlan.ifconfig()[0])
    return wlan.ifconfig()[0]

# 初始化 I2C 與 SSD1306 OLED
i2c = I2C(0, scl=Pin(22), sda=Pin(21))  # GPIO 22 (SCL), GPIO 21 (SDA)
oled = SSD1306_I2C(128, 64, i2c)  # 128x64 OLED

def display_text(text):
    oled.fill(0)  # 清除畫面
    oled.text(text, 0, 0)  # 在 (0,0) 顯示文字
    oled.show()

# 發送 HTTP 請求
def fetch_remote_data():
    try:
        response = urequests.get(REMOTE_URL)
        data = response.text[:20]  # 限制 20 字元內顯示
        print("Response:", data)
        display_text(data)  # 顯示在 OLED 上
        response.close()
    except Exception as e:
        print("Failed to fetch data:", e)
        display_text("Fetch Error")

# 啟動 Web 伺服器
def start_server(ip):
    addr = (ip, 80)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(addr)
    s.listen(5)
    print("Web server is running on", ip)
    
    while True:
        conn, addr = s.accept()
        print("Connection from:", addr)
        request = conn.recv(1024).decode()
        print("Request:", request)

        if "GET /text=" in request:
            text = request.split("GET /text=")[1].split(" ")[0]
            text = text.replace("%20", " ")  # 轉換 URL 空格
            display_text(text[:20])  # 限制 20 字元內顯示
        else:
            fetch_remote_data()  # 抓取遠端數據並顯示

        # 回應 HTML 頁面
        response = """
HTTP/1.1 200 OK
Content-Type: text/html

<html>
<head>
    <title>ESP32 OLED Display</title>
</head>
<body>
    <h1>Send Text to OLED</h1>
    <form action="/" method="GET">
        <input type="text" name="text" placeholder="Enter text">
        <input type="submit" value="Send">
    </form>
</body>
</html>
"""
        conn.send(response)
        conn.close()

# 主程式
ip = connect_wifi()
start_server(ip)
