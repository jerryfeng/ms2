import pyautogui
import time
from keyboard import PressKey, ReleaseKey, SCAN_CODE

FISH_INTERVAL = 7
BAIT_INTERVAL = 10000

width, height = pyautogui.size()

tick = 0
on = False

while True:
    pos = pyautogui.position()
    if pos == (0,0):
        print('--Start botting--')
        on = True
        time.sleep(2)
    elif pos == (width - 1, 0):
        print('--Pause botting--')
        on = False
        time.sleep(2)
    elif pos == (width - 1, height - 1):
        print('Program exits normally')
        quit()

    if on:
        if tick % FISH_INTERVAL == 0:
            # press space
            PressKey(SCAN_CODE.SPACE.value)
            time.sleep(0.2)
            ReleaseKey(SCAN_CODE.SPACE.value)
        if tick % BAIT_INTERVAL == 0:
            time.sleep(4)
            PressKey(SCAN_CODE.SIX.value)
            time.sleep(0.2)
            ReleaseKey(SCAN_CODE.SIX.value)
        tick += 1
    time.sleep(0.1)
