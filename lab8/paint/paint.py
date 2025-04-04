import pygame

# Initialize pygame
pygame.init()

# Set screen width and height
WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create window with given dimensions

# Define colors using RGB values
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)

# List of selectable drawing colors
colors = [colorRED, colorGREEN, colorBLUE]

# Available figures to draw
figures = ["square", "circle", "triangle"]

# Default drawing color and shape
current_color = colorWHITE
current_figure = "circle"

# Mouse button flags
LMBpressed = False  # Left Mouse Button
RMBpressed = False  # Right Mouse Button

# Default size of shapes
SIZE = 10

# Fill screen with white color initially
screen.fill(colorWHITE)

# Create font object for drawing text
font = pygame.font.SysFont("Verdana", 24)

# Main program loop flag
running = True

# Start of main event loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Quit the loop if window is closed

        # Mouse button pressed events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LMBpressed = True  # Left mouse button pressed
            elif event.button == 3:
                RMBpressed = True  # Right mouse button pressed

        # Mouse button released events
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                LMBpressed = False
            elif event.button == 3:
                RMBpressed = False

        # Keyboard events for changing size
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:  # "+" key
                SIZE += 1  # Increase shape size
            elif event.key == pygame.K_MINUS:
                SIZE = max(1, SIZE - 1)  # Decrease size, but not below 1

    # Draw color selection buttons at top left
    color_boxes = []
    for i, col in enumerate(colors):
        rect = pygame.draw.rect(screen, col, (i * 40, 0, 40, 40))
        color_boxes.append((rect, col))  # Store box and its color

    # Draw selection shapes (icons) on top bar
    square_rect = pygame.draw.rect(screen, colorBLACK, (130, 0, 40, 40), 3)
    circle_rect = pygame.draw.circle(screen, colorBLACK, (197, 20), 23, 3)
    triangle_rect = pygame.draw.polygon(screen, colorBLACK, ((230, 0), (230, 40), (270, 40)), 3)

    # Draw eraser label on top right
    pygame.draw.rect(screen, colorWHITE, (300, 0, 200, 40))  # Background for text
    eraser_label = font.render("RMB: Eraser", True, colorBLACK)  # Create text surface
    screen.blit(eraser_label, (300, 10))  # Draw text on screen

    # Get mouse position and button states
    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    # Check if a color or shape button is clicked
    if click[0]:  # Left click
        for rect, col in color_boxes:
            if rect.collidepoint(pos):
                current_color = col  # Change current drawing color

        if square_rect.collidepoint(pos):
            current_figure = "square"  # Select square
        elif circle_rect.collidepoint(pos):
            current_figure = "circle"  # Select circle
        elif triangle_rect.collidepoint(pos):
            current_figure = "triangle"  # Select triangle

    # Free-hand drawing with mouse
    if LMBpressed or RMBpressed:
        draw_color = colorWHITE if RMBpressed else current_color  # Use white if erasing

        # Draw selected shape at mouse position
        if current_figure == "circle":
            pygame.draw.circle(screen, draw_color, pos, SIZE)
        elif current_figure == "square":
            pygame.draw.rect(screen, draw_color, (pos[0], pos[1], SIZE, SIZE))
        elif current_figure == "triangle":
            pygame.draw.polygon(screen, draw_color, [
                (pos[0], pos[1]),
                (pos[0] - SIZE, pos[1] + SIZE),
                (pos[0] + SIZE, pos[1] + SIZE)
            ])

    # Update the display with all changes
    pygame.display.flip()

# Quit pygame when loop ends
pygame.quit()
