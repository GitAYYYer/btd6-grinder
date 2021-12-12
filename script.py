"""
Program is meant for 2560 x 1440 monitor.
This code is hardcoded as heck, but it works :)
"""

import cv2
import random
import imagehash
import pyautogui
import numpy as np
import pytesseract
from PIL import Image
from time import sleep
from pynput.mouse import Button, Controller as MController
from pynput.keyboard import Key, Controller as KController

# Constants not related to game
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
CUTOFF = 5 # Used when comparing images
WIDTH = 2560
HEIGHT = 1440
MIDDLEX = WIDTH/2
MIDDLEY = HEIGHT/2

# Constants related to game itself (the towers)
HERO_POS = (2300, 280)
DART_POS = (2420, 234)
BOOMERANG_POS = (2276, 469)
BOMB_POS = (2438, 468)
SUB_POS = (2280, 970)
SNIPER_POS = (2436, 806)
GO_POS = (2448, 1350)

# Constants related to the maps
TOTAL_EXPERT_MAPS = 10
MAPS = ['sanctuary', 'ravine', 'flooded', 'infernal', 'bloody', 'workshop', 'quad', 'dark', 'muddy', 'ouch']
MAP_POSITIONS = {
    'sanctuary': (718, 350),
    'ravine': (1286, 350),
    'flooded': (1846, 350),
    'infernal': (718, 770),
    'bloody': (1286, 770),
    'workshop': (1846, 770),

    'quad': (718, 350),
    'dark': (1286, 350),
    'muddy': (1846, 350),
    'ouch': (718, 770),
}
BONUS_REWARDS_PIXEL = (540, 308)
BONUS_RGB_CUTOFF = (240, 200, 0)
MONKEY_KNOWLEDGE_PIXEL = (255, 177)
MONKEY_KNOWLEDGE_RGB_CUTOFF = (140, 80, 200)

# Constants related to home screen
HOME_PLAY_BTN = (1108, 1242)
HOME_EXPERT_MAP_ICON = (1784, 1300)
HOME_EASY_MODE_ICON = (836, 548)
HOME_EASY_STANDARD_PLAY_ICON = (848, 776)
COLLECT_BTN = (1281, 903)
COLLECTION_BACK_BTN = (106, 70)

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
    sleep(1.5)
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

# After finishing a map, check if the collect button is on screen.
def get_collect_status():
    image = pyautogui.screenshot(region=(1104, 837, 354, 136))
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    cv2.imwrite("collect_status.png", image)

    current = imagehash.average_hash(Image.open('collect_status.png'))
    original = imagehash.average_hash(Image.open('collect_btn.png'))

    if current - original < CUTOFF:
        return True
    else:
        return False

# During each loop iteration, checks for certain colour pixels to see if player leveled up, and handles it by clicking.
def handle_level_up():
    screenshot = pyautogui.screenshot(region=(1045, 455, 490, 390))
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
    cv2.imwrite('level_up_check.png', screenshot)

    image = Image.open('level_up_check.png')
    colour = image.getpixel(MONKEY_KNOWLEDGE_PIXEL)

    # In this case, click on the middle of the screen to get rid of the monkey knowledge alert
    if colour[0] >= MONKEY_KNOWLEDGE_RGB_CUTOFF[0] and colour[1] >= MONKEY_KNOWLEDGE_RGB_CUTOFF[1] and colour[2] >= MONKEY_KNOWLEDGE_RGB_CUTOFF[2]:
        click(MIDDLEX, MIDDLEY)

# After confirming collect and pressing collect button, need to collect all rewards.
# Can many rewards, so click a lot of times from x = 0 -> 2560 with a decent step size.
def collect_rewards():
    for x in range(0, 2560, 30):
        click(x, 720)
    # Press collect button at the bottom
    click(1284, 1332)

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
        handle_level_up()
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
        handle_level_up()
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
                get_bomb()
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
        handle_level_up()
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
                click(MIDDLEX, MIDDLEY)

            elif current_round == 29:
                # Upgrade 2nd sub
                click(1338, 1045)
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
        handle_level_up()
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
        handle_level_up()
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
        handle_level_up()
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
        handle_level_up()
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
        handle_level_up()
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
        handle_level_up()
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
        handle_level_up()
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
                click(MIDDLEX, MIDDLEY)

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

# Basic 2d loop to screenshot each map, then compare each map to each of the screenshots of them with bonus rewards, and return the name of the map with the bonus rewards.
def check_bonus_rewards_map():
    mapCounter = 0
    startingX = 436
    startingY = 140
    screenshotWidth = 560
    screenshotHeight = 432

    # The maps are laid out in 2 rows, 3 columns, need to loop through each column, then each row
    for y in range(2):
        for x in range(3):
            # Screenshot the next map
            image = pyautogui.screenshot(region=(startingX + (x * 564), startingY + (y * 432), screenshotWidth, screenshotHeight))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite('maps/' + MAPS[mapCounter] + '.png', image)

            # Check if a yellowish colour (from the words 'bonus rewards') appears at a pixel in the picture. If so, this map is the bonus map.
            currentMap = Image.open('maps/' + MAPS[mapCounter] + '.png')
            pixels = [i for i in currentMap.getdata()]

            if (255, 220, 0) in pixels and pixels.count((255, 220, 0)) >= 150:
                return MAPS[mapCounter]

            mapCounter += 1

    # Reaching this point means I need to goto the next page of expert maps, so click on expert icon again
    click(1784, 1300)

    # Same as above 2d loop, but do early return since there are less than 6 maps here
    for y in range(2):
        for x in range(3):
            image = pyautogui.screenshot(region=(startingX + (x * 564), startingY + (y * 432), screenshotWidth, screenshotHeight))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite('maps/' + MAPS[mapCounter] + '.png', image)

            currentMap = Image.open('maps/' + MAPS[mapCounter] + '.png')
            pixels = [i for i in currentMap.getdata()]

            if (255, 220, 0) in pixels and pixels.count((255, 220, 0)) >= 150:
                return MAPS[mapCounter]

            mapCounter += 1

            # Currently, only 10 expert maps. If code scans 10 maps and no match, choose a map from the current screen.
            if mapCounter == TOTAL_EXPERT_MAPS:
                return MAPS[random.randint(7, TOTAL_EXPERT_MAPS - 1)]

# Used only to screenshot maps in debug mode, to save the one with the bonus rewards icon
def DEBUG_capture_maps():
    # The maps are laid out in 2 rows, 3 columns, need to loop through each column, then each row
    mapCounter = 0
    startingX = 436
    startingY = 140
    screenshotWidth = 560
    screenshotHeight = 432

    for y in range(2):
        for x in range(3):
            image = pyautogui.screenshot(region=(startingX + (x * 564), startingY + (y * 432), screenshotWidth, screenshotHeight))
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            cv2.imwrite('bonus_maps/' + str(MAPS[mapCounter]) + '.png', image)

            # Now, compare this image to the existing images in the project, to see which one has the bonus rewards.
            # TODO: maybe use opencv to see if 'bonus rewards' exists in the image? Each collection event has diff image for bonus rewards.
            #       Instead, do nothing for now without the collection event.
            mapCounter += 1

if __name__ == '__main__':
    looping = True

    # Clicks onto main screen since it will be on the terminal as soon as you run the script
    click(MIDDLEX, MIDDLEY)

    # image = Image.open('maps/flooded.png')
    # pixels = [i for i in image.getdata()]
    # print(pixels.count((255, 220, 0)))
    # exit(0)

    while looping:
        # On home screen, check if need to collect from collection event. Make sure to sleep first since there is a bit of delay going to home.
        sleep(3.0)
        collect_ready = get_collect_status()
        if (collect_ready):
            click(COLLECT_BTN[0], COLLECT_BTN[1])
            sleep(1.5)
            collect_rewards()

            # After collecting, press back button to go back to home screen
            click(COLLECTION_BACK_BTN[0], COLLECTION_BACK_BTN[1])

        # At this point, it is confirmed on home screen. Click in specific positions to goto expert maps.
        sleep(2.0)
        click(HOME_PLAY_BTN[0], HOME_PLAY_BTN[1])
        sleep(0.5)
        click(HOME_EXPERT_MAP_ICON[0], HOME_EXPERT_MAP_ICON[1])

        # Now, take a screenshot of each map and find the one with bonus rewards.
        bonusMap = check_bonus_rewards_map()

        # After finding which map it is, click on that map's position
        click(MAP_POSITIONS[bonusMap][0], MAP_POSITIONS[bonusMap][1])
        sleep(1)

        # Click on the easy mode icon, then the standard play button
        click(HOME_EASY_MODE_ICON[0], HOME_EASY_MODE_ICON[1])
        sleep(1)
        click(HOME_EASY_STANDARD_PLAY_ICON[0], HOME_EASY_STANDARD_PLAY_ICON[1])

        # This method of sleep is pretty unreliable, since I'm not sure if each map takes the same amount of time to load up or not.
        # Regardless, give a generous wait time.
        sleep(5)

        if bonusMap == 'sanctuary':
            sanctuary()
        elif bonusMap == 'ravine':
            ravine()
        elif bonusMap == 'flooded':
            flooded()
        elif bonusMap == 'infernal':
            infernal()
        elif bonusMap == 'bloody':
            bloody()
        elif bonusMap == 'workshop':
            workshop()
        elif bonusMap == 'quad':
            quad()
        elif bonusMap == 'dark':
            dark()
        elif bonusMap == 'muddy':
            muddy()
        elif bonusMap == 'ouch':
            ouch()

    # image = pyautogui.screenshot(region=(2364, 1278, 158, 151))
    # image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    # cv2.imwrite("round_status.png", image)

    # current = imagehash.average_hash(Image.open('round_status.png'))
    # original = imagehash.average_hash(Image.open('go_btn.png'))