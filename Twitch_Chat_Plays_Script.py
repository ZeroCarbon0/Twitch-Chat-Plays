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
from cred import APP_ID, APP_SECRET

TARGET_CHANNEL = 'Zerocarbon0'
SCOPES = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

async def on_ready(ready_event: EventData):
    print('Bot is ready for work, joining channels')
    await ready_event.chat.join_room(TARGET_CHANNEL)

async def on_message(msg: ChatMessage):
    print(f'{msg.user.name}: {msg.text}')

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

    