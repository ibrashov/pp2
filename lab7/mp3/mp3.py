import pygame
import os

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("🎵 MP3 Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (30, 144, 255)

font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 28)

music_folder = "lab7/mp3"

songs = [
    os.path.join(music_folder, "crazy.mp3"),
    os.path.join(music_folder, "feel.mp3"),
    os.path.join(music_folder, "ma.mp3")
]

current_index = 0
is_playing = False

def play_song():
    global is_playing
    pygame.mixer.music.load(songs[current_index])
    pygame.mixer.music.play()
    is_playing = True

def next_song():
    global current_index
    current_index = (current_index + 1) % len(songs)
    play_song()

def previous_song():
    global current_index
    current_index = (current_index - 1) % len(songs)
    play_song()

def toggle_pause():
    global is_playing
    if is_playing:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()
    is_playing = not is_playing

def stop_music():
    pygame.mixer.music.stop()

def draw_screen():
    screen.fill(WHITE)

    if songs:
        song_text = f"Now Playing: {os.path.basename(songs[current_index])}"
    else:
        song_text = "No MP3 files found"

    text_surface = font.render(song_text, True, BLACK)
    screen.blit(text_surface, (20, 50))

    instructions = [
        "Controls:",
        "SPACE - Play / Pause",
        "RIGHT ARROW - Next Song",
        "LEFT ARROW - Previous Song",
        "S - Stop",
        "ESC - Exit"
    ]

    y = 150
    for line in instructions:
        text_surface = small_font.render(line, True, BLUE)
        screen.blit(text_surface, (20, y))
        y += 40

    pygame.display.flip()

play_song()

running = True
while running:
    draw_screen()
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                toggle_pause()
            elif event.key == pygame.K_RIGHT:
                next_song()
            elif event.key == pygame.K_LEFT:
                previous_song()
            elif event.key == pygame.K_s:
                stop_music()

pygame.quit()
