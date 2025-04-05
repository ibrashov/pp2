import pygame

pygame.init()
WIDTH = 1400
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))

colorBLACK = (0, 0, 0)
colorWHITE = (255, 255, 255)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)

colors = [colorRED, colorGREEN, colorBLUE]

# Only 2 shapes now: circle and rectangle
figures = ["circle", "rectangle"]
current_color = colorWHITE
current_figure = "circle"

LMBpressed = False
RMBpressed = False
SIZE = 10

screen.fill(colorWHITE)
font = pygame.font.SysFont("Verdana", 24)
running = True

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

    # Color buttons
    color_boxes = []
    for i, col in enumerate(colors):
        rect = pygame.draw.rect(screen, col, (i * 40, 0, 40, 40))
        color_boxes.append((rect, col))

    # Shape buttons
    circle_rect = pygame.draw.circle(screen, colorBLACK, (150, 20), 20, 3)
    rectangle_rect = pygame.draw.rect(screen, colorBLACK, (190, 10, 50, 25), 3)

    # Eraser label
    pygame.draw.rect(screen, colorWHITE, (300, 0, 200, 40))
    eraser_label = font.render("RMB: Eraser", True, colorBLACK)
    screen.blit(eraser_label, (300, 10))

    pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if click[0]:
        for rect, col in color_boxes:
            if rect.collidepoint(pos):
                current_color = col
        if circle_rect.collidepoint(pos):
            current_figure = "circle"
        elif rectangle_rect.collidepoint(pos):
            current_figure = "rectangle"

    if LMBpressed or RMBpressed:
        draw_color = colorWHITE if RMBpressed else current_color
        if current_figure == "circle":
            pygame.draw.circle(screen, draw_color, pos, SIZE)
        elif current_figure == "rectangle":
            pygame.draw.rect(screen, draw_color, (pos[0], pos[1], SIZE * 2, SIZE))

    pygame.display.flip()

pygame.quit()
