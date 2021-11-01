"""
Program is meant for 2560 x 1440 monitor.
This code is hardcoded as heck, but it works :)
"""

import cv2
import imagehash
import pyautogui
import numpy as np
import pytesseract
from PIL import Image
from time import sleep
from pynput.mouse import Button, Controller as MController
from pynput.keyboard import Key, Controller as KController

# Constants
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CUTOFF = 5 # Used when comparing images
WIDTH = 2560
HEIGHT = 1440
MIDDLEX = WIDTH/2
MIDDLEY = HEIGHT/2
HERO_POS = (2300, 280)
DART_POS = (2420, 234)
SUB_POS = (2280, 970)
SNIPER_POS = (2436, 806)
GO_POS = (2448, 1350)

# Refers to the X pos of the upgrade menu, being either left or right side depending on monkey pos.
LEFT_SIDE_UGPRADES = 440
RIGHT_SIDE_UPGRADES = 2070
FIRST_TREE = 638
SECOND_TREE = 846
THIRD_TREE = 1030

# Use to control mouse clicks and movement
mouse = MController()

# Use to control key presses
keyboard = KController()

# Saves having to type 'mouse.position' and 'mouse.click' every time.
def click(x, y):
    mouse.position = (x, y)
    mouse.press(Button.left)
    mouse.release(Button.left)
    sleep(0.2)

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

# After finishing 40 rounds, click on the following buttons to go to main menu
# Remember the finish screens take time to open, so sleep for a moment.
def go_home():
    sleep(1)
    click(1280, 1210)
    sleep(1)
    click(930, 1125)

# Take screenshot. If same as 'go_btn.png' then the round has 'finished', and return true
def get_round_status():
    image = pyautogui.screenshot(region=(2364, 1278, 158, 151))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("round_status.png", image)

    current = imagehash.average_hash(Image.open('round_status.png'))
    original = imagehash.average_hash(Image.open('go_btn.png'))

    if current - original < CUTOFF:
        return True
    else:
        return False

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
    current_round = 1
    done = False

    setup_hero_dart_sub(1113, 234, 1672, 564, 981, 237)
    while not done:
        finished = get_round_status()
        if (finished):
            current_round += 1

            if (current_round == 9):
                # Get a new sub
                get_sub()
                click(1247, 244)

                # Upgrade the 1st sub
                click(981, 237)
                click(RIGHT_SIDE_UPGRADES, 638)
                click(RIGHT_SIDE_UPGRADES, 1030)
                click(RIGHT_SIDE_UPGRADES, 638)

                # Buy a dart monkey for the left
                click(DART_POS[0], DART_POS[1])
                click(546, 566)

            elif (current_round == 23):
                # Upgrade 1st dart monkey
                click(1874, 338)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

                # Upgrade the 1st sub
                click(981, 237)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

                # Upgrade 2nd sub
                click(1247, 244)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)

                # Click off upgrades so you can click on left dart monkey
                click(MIDDLEX, MIDDLEY)

                # Upgrade 2nd dart monkey
                click(546, 566)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif (current_round == 41):
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

if __name__ == '__main__':
    looping = True
    while looping:
        mapInput = input("Map: ")
        mapInput = mapInput.lower()

        if (mapInput != 'e'):
            click_main_screen()

        if (mapInput == 's'):
            sanctuary()
        elif (mapInput == 'i'):
            print('hey')
        elif (mapInput == 'e'):
            looping = False
            print('cya')
        else:
            print('??? lol')

