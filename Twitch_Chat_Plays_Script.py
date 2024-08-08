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


TARGET_CHANNEL = 'Zerocarbon0'
SCOPES = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

#State Variables
SEQUENCE = {
    'blue': ['b', 'l', 'u', 'e'],
    'green': ['g', 'r', 'e', 'e', 'n'],
    'red': ['r', 'e', 'd'],
    'yellow': ['y', 'e', 'l', 'l', 'o', 'w']
}

current_indices = {
    'blue': 0,
    'green': 0,
    'red': 0, 
    'yellow': 0
}

KEY_TO_PRESS = {
    'blue': '1',
    'green': '2',
    'red': '3', 
    'yellow': '4'
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
            print(current_indices)
            if current_indices[color] == len(sequence):
                pyautogui.press(KEY_TO_PRESS[color])
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

    