"""
newsreceipt.py
Copyright (c) 2015 Brunston Poon/brupoon

Written for RPi and Adafruit Thermal Printer
(note to self: try PEP8 for functions/classes, etc.)
"""

from __future__ import print_function
import RPi.GPIO as GPIO
import sys, os, random, getopt, re
import subprocess, time, Image, socket
from Adafruit_Thermal import *
from button import Button

class NewsReceipt(Button):
    #class extends Button class
    def __init__(self):
        self.printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
        self.running = True
        self.locked
        self.buttons = [False]

        printer.setLineHeight(23)
        threading.Thread(target=self.main_loop).start()

        super(NewsReceipt, self).__init__()

    def main_loop(self):
        while(self.running):

    def button_pushed(self, button):
		self.buttons[button] = True

    def get_ip_address(self, ifname):
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		return socket.inet_ntoa(fcntl.ioctl(s.fileno(),0x8915,\
                                            struct.pack('256s',\
                                            ifname[:15]))[20:24])

if __name__ == '__main__':
    NewsReceipt()
