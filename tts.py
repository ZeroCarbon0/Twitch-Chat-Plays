import os
from gtts import gTTS
import pygame
import time
import tempfile  # Use tempfile for unique file names

def speak_message(message):
    # Create a unique temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as tmp_file:
        output_path = tmp_file.name  # Get the unique temp file path

    # Generate the speech audio
    tts = gTTS(text=message, lang='en')
    tts.save(output_path)

    # Initialize pygame mixer and play the sound
    pygame.mixer.init()
    pygame.mixer.music.load(output_path)
    pygame.mixer.music.play()

    # Wait for the playback to complete
    while pygame.mixer.music.get_busy():
        time.sleep(0.1)

    # Stop the mixer and cleanup
    pygame.mixer.music.stop()
    pygame.mixer.quit()

    # Small delay to ensure file is fully released before deletion
    time.sleep(0.5)

    # Delete the temporary file
    try:
        os.remove(output_path)
    except OSError as e:
        print(f"Error deleting file {output_path}: {e}")

# Example usage
# speak_message('Hello World') # Uncomment for testing

