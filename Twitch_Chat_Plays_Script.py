from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatEvent
import asyncio
import pyautogui
from cred import APP_ID, APP_SECRET
import tts
import time
import random


TARGET_CHANNEL = 'Zerocarbon0'
SCOPES = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

#State Variables
SEQUENCE = {
    'forward': 'forward',
    'back': 'back',
    'left': 'left',
    'right': 'right',
    'left turn signal': 'left turn signal',
    'right turn signal': 'right turn signal',
    'hazard lights': 'hazard lights',
    'parking breaks': 'parking breaks',
    'reload vehicle': 'reload vehicle',
    'horn': 'horn',
}

KEY_TO_PRESS = {
    'forward': 'w',
    'back': 's',
    'left': 'a',
    'right': 'd',
    'left turn signal': ',',
    'right turn signal': '.',
    'hazard lights': '/',
    'parking breaks': 'space',
    'reload vehicle': 'ctrl + m',
    'horn': 'h',
}

Announcement = {
    'forward': ['GO FORWARD', 'DRIVE DRIVE DRIVE', 'GET US OUT OF HERE MARTY!!'],
    'back': ['GO BACK', 'BACK BACK BACK'],
    'left': ['GO LEFT', 'LEFT LEFT LEFT'],
    'right': ['GO RIGHT', 'RIGHT RIGHT RIGHT'],
    'left turn signal': ['SIGNAL LEFT', 'BMW DRIVER INCOMING'],
    'right turn signal': ['SIGNAL RIGHT', 'BMW DRIVER INCOMING'],
    'hazard lights': ['WE ARE A HAZARD', 'GET OUT OF THE WAYYYYY NOW'],
    'parking breaks': ['PARKING BREAKS', 'PARKING'],
    'reload vehicle': ['CALL THE MECHANIC', 'wRELOAD'],
    'horn': ['HEY', 'LOOK AT ME'],
}

#hold the key
async def press_key_with_delay(key, delay):
    pyautogui.keyDown(key)
    await asyncio.sleep(delay)
    pyautogui.keyUp(key)

#join channel
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)

#read message
#if it is one of the keywords(W) forward(S), backwards(A), left(A), right(D), left turn signal(,), right turn signal(.), hazard lights(/), parking breaks(space), reload vehicle(ctrl + R))
async def on_message(msg: ChatMessage):
    print(f'{msg.user.name}: {msg.text}')
    chat_message = msg.text.lower()

    for direction, sequence in SEQUENCE.items():
        if sequence in chat_message:
            await press_key_with_delay(KEY_TO_PRESS[direction], 10)
            #time.sleep(10)
            message = random.choice(Announcement[direction])
            tts.speak_message(message)
        else:
            continue

async def run():
    
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, SCOPES)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, SCOPES, refresh_token)
    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()


asyncio.run(run())



# should release the last press key when new key is pressed