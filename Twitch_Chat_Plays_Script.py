from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat, ChatEvent
import asyncio
import pyautogui
from cred import APP_ID, APP_SECRET
import tts
import re
from pynput import keyboard

KEYWORDS = {
    'left': 'a',
    'right': 'd',
    'shoot': 'space',
    'aim left': 'left',
    'aim right': 'right',
    'less power': 'down',
    'more power': 'up',
    'up weapon': 'w',
    'down weapon': 's',
}

# Global variable to track bot's enabled state
enabled = True

# Keyboard listener to toggle the bot
def on_press(key):
    global enabled
    try:
        if key.char == '=':
            enabled = not enabled
            print(f"Bot {'enabled' if enabled else 'disabled'}")
    except AttributeError:
        pass

listener = keyboard.Listener(on_press=on_press)
listener.start()

async def on_message(msg):
    if not enabled:
        return

    print(f'{msg.user.name}: {msg.text}')
    chat_message = msg.text.lower().strip()

    tokens = chat_message.split()
    if not tokens:
        return

    # Check if the last token is a number (the count or duration)
    if tokens[-1].isdigit():
        times = int(tokens.pop())
    else:
        times = 1

    # Reconstruct the command from the remaining tokens
    command = ' '.join(tokens)

    if command in KEYWORDS:
        key = KEYWORDS[command]

        if command in ['left', 'right']:
            # For 'left' and 'right', hold down the key for 'times' seconds
            print(f"Holding key '{key}' for {times} seconds")
            await asyncio.to_thread(pyautogui.keyDown, key)
            await asyncio.sleep(times)
            await asyncio.to_thread(pyautogui.keyUp, key)
        else:
            # For other commands, press the key 'times' times
            print(f"Pressing key '{key}' {times} times")
            for _ in range(times):
                await asyncio.to_thread(pyautogui.press, key)
                await asyncio.sleep(0.1)  # Small delay between key presses
    else:
        print(f"Unknown command: {command}")

TARGET_CHANNEL = 'Zerocarbon0'
SCOPES = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

async def on_ready(ready_event):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def main(twitch):
    # Run tts.speak_message in a separate thread to prevent blocking
    await asyncio.to_thread(tts.speak_message, "Let's PLAY SHELLSHOCK")

    chat = await Chat(twitch)
    chat.register_event(ChatEvent.READY, on_ready)
    chat.register_event(ChatEvent.MESSAGE, on_message)
    chat.start()

    # Keep the event loop running
    while True:
        await asyncio.sleep(1)

async def launch():
    twitch = await Twitch(APP_ID, APP_SECRET)
    auth = UserAuthenticator(twitch, SCOPES)
    token, refresh_token = await auth.authenticate()
    await twitch.set_user_authentication(token, SCOPES, refresh_token)
    await main(twitch)

# Start the bot
asyncio.run(launch())

