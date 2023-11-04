import os
import sys
import logging
import spidev as SPI
sys.path.append("..")
from lib import LCD_1inch8 as LCD
from PIL import Image, ImageDraw, ImageFont
import socket

# Raspberry Pi pin configuration:
RST = 13  # Reset pin (you may need to change this depending on your wiring)
DC = 22   # Data/Command pin
BL = 6   # Backlight control pin
bus = 0   # SPI bus (0 or 1)
device = 0  # SPI device (0 or 1)

logging.basicConfig(level=logging.DEBUG)
directory = os.getcwd()

# Server For Data Reception
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('0.0.0.0', 1013))
server.listen(2)

doInterrupt = 0
showOn = 0

def show(emotion):
    global doInterrupt, showOn, disp
    try:
        disp = LCD.LCD_1inch8(spi=SPI.SpiDev(bus, device), rst=RST, dc=DC, bl=BL)
        disp.Init()  # Initialize the library.
        bg = Image.new("RGB", (disp.width, disp.height), "BLACK")
        draw = ImageDraw.Draw(bg)
        
        for i in range(180):
            if doInterrupt == 1:
                doInterrupt = 0
                break
            else:
                image = Image.open(directory + '/emotion/' + emotion + '/frame' + str(i) + '.png')
                image = image.rotate(180)
                disp.ShowImage(image)
        
        showOn = 0
        disp.module_exit()
        logging.info("quit:")
    except IOError as e:
        logging.info(e)
    except KeyboardInterrupt:
        disp.module_exit()
        logging.info("quit:")
        exit()

def main():
    global doInterrupt, showOn
    previousData = 'happy'
    show('happy')
    conn, addr = server.accept()
    conn.settimeout(0.1)
    
    while True:
        try:
            data = conn.recv(5).decode()
            if previousData != data:
                print(data)
                doInterrupt = 1
                previousData = data
                show(data)
        except socket
