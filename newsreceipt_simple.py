"""
newsreceipt_simple.py
Copyright (c) 2015 Brunston Poon/brupoon

Written for RPi and Adafruit Thermal Printer
Adapted from github.com/iworkinpixels/news_rcpt-gen
(note to self: try PEP8 for functions/classes, etc.)
"""

from __future__ import print_function
import RPi.GPIO as GPIO
import sys, os, random, getopt, re
import subprocess, time, Image, socket
from Adafruit_Thermal import *


"""Initialization"""

led_pin = 18
button_pin = 23
hold_time = 3     # Duration for button hold (shutdown)
tap_time = 0.01  # Debounce time for button taps
printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
printer.setLineHeight(23) # So graphical characters fit together

# Use Broadcom pin numbers (not Raspberry Pi pin numbers) for GPIO
GPIO.setmode(GPIO.BCM)
# Enable LED and button (w/pull-up on latter)
GPIO.setup(led_pin, GPIO.OUT)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
# LED on while working
GPIO.output(led_pin, GPIO.HIGH)
# Processor load is heavy at startup; wait a moment to avoid
# stalling during greeting.
time.sleep(30)

# Show IP address (if network is available)
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(('8.8.8.8', 0))
    # printer.println('My IP address is ' + s.getsockname()[0])
    # printer.boldOn()
    # printer.println('Network connected.')
    # printer.boldOff()
    # printer.feed(3)
except:
    printer.boldOn()
    printer.println('Network not connected.')
    printer.boldOff()
    printer.feed(3)

# Print greeting image
printer.printImage(Image.open('dat/logo.png'), True)
printer.feed(3)
GPIO.output(led_pin, GPIO.LOW)

# Poll initial button state and time
prev_button_state = GPIO.input(button_pin)
prev_time = time.time()
tap_enable = False
hold_enable = False

"""End Initialization"""

def tap():
    # Called when button is briefly tapped.  Prints one copy of the news_rcpt.
    GPIO.output(led_pin, GPIO.HIGH)  # LED on while working

    generate_rcpt()
    news_rcpt = file("/ramdisk/news_rcpt.txt")

    printer.feed(3)
    for line in news_rcpt:
        printer.println(line)
    printer.feed(3)

    file.close(news_rcpt)
    GPIO.output(led_pin, GPIO.LOW)
    return None

def hold():
    # Called when button is held down.  Invokes shutdown process.
    GPIO.output(led_pin, GPIO.HIGH)
    subprocess.call(["shutdown", "-h", "now"])
    GPIO.output(led_pin, GPIO.LOW)
    return None

def generate_rcpt():
    #generates news receipt

    #Gets API and User information
    with open("dat/settings.cfg") as file:
        cfg_list = [line.rstrip('\n') for line in file]
    weather_key = cfg_list[0]
    username = cfg_list[1]
    weather_loc = cfg_list[2]


def text_setter():
    #makes sure all text will fit on the line, using new line.

def main_loop():
    while(True):
      # Poll current button state and time
      button_state = GPIO.input(button_pin)
      t = time.time()

      # Has button state changed?
      if button_state != prev_button_state:
        prev_button_state = button_state   # Yes, save new state/time
        prev_time = t
      else:                             # Button state unchanged
        if (t - prev_time) >= hold_time:  # Button held more than 'hold_time'?
          # Yes it has.  Is the hold action as-yet untriggered?
          if hold_enable == True:        # Yep!
            hold()                      # Perform hold action (usu. shutdown)
            hold_enable = False          # 1 shot...don't repeat hold action
            tap_enable = False          # Don't do tap action on release
        elif (t - prev_time) >= tap_time: # Not hold_time.  tap_time elapsed?
          # Yes.  Debounced press or release...
          if button_state == True:       # Button released?
            if tap_enable == True:       # Ignore if prior hold()
              tap()                     # Tap triggered (button released)
              tap_enable = False        # Disable tap and hold
              hold_enable = False
          else:                         # Button pressed
            tap_enable = True           # Enable tap and hold actions
            hold_enable = True

      # LED blinks while idle, for a brief interval every 2 seconds.
      # Pin 18 is PWM-capable and a "sleep throb" would be nice, but
      # the PWM-related library is a hassle for average users to install
      # right now.  Might return to this later when it's more accessible.
      if ((int(t) & 1) == 0) and ((t - int(t)) < 0.15):
        GPIO.output(led_pin, GPIO.HIGH)
      else:
        GPIO.output(led_pin, GPIO.LOW)

if __name__ == '__main__':
    main_loop()
