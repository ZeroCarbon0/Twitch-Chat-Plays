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
    'reset': 'reset'
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
    'reload vehicle': 'f7',
    'horn': 'h',
}

Announcement = {
    'forward': ['GO FORWARD', 'DRIVE DRIVE DRIVE', 'GET us OUT OF HERE MARTY'],
    'back': ['GO BACK', 'BACK BACK BACK'],
    'left': ['GO LEFT', 'LEFT LEFT LEFT'],
    'right': ['GO RIGHT', 'RIGHT RIGHT RIGHT'],
    'left turn signal': ['SIGNAL LEFT', 'BMW DRIVER INCOMING'],
    'right turn signal': ['SIGNAL RIGHT', 'BMW DRIVER INCOMING'],
    'hazard lights': ['WE ARE A HAZARD', 'GET OUT OF THE WAYYYYY NOW'],
    'parking breaks': ['PARKING BREAKS', 'PARKING'],
    'reload vehicle': ['CALL THE MECHANIC', 'wRELOAD'],
    'horn': ['HEY', 'LOOK AT ME'],
    'reset': ['FLIP THE CAR', 'CALL THE PIT CREW', 'WHO BROKE THE CAR']
}

# State management for keys
active_forward = None  # To track forward/back state
active_left = None  # To track left/right state

# Release control for key press cancellation
forward_event = asyncio.Event()
left_event = asyncio.Event()

# Function to press a key for a specified time or until interrupted
async def press_key_with_event(key, event, delay):
    pyautogui.keyDown(key)
    try:
        await asyncio.wait_for(event.wait(), delay)
    except asyncio.TimeoutError:
        pass  # The delay finished, so we release the key
    finally:
        pyautogui.keyUp(key)
        event.clear()  # Reset the event for future uses

async def press_key_once(key):
        pyautogui.keyDown(key)
        await asyncio.sleep(5)
        pyautogui.keyDown(key)

# Join channel
async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)

# Read message and take action
async def on_message(msg: ChatMessage):
    global active_forward, active_left

    print(f'{msg.user.name}: {msg.text}')
    chat_message = msg.text.lower()

    # Handle forward/backward commands
    if 'forward' in chat_message:
        if active_forward:
            forward_event.set()  # Stop the current forward movement
        active_forward = 'forward'
        forward_event.clear()  # Reset the event for a new 10-second timer
        message = random.choice(Announcement['forward'])
        tts.speak_message(message)
        asyncio.create_task(press_key_with_event(KEY_TO_PRESS['forward'], forward_event, 10))

    elif 'back' in chat_message:
        if active_forward:
            forward_event.set()  # Stop the current forward or backward movement
        active_forward = 'back'
        forward_event.clear()  # Reset the event for a new 10-second timer
        message = random.choice(Announcement['back'])
        tts.speak_message(message)
        asyncio.create_task(press_key_with_event(KEY_TO_PRESS['back'], forward_event, 10))

    # Handle left/right commands
    elif 'left' in chat_message:
        if active_left:
            left_event.set()  # Stop the current left movement
        active_left = 'left'
        left_event.clear()  # Reset the event for a new 10-second timer
        message = random.choice(Announcement['left'])
        tts.speak_message(message)
        asyncio.create_task(press_key_with_event(KEY_TO_PRESS['left'], left_event, 10))

    elif 'right' in chat_message:
        if active_left:
            left_event.set()  # Stop the current left or right movement
        active_left = 'right'
        left_event.clear()  # Reset the event for a new 10-second timer
        message = random.choice(Announcement['right'])
        tts.speak_message(message)
        asyncio.create_task(press_key_with_event(KEY_TO_PRESS['right'], left_event, 10))

    elif 'horn' in chat_message:
        message = random.choice(Announcement['horn'])
        tts.speak_message(message)
        await press_key_once(KEY_TO_PRESS['horn'])

    elif 'reload vehicle' in chat_message:
        message = random.choice(Announcement['reload vehicle'])
        tts.speak_message(message)
        await press_key_once(KEY_TO_PRESS['reload vehicle'])

    elif 'parking breaks' in chat_message:
        message = random.choice(Announcement['parking breaks'])
        tts.speak_message(message)
        await press_key_once(KEY_TO_PRESS['parking breaks'])

    elif 'hazard lights' in chat_message:
        message = random.choice(Announcement['hazard lights'])
        tts.speak_message(message)
        await press_key_once(KEY_TO_PRESS['hazard lights'])
    
    #else:
        #message = f"{msg.text}"
        #tts.speak_message(message)

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