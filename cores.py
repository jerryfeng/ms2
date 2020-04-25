import pyautogui
import time
from keyboard import PressKey, ReleaseKey, SCAN_CODE

width, height = pyautogui.size()
on = False
ATTACK_BUTTON = SCAN_CODE.E.value
MOUNT_BUTTON = SCAN_CODE.EIGHT.value
MOUNT2_BUTTON = SCAN_CODE.SEVEN.value
SHIELD_BUTTON = SCAN_CODE.F.value

CYCLE_INTERVAL = 37
tick = 0 # .1 sec per tick

while True:
    pos = pyautogui.position()
    if pos == (0,0):
        print('--Start botting--')
        tick = 0
        on = True
        currentStateIndex = 0
        time.sleep(2)
    elif pos == (width - 1, 0):
        print('--End botting--')
        tick = 0
        on = False
        time.sleep(2)
    elif pos == (width - 1, height - 1):
        print('Program exits normally')
        quit()

    if on and tick % (CYCLE_INTERVAL * 10) == 0:
            PressKey(MOUNT2_BUTTON)
            time.sleep(0.2)
            ReleaseKey(MOUNT2_BUTTON)
            time.sleep(1)
            PressKey(MOUNT_BUTTON)
            time.sleep(0.2)
            ReleaseKey(MOUNT_BUTTON)
            time.sleep(1)

            # drop from air mount
            PressKey(MOUNT_BUTTON)
            time.sleep(0.2)
            ReleaseKey(MOUNT_BUTTON)
            # take damage from falling
            time.sleep(4)
            # wildfire
            PressKey(ATTACK_BUTTON)
            time.sleep(0.2)
            ReleaseKey(ATTACK_BUTTON)
            # rise back to sky
            time.sleep(2)
            PressKey(MOUNT_BUTTON)
            time.sleep(0.2)
            ReleaseKey(MOUNT_BUTTON)
    tick+=1
    time.sleep(0.1)
