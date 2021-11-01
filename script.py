"""
Program is meant for 2560 x 1440 monitor.
This code is hardcoded as heck, but it works :)
"""

import cv2
import pyautogui
import numpy as np
import pytesseract
from time import sleep
from pynput.mouse import Button, Controller as MController
from pynput.keyboard import Key, Controller as KController

# Constants
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
WIDTH = 2560
HEIGHT = 1440
MIDDLEX = WIDTH/2
MIDDLEY = HEIGHT/2
HERO_POS = (2300, 280)
DART_POS = (2420, 234)
SUB_POS = (2280, 970)
SNIPER_POS = (2436, 806)
GO_POS = (2448, 1350)

# Use to control mouse clicks and movement
mouse = MController()

# Use to control key presses
keyboard = KController()

# Saves having to type 'mouse.position' and 'mouse.click' every time.
def click(x, y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    sleep(0.05)

# Always used at the start since you need to click out of the terminal window to the main game
def click_main_screen():
    click(MIDDLEX, MIDDLEY)

# Clicks on the hero in the buy menu, but does not place it (placing is based on map)
def get_hero():
    click(HERO_POS[0], HERO_POS[1])

# Clicks on dart monkey in the buy menu but does not place it
def get_dart():
    click(DART_POS[0], DART_POS[1])

# Clicks on sub in buy menu but does not place it
def get_sub():
    click(SUB_POS[0], SUB_POS[1])

# Clicks on sniper monkey in buy menu but does not place it
def get_sniper():
    click(SNIPER_POS[0], SNIPER_POS[1])

# Helper method to get screenshot of round, then read what the round is
def get_current_round():
    # First, get the image on the screen and get the text from the image
    image = pyautogui.screenshot(region=(1920, 8, 160, 90))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("round.png", image)
    text = pytesseract.image_to_string(image)

    # Then, get substring that is the actual round number and return it
    # Use try/accept because if cv cannot recognise the text, then there will be index and string errors.
    try:
        index = text.index('/')
        return text[index - 2 : index]
    except:
        print(text)
        return -1

# This method is used in most maps, where the opener on Round 1 can be hero, dart and sub.
# X and Y are specific to each map, where you want to place your opener towers.
def setup_hero_dart_sub(heroX, heroY, dartX, dartY, subX, subY):
    get_hero()
    click(heroX, heroY)

    get_dart()
    click(dartX, dartY)

    get_sub()
    click(subX, subY)

    # Click twice to make it go double speed
    click(GO_POS[0], GO_POS[1])
    click(GO_POS[0], GO_POS[1])

def sanctuary():
    round8done = False
    done = False

    setup_hero_dart_sub(1113, 234, 1672, 564, 981, 237)

    while not done:
        current_round = str(get_current_round()).strip()
        # Make sure to sleep for a moment after getting the current round, since the platforms move in sanctuary
        sleep(1)

        if (not round8done and current_round == '8'):
            # Upgrade the current sub
            click(981, 237)
            click(2070, 638)
            click(2070, 638)
            click(2070, 1030)

            # Buy a dart monkey for the left
            click(DART_POS[0], DART_POS[1])
            click(546, 366)

if __name__ == '__main__':
    # img = cv2.imread('test.png')
    # text = pytesseract.image_to_string(img)
    # print(text)

    looping = True
    while looping:
        mapInput = input("Map: ")
        mapInput = mapInput.lower()

        if (mapInput != 'e'):
            click_main_screen()

        if (mapInput == 's'):
            sanctuary()
        elif (mapInput == 'infernal'):
            print('hey')
        elif (mapInput == 'e'):
            looping = False
            print('cya')
        else:
            print('??? lol')
            print(mapInput)

