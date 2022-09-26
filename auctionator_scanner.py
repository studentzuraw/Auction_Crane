"""
Module to log in to the game and scan Auction House
using Auctioneer guide
"""
import subprocess
import time
import ctypes
import keyboard
import pyautogui

VK_NUMLOCK = 0x90


def main():
    """
    Step by step new Auctionator.lua gathering
    """
    with open("password.txt", "r", encoding="utf-8") as file_1:
        password = file_1.read()

    hll_dll = ctypes.WinDLL("User32.dll")

    # Check if num is on, if not change its status to on
    if not hll_dll.GetKeyState(VK_NUMLOCK):
        hll_dll.keybd_event(VK_NUMLOCK, 0x3A, 0x1, 0)
        hll_dll.keybd_event(VK_NUMLOCK, 0x3A, 0x3, 0)
        print("Num Lock was turned off, changed status to on")
    else:
        print("Num Lock was turned on, status was not changed")

    # open World of Worcraft.exe
    subprocess.Popen(
        r"C:\wow\World of Warcraft 3.3.5a (no install)\Wow"
    )  # Consider using 'with' for resource-allocating operations (consider-using-with) - pylint

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
    pyautogui.moveTo(1220, 439)
    pyautogui.click(button="right")
    time.sleep(10)

    # Click on "More" Button
    move_click_wait(371, 543, 10)

    # Click "Full Scan" Button
    move_click_wait(722, 190, 10)

    # Click "Start scanning" Button
    move_click_wait(537, 291, 25)

    # Close app
    keyboard.send("enter")
    time.sleep(0.5)
    keyboard.write(r"/exit")
    time.sleep(0.5)
    keyboard.send("enter")

    print("Finish")


def move_click_wait(x_axis, y_axis, time_value):
    """
    Repeatable function to move click and wait
    """
    pyautogui.moveTo(x_axis, y_axis)
    pyautogui.click()
    time.sleep(time_value)


if __name__ == "__main__":
    main()
