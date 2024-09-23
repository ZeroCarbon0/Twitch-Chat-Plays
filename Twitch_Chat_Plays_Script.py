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
    'light': 'light',
    'brake': 'brake',
    'reset': 'reset',
    'restart': 'restart',
    'horn': 'horn',
    'reset': 'reset'
}

KEY_TO_PRESS = {
    'forward': 'w',
    'back': 's',
    'left turn signal': ',',
    'right turn signal': '.',
    'left': 'a',
    'right': 'd',
    'light': '/',
    'brake': 'p',
    'reset': 'f7',
    'restart': 'r',
    'horn': 'h',
}

Announcement = {
    'forward': ['GO FORWARD', 'DRIVE DRIVE DRIVE', 'GET us OUT OF HERE MARTY'],
    'back': ['GO BACK', 'BACK BACK BACK'],
    'left': ['GO LEFT', 'LEFT LEFT LEFT'],
    'right': ['GO RIGHT', 'RIGHT RIGHT RIGHT'],
    'left turn signal': ['SIGNAL LEFT', 'BMW DRIVER INCOMING'],
    'right turn signal': ['SIGNAL RIGHT', 'BMW DRIVER INCOMING'],
    'light': ['WE ARE A HAZARD', 'GET OUT OF THE WAY NOW'],
    'brake': ['brake', 'PARKING'],
    'reset': ['CALL THE MECHANIC', 'RELOAD','FLIP THE CAR', 'CALL THE PIT CREW', 'WHO BROKE THE CAR'],
    'restart': ['RESTARTING', "Chat can't drive"],
    'horn': ['HEY', 'LOOK AT ME']
}

async def press_key_with_event(key, event, delay):
    pyautogui.keyDown(key)
    try:
        await asyncio.wait_for(event.wait(), delay)
    except asyncio.TimeoutError:
        pass
    finally:
        pyautogui.keyUp(key)
        event.clear()


async def press_key_once(key):
    pyautogui.keyDown(key)
    await asyncio.sleep(2)
    pyautogui.keyUp(key)


# Join channel
async def on_ready(ready_event):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)


# Read message and take action
def create_message_handler(forward_event, left_event):
    async def on_message(msg):
        print(f'{msg.user.name}: {msg.text}')
        chat_message = msg.text.lower()

        if 'forward' in chat_message:
            forward_event.clear()  # Reset the event for a new 10-second timer
            message = random.choice(Announcement['forward'])
            #tts.speak_message(message)  # Assuming tts is a text-to-speech function
            asyncio.create_task(press_key_with_event(KEY_TO_PRESS['forward'], forward_event, 10))

        elif 'back' in chat_message:
            forward_event.clear()  # Reset the event for a new 10-second timer
            message = random.choice(Announcement['back'])
            #tts.speak_message(message)
            asyncio.create_task(press_key_with_event(KEY_TO_PRESS['back'], forward_event, 10))

        elif 'left turn signal' in chat_message:
            message = random.choice(Announcement['left turn signal'])
            #tts.speak_message(message)
            await press_key_once(KEY_TO_PRESS['left turn signal'])

        elif 'right turn signal' in chat_message:
            message = random.choice(Announcement['right turn signal'])
            #tts.speak_message(message)
            await press_key_once(KEY_TO_PRESS['right turn signal'])

        elif 'left' in chat_message:
            left_event.clear()  # Reset the event for a new 10-second timer
            message = random.choice(Announcement['left'])
            #tts.speak_message(message)
            asyncio.create_task(press_key_with_event(KEY_TO_PRESS['left'], left_event, 10))

        elif 'right' in chat_message:
            left_event.clear()  # Reset the event for a new 10-second timer
            message = random.choice(Announcement['right'])
            #tts.speak_message(message)
            asyncio.create_task(press_key_with_event(KEY_TO_PRESS['right'], left_event, 10))

        elif 'horn' in chat_message:
            message = random.choice(Announcement['horn'])
            tts.speak_message(message)
            await press_key_once(KEY_TO_PRESS['horn'])

        #elif 'reset' in chat_message:
        #    message = random.choice(Announcement['reset'])
        #    #tts.speak_message(message)
        #,dp    await press_key_once(KEY_TO_PRESS['reset'])

        #elif 'start' in chat_message:
        #    message = random.choice(Announcement['restart'])
        #    #tts.speak_message(message)
        #    await press_key_once(KEY_TO_PRESS['restart'])

        elif 'brake' in chat_message:
            message = random.choice(Announcement['brake'])
            #tts.speak_message(message)
            await press_key_once(KEY_TO_PRESS['brake'])

        elif 'light' in chat_message:
            message = random.choice(Announcement['light'])
            #tts.speak_message(message)
            await press_key_once(KEY_TO_PRESS['light'])

    return on_message


async def main(twitch):
    tts.speak_message("It's Chats Turn!")

    # Create new events in the correct event loop
    forward_event = asyncio.Event()
    left_event = asyncio.Event()

    # Set up chat and register events
    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, create_message_handler(forward_event, left_event))
    chat.start()

    # Run the bot for 10 seconds
    await asyncio.sleep(1200)

    tts.speak_message("IT's OVER!")
    chat.stop()


async def periodic_runner():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, SCOPES)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, SCOPES, refresh_token)

    while True:
        await main(twitch)
        print("Waiting 5 minutes")
        await asyncio.sleep(0)  # Sleep for 5 minutes


# Start the periodic runner
asyncio.run(periodic_runner())