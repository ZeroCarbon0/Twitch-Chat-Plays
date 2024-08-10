''' Twitch Chat Plays
Python code with the goal of letting twitch chat type message and then interact with my computer, stream, or game. 
KEEP IT SIMPLE STUPID'''

""" 
Commands to update githud
E:
CD FILEPATH
git status
git add.
git coommit -m "NAME FOR GITHUB" 
git push origin main
"""

# connect to twitch chat


from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.type import AuthScope
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatEvent
import asyncio
import pyautogui
from cred import APP_ID, APP_SECRET
import tts
import time


TARGET_CHANNEL = 'Zerocarbon0'
SCOPES = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]


#State Variables
SEQUENCE = {
    'grey': ['g', 'r', 'e', 'y'],
    'white': ['w', 'h', 'i', 't', 'e'],
    'blue': ['b', 'l', 'u', 'e'],
    'red': ['r', 'e', 'd'],
    'green': ['g', 'r', 'e', 'e', 'n'],
    'black': ['b', 'l', 'a', 'c', 'k'],
    'ore': ['o', 'r', 'e'],
    'brown': ['b', 'r', 'o', 'w', 'n'],
    'uno': ['u', 'n', 'o']
}

current_indices = {
    'grey': 0,
    'white': 0,
    'blue': 0,
    'red': 0,
    'green': 0,
    'black': 0,
    'ore': 0,
    'brown': 0,
    'uno': 0
}

KEY_TO_PRESS = {
    'grey': 'f13',
    'white': 'f14',
    'blue': 'f15',
    'red': 'o',
    'green': 'f17',
    'black': 'f18',
    'ore': 'f19',
    'brown': 'f20',
    'uno': 'f21'
}

Announcement = {
    'grey': 'Twitch Chat Typed Grey',
    'white': 'Twitch Chat Typed White',
    'blue': 'Twitch Chat Typed Blue',
    'red': 'Twitch Chat Typed Red',
    'green': 'Twitch Chat Typed Green',
    'black': 'Twitch Chat Typed Black',
    'ore': 'Twitch Chat Typed Ore',
    'brown': 'Twitch Chat Typed Brown',
    'uno': 'Twitch Chat Typed Uno'
}

async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def on_message(msg: ChatMessage):
    global current_indices
    print(f'{msg.user.name}: {msg.text}')
    chat_message = msg.text.lower()

    for color, sequence in SEQUENCE.items():
        expected_letter = sequence[current_indices[color]]
        if expected_letter in chat_message:
            current_indices[color] += 1
            if current_indices[color] == len(sequence):
                pyautogui.keyDown(KEY_TO_PRESS[color])
                time.sleep(.01)
                pyautogui.keyUp(KEY_TO_PRESS[color])
                message = Announcement[color]
                tts.speak_message(message)
                current_indices[color] = 0
        else:
            current_indices[color] = 0
            

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