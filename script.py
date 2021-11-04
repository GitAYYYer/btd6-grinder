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
BOOMERANG_POS = (2276, 469)
BOMB_POS = (2438, 468)
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

# Clicks on boomerang monkey but does not place it
def get_boomerang():
    click(BOOMERANG_POS[0], BOOMERANG_POS[1])

# Clicks on bomb tower but does not place it
def get_bomb():
    click(BOMB_POS[0], BOMB_POS[1])

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
    sleep(0.5)
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

# Same concept as setup_hero_dart_sub, except uses sniper in place of sub
def setup_hero_dart_sniper(heroX, heroY, dartX, dartY, sniperX, sniperY):
    get_hero()
    click(heroX, heroY)

    get_dart()
    click(dartX, dartY)

    get_sniper()
    click(sniperX, sniperY)

    # Click twice to make it go double speed
    click(GO_POS[0], GO_POS[1])
    click(GO_POS[0], GO_POS[1])

def sanctuary():
    current_round = 1
    done = False

    setup_hero_dart_sub(1113, 234, 1672, 564, 981, 237)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 9:
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

            elif current_round == 23:
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

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def ravine():
    current_round = 1
    done = False

    setup_hero_dart_sniper(1602, 641, 935, 143, 1381, 263)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 2:
                # Set first sniper to target strong
                click(1381, 264)
                click(120, 500)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 13:
                # Upgrade 1st sniper
                click(1381, 263)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 21:
                # Upgrade 1st sniper
                click(1381, 263)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

                # Buy boomerang to clean up
                get_boomerang()
                click(991, 1093)
                click(991, 1093)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 35:
                # Upgrade 1st sniper
                click(1381, 263)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)

                # Upgrade boomerang
                click(991, 1093)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 36:
                # Buy bomb
                click(924, 236)
                click(924, 236)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY)
                
            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def flooded():
    current_round = 1
    done = False

    setup_hero_dart_sub(288, 127, 690, 672, 1246, 228)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 17:
                # Upgrade 1st sub
                click(1246, 228)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)

                # Buy 2nd sub, get upgrades for it
                get_sub()
                click(1338, 1045)
                click(1338, 1045)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

            elif current_round == 29:
                # Can just click bottom upgrade, upgrade menu is still open
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def infernal():
    current_round = 1
    done = False

    setup_hero_dart_sub(2138, 644, 619, 374, 567, 1105)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 10:
                # Upgrade dart monkey
                click(619, 374)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)

                # Upgrade 1st sub
                click(567, 1105)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY)

                # Buy 2nd sub, upgrade it
                get_sub()
                click(1540, 316)
                click(1540, 316)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 27:
                # Upgrade 1st sub
                click(567, 1105)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)

                # Upgrade 2nd sub
                click(1540, 316)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 29:
                # Upgrade 1st sub
                click(567, 1105)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def bloody():
    current_round = 1
    done = False

    setup_hero_dart_sub(368, 144, 1570, 932, 805, 781)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 9:
                # Buy sub on right side, upgrade it
                get_sub()
                click(1594, 261)
                click(1594, 261)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY) # Need to click off, to place left sub

                # Buy sub on left side
                get_sub()
                click(372, 580)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 21:
                # Upgrade left sub
                click(372, 580)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)

                # Upgrade middle (1st) sub
                click(805, 781)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)

                # Upgrade right sub
                click(1594, 261)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 36:
                # Upgrade left sub
                click(372, 580)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)

                # Upgrade right sub
                click(1594, 261)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def workshop():
    current_round = 1
    done = False

    setup_hero_dart_sniper(670, 660, 190, 830, 1365, 670)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 11:
                # Upgrade sniper
                click(1365, 670)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 21:
                # Buy 2nd sniper, upgrade it. ALSO, set to strong.
                get_sniper()
                click(1309, 613)
                click(1309, 613)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(120, 500) # X,Y for setting strong
                click(MIDDLEX - 50, MIDDLEY)

            elif current_round == 35:
                # Upgrade 1st sniper
                click(1365, 670)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

                # Upgrade 2nd sniper
                click(1309, 613)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(MIDDLEX - 50, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def quad():
    current_round = 1
    done = False

    setup_hero_dart_sub(1042, 1142, 1560, 1040, 980, 625)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 15:
                # Upgrade 1st sub
                click(980, 625)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)

                # Buy 2nd sub, click on it, upgrade it
                get_sub()
                click(1227, 600)
                click(1227, 600)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 29:
                # Upgrade 2nd sub
                click(1227, 600)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 33:
                # Upgrade 1st sub, to stop lots of leaks
                click(980, 625)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def dark():
    current_round = 1
    done = False
    
    setup_hero_dart_sub(713, 618, 608, 1059, 1459, 574)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 18:
                # Buy dart monkey
                get_dart()
                click(590, 410)

                # Upgrade 1st sub
                click(1459, 574)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)

                # Buy new sub, make sure to click on it again after buying it
                get_sub()
                click(1444, 926)
                click(1444, 926)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 30:
                # Upgrade 2nd sub
                click(1444, 926)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def muddy():
    current_round = 1
    done = False

    setup_hero_dart_sub(452, 120, 1564, 393, 1025, 793)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 10:
                # Upgrade 1st sub
                click(1025, 793)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)

                # Buy 2nd sub, upgrade it.
                get_sub()
                click(444, 602)
                click(444, 602)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 27:
                # Upgrade 2nd sub
                click(444, 602)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)
                click(RIGHT_SIDE_UPGRADES, SECOND_TREE)

                # Upgrade 1st sub
                click(1025, 793)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)

                # Upgrade dart monkey
                click(1564, 393)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 34:
                # Upgrade 1st sub
                click(1025, 793)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(MIDDLEX, MIDDLEY)
                
            elif current_round == 41:
                done = True

            # Before clicking next round, wait a moment
            sleep(0.1)
            click(GO_POS[0], GO_POS[1])

    # Go back to main menu
    go_home()

def ouch():
    # In the middle there is a removable object, so need to click off of it to proceed.
    click(MIDDLEX, 100)

    current_round = 1
    done = False

    setup_hero_dart_sub(715, 398, 1367, 212, 955, 810)
    while not done:
        finished = get_round_status()
        if finished:
            current_round += 1

            if current_round == 15:
                # Buy 2nd dart monkey
                get_dart()
                click(332, 901)

                # Upgrade 1st sub
                click(955, 810)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)
                click(RIGHT_SIDE_UPGRADES, FIRST_TREE)

                # Buy 2nd sub, upgrade it
                get_sub()
                click(1275, 631)
                click(1275, 631)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(LEFT_SIDE_UGPRADES, SECOND_TREE)
                click(MIDDLEX, MIDDLEY)

            elif current_round == 27:
                # Upgrade 1st sub
                click(955, 810)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)
                
                # Buy 3rd sub, cant buy 4th upgrade for 1st sub so might as well just chuck money to a 3rd sub
                get_sub()
                click(1305, 813)
                click(1305, 813)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, FIRST_TREE)
                click(LEFT_SIDE_UGPRADES, THIRD_TREE)

            elif current_round == 39:
                # Shouldn't be necessary to win, but just in case, upgrade 1st sub
                click(955, 810)
                click(RIGHT_SIDE_UPGRADES, THIRD_TREE)

            elif current_round == 41:
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

        if mapInput != 'e':
            click_main_screen()

        if mapInput == 's':
            sanctuary()
        elif mapInput == 'r':
            ravine()
        elif mapInput == 'f':
            flooded()
        elif mapInput == 'i':
            infernal()
        elif mapInput == 'b':
            bloody()
        elif mapInput == 'w':
            workshop()
        elif mapInput == 'q':
            quad()
        elif mapInput == 'd':
            dark()
        elif mapInput == 'm':
            muddy()
        elif mapInput == 'o':
            ouch()
        elif mapInput == 'e':
            looping = False
            print('cya')
        else:
            print('??? lol')

