"""
Module to log in to the game and scan Auction House
using Auctioneer guide
"""
import subprocess
import time
import ctypes
import keyboard
import pyautogui

# NUM 7 PRESS TWICE TO FIRST PERSON
# Clicking directly by using pyautogui.click(x=,y=) is bugged
# First use .moveTo(x=,y=) then click()

with open("password.txt", "r", encoding="utf-8") as f:
    password = f.read()

hllDll = ctypes.WinDLL("User32.dll")
VK_NUMLOCK = 0x90

# Check if num is on, if not change its status to on
if not hllDll.GetKeyState(VK_NUMLOCK):
    hllDll.keybd_event(VK_NUMLOCK, 0x3A, 0x1, 0)
    hllDll.keybd_event(VK_NUMLOCK, 0x3A, 0x3, 0)
    print("Num Lock was turned off, changed status to on")
else:
    print("Num Lock was turned on, status was not changed")

# open World of Worcraft.exe
p1 = subprocess.Popen(r"C:\wow\World of Warcraft 3.3.5a (no install)\Wow")

time.sleep(15)

# Enter password
keyboard.write(password)
time.sleep(1)
keyboard.send("enter")
time.sleep(10)

# Select Character
pyautogui.moveTo(x=1674, y=688)
pyautogui.doubleClick()
time.sleep(10)

# Click on Auctioner
pyautogui.press("num7")  # Num 7
pyautogui.press("num7")  # Num 7
pyautogui.click(button="right", x=1220, y=439)
time.sleep(10)

# Click on "More" Button
pyautogui.moveTo(x=371, y=543)
pyautogui.click()
time.sleep(10)

# Click "Full Scan" Button
pyautogui.moveTo(x=722, y=190)
pyautogui.click()
time.sleep(10)

# Click "Start scanning" Button
pyautogui.moveTo(x=537, y=291)
pyautogui.click()
time.sleep(30)

# Close app
keyboard.send("enter")
time.sleep(0.5)
keyboard.send(r"/exit")
time.sleep(0.5)
keyboard.send("enter")

print("Finish")
