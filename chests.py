import pyautogui
import time
from keyboard import PressKey, ReleaseKey, SCAN_CODE, PressKeys, ReleaseKeys
import queue

moveNextChannelTyped = False;
actionQueue = queue.Queue()
width, height = pyautogui.size()
on = False
currentState = None
spawnPoint = ''
MOUNT_BUTTON = SCAN_CODE.EIGHT.value
CRAWL_BUTTON = SCAN_CODE.PERIOD.value
BOW_BUTTON = SCAN_CODE.F2.value
chestEmpty = False
gameResolution = None

def PressReleaseKey(key):
    PressKey(key);
    time.sleep(0.2)
    ReleaseKey(key)

def PressReleaseKeys(keys):
    for key in keys:
        PressReleaseKey(key)

def matchGameResolution():
    for resolution in [720, 1080, 1440, 2160]:
        found = pyautogui.locateOnScreen(f'KidelCrossingLeftSpawn{resolution}p.png', confidence = 0.9)
        if found:
            return resolution
    print('Error: unable to detect game resolution')
    quit()

def checkSpawnPoint():
    global spawnPoint
    found = pyautogui.locateOnScreen(f'KidelCrossingLeftSpawn{gameResolution}p.png', confidence = 0.8)
    spawnPoint = 'LEFT' if found else 'RIGHT'

def checkChestEmpty():
    global chestEmpty
    found = pyautogui.locateOnScreen(f'KidelCrossingChestEmpty{gameResolution}p.png', confidence = 0.8)
    chestEmpty = True if found else False

def queueAction(action, *params):
    actionQueue.put((action, *params))

# this function queue no-op actions so that program can sleep while still able
# to detect commands that start / stop the script
def nop():
    pass
def wait(tick):
    for i in range(tick):
        queueAction(nop)

def moveNextChannel():
    global moveNextChannelTyped
    queueAction(PressReleaseKey, SCAN_CODE.RETURN.value)
    wait(5)
    if not moveNextChannelTyped:
        # type: /moveNextChannel
        moveNextChannelKeys = [
            SCAN_CODE.SLASH.value,
            SCAN_CODE.M.value,
            SCAN_CODE.O.value,
            SCAN_CODE.V.value,
            SCAN_CODE.E.value,
            SCAN_CODE.N.value,
            SCAN_CODE.E.value,
            SCAN_CODE.X.value,
            SCAN_CODE.T.value,
            SCAN_CODE.C.value,
            SCAN_CODE.H.value,
            SCAN_CODE.A.value,
            SCAN_CODE.N.value,
            SCAN_CODE.N.value,
            SCAN_CODE.E.value,
            SCAN_CODE.L.value,
        ]
        queueAction(PressReleaseKeys, moveNextChannelKeys)

        moveNextChannelTyped = True
    else:
        queueAction(PressReleaseKey, SCAN_CODE.UP.value)
    wait(5)
    queueAction(PressReleaseKey, SCAN_CODE.RETURN.value)
    # allow 10 seconds to change channel
    wait(100)

def leftPath():
    queueAction(PressReleaseKey, MOUNT_BUTTON)
    wait(10)
    queueAction(PressKey, SCAN_CODE.UP.value)
    wait(45)
    queueAction(PressKey, SCAN_CODE.RIGHT.value)
    wait(28)
    queueAction(ReleaseKeys, [SCAN_CODE.RIGHT.value, SCAN_CODE.UP.value])
    wait(2)
    queueAction(PressReleaseKey, MOUNT_BUTTON)
    wait(25)

def rightPath():
    queueAction(PressReleaseKey, MOUNT_BUTTON)
    queueAction(PressKey, SCAN_CODE.LEFT.value)
    wait(48)
    queueAction(PressKey, SCAN_CODE.DOWN.value)
    wait(46)
    queueAction(ReleaseKeys, [SCAN_CODE.LEFT.value, SCAN_CODE.DOWN.value])
    wait(2)
    queueAction(PressReleaseKey, MOUNT_BUTTON)
    wait(25)

def walkTowardsPoing():
    queueAction(PressKeys, [SCAN_CODE.LEFT.value, SCAN_CODE.UP.value])
    wait(6)
    queueAction(ReleaseKeys, [SCAN_CODE.LEFT.value, SCAN_CODE.UP.value])

def interactWithPoing():
    queueAction(PressReleaseKey, SCAN_CODE.SPACE.value)
    wait(5)
    queueAction(PressReleaseKey, SCAN_CODE.SPACE.value)
    wait(25)
    queueAction(PressReleaseKey, BOW_BUTTON)
    wait(5)
    queueAction(PressKeys, [CRAWL_BUTTON, SCAN_CODE.UP.value])
    wait(80)
    queueAction(ReleaseKeys, [CRAWL_BUTTON, SCAN_CODE.UP.value])

def openChest():
    queueAction(PressKey, SCAN_CODE.UP.value)
    wait(25)
    queueAction(ReleaseKey, SCAN_CODE.UP.value)
    queueAction(PressKey, SCAN_CODE.DOWN.value)
    wait(3)
    queueAction(ReleaseKey, SCAN_CODE.DOWN.value)
    queueAction(PressReleaseKey, SCAN_CODE.SPACE.value)
    wait(2)
    queueAction(PressReleaseKey, SCAN_CODE.SPACE.value)
    wait(15)

def getNextState():
    # how I wish there's switch statement in python
    if currentState == 'initial':
        if HEAL_BUTTON:
            queueAction(PressReleaseKey, HEAL_BUTTON)
            wait(3)
        queueAction(checkSpawnPoint)
        return 'checking spawn point'
    elif currentState == 'checking spawn point':
        if spawnPoint == 'LEFT':
            leftPath()
            return 'left path'
        else:
            rightPath()
            return 'right path'
    elif currentState == 'left path' or currentState == 'right path':
        queueAction(checkChestEmpty)
        return 'checking chest empty'
    elif currentState == 'checking chest empty':
        if chestEmpty:
            moveNextChannel()
            return 'changing channel'
        else:
            walkTowardsPoing()
            return 'walking towards poing'
    elif currentState == 'walking towards poing':
        interactWithPoing()
        return 'interacting with poing'
    elif currentState == 'interacting with poing':
        openChest()
        return 'opening chest'
    elif currentState == 'opening chest':
        moveNextChannel()
        return 'changing channel'
    elif currentState == 'changing channel':
        return 'initial'


tick = 0 # 10 ticks per second
while True:
    pos = pyautogui.position()
    if pos == (0,0):
        print('--Start botting--')
        on = True
        currentState = 'initial'
        if not gameResolution:
            gameResolution = matchGameResolution();
            print(f'game resolution detected: {gameResolution}p')
        time.sleep(1)
    elif pos == (width - 1, 0):
        print('\n--End botting--')
        on = False
        actionQueue = queue.Queue()
        time.sleep(1)
    elif pos == (width - 1, height - 1):
        print('\nProgram exits normally')
        quit()

    if on:
        if actionQueue.empty():
            currentState = getNextState()
            print(f'\rcurrent state: {currentState:30} ', end="")
        else:
            action, *params = actionQueue.get()
            action(*params)
    tick += 1
    time.sleep(0.1)
