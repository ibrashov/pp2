import pygame

# Initialize pygame
pygame.init()

# Set screen width and height
WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Define colors using RGB values
colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)

# List of selectable drawing colors
colors = [colorRED, colorGREEN, colorBLUE]

# Available figures to draw
figures = ["square", "circle", "rectangle", "right_triangle", "equilateral_triangle", "rhombus"]

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
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                LMBpressed = True
            elif event.button == 3:
                RMBpressed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                LMBpressed = False
            elif event.button == 3:
                RMBpressed = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_EQUALS:
                SIZE += 1
            elif event.key == pygame.K_MINUS:
                SIZE = max(1, SIZE - 1)

    # Draw color selection buttons
    color_boxes = []
    for i, col in enumerate(colors):
        rect = pygame.draw.rect(screen, col, (i * 40, 0, 40, 40))
        color_boxes.append((rect, col))

    # Draw shape selection buttons
    square_rect = pygame.draw.rect(screen, colorBLACK, (130, 0, 40, 40), 3)
    circle_rect = pygame.draw.circle(screen, colorBLACK, (197, 20), 23, 3)
    rectangle_rect = pygame.draw.rect(screen, colorBLACK, (230, 10, 50, 25), 3)
    right_triangle_rect = pygame.draw.polygon(screen, colorBLACK, [(290, 0), (290, 40), (330, 40)], 3)
    equilateral_triangle_rect = pygame.draw.polygon(screen, colorBLACK, [(340, 40), (360, 0), (380, 40)], 3)
    rhombus_rect = pygame.draw.polygon(screen, colorBLACK, [(390, 20), (410, 0), (430, 20), (410, 40)], 3)

    # Eraser label
    pygame.draw.rect(screen, colorWHITE, (440, 0, 400, 40))
    eraser_label = font.render("RMB: Eraser", True, colorBLACK)
    screen.blit(eraser_label, (440, 10))

    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        for rect, col in color_boxes:
            if rect.collidepoint(pos):
                current_color = col

        if square_rect.collidepoint(pos):
            current_figure = "square"
        elif circle_rect.collidepoint(pos):
            current_figure = "circle"
        elif rectangle_rect.collidepoint(pos):
            current_figure = "rectangle"
        elif right_triangle_rect.collidepoint(pos):
            current_figure = "right_triangle"
        elif equilateral_triangle_rect.collidepoint(pos):
            current_figure = "equilateral_triangle"
        elif rhombus_rect.collidepoint(pos):
            current_figure = "rhombus"

    if LMBpressed or RMBpressed:
        draw_color = colorWHITE if RMBpressed else current_color

        if current_figure == "circle":
            pygame.draw.circle(screen, draw_color, pos, SIZE)
        elif current_figure == "square":
            pygame.draw.rect(screen, draw_color, (pos[0], pos[1], SIZE, SIZE))
        elif current_figure == "rectangle":
            pygame.draw.rect(screen, draw_color, (pos[0], pos[1], SIZE * 2, SIZE))
        elif current_figure == "right_triangle":
            pygame.draw.polygon(screen, draw_color, [
                (pos[0], pos[1]),
                (pos[0], pos[1] + SIZE),
                (pos[0] + SIZE, pos[1] + SIZE)
            ])
        elif current_figure == "equilateral_triangle":
            pygame.draw.polygon(screen, draw_color, [
                (pos[0], pos[1]),
                (pos[0] - SIZE, pos[1] + SIZE),
                (pos[0] + SIZE, pos[1] + SIZE)
            ])
        elif current_figure == "rhombus":
            pygame.draw.polygon(screen, draw_color, [
                (pos[0], pos[1] - SIZE),
                (pos[0] - SIZE, pos[1]),
                (pos[0], pos[1] + SIZE),
                (pos[0] + SIZE, pos[1])
            ])

    pygame.display.flip()

pygame.quit()
