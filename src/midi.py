import mido
import pygame
import pygame.midi
import time

def play_chord(notes, duration=1):
    # Initialize Pygame MIDI
    pygame.init()
    pygame.midi.init()
    
    # Open a MIDI output
    port = pygame.midi.Output(pygame.midi.get_default_output_id())
    
    # Set instrument to acoustic grand piano (MIDI program 0)
    port.set_instrument(0)
    
    # Start playing each note in the chord
    for note in notes:
        port.note_on(note, velocity=100)  # note on with velocity 100
    
    # Let the chord play for the duration specified
    time.sleep(duration)
    
    # Stop playing each note
    for note in notes:
        port.note_off(note, velocity=100)  # note off with velocity 100
    
    # Close the MIDI port and quit pygame
    port.close()
    pygame.midi.quit()
    pygame.quit()

# Example usage: Play a C major chord
play_chord([60, 64, 67, 72])