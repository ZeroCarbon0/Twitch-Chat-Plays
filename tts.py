import os
from gtts import gTTS
import pygame
import time

def speak_message(message, output_path="output.mp3"):
    tts = gTTS(text=message, lang='en')
    tts.save(output_path)
    
    pygame.mixer.init()
    pygame.mixer.music.load(output_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        time.sleep(0.1)
    
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    os.remove(output_path)

speak_message('Hello World')