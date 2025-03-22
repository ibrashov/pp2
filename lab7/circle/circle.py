import pygame

pygame.init()
screen = pygame.display.set_mode((400, 300))
running = True
blue_mode = True
pos_x, pos_y = 30, 30

clock = pygame.time.Clock()

while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
        if e.type == pygame.KEYDOWN and e.key == pygame.K_SPACE:
            blue_mode = not blue_mode

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and pos_y > 0: pos_y -= 3
    if keys[pygame.K_DOWN] and pos_y < 300: pos_y += 3
    if keys[pygame.K_LEFT] and pos_x > 0: pos_x -= 3
    if keys[pygame.K_RIGHT] and pos_x < 400: pos_x += 3

    screen.fill((0, 0, 0))
    clr = (0, 128, 255) if blue_mode else (255, 100, 0)
    pygame.draw.circle(screen, clr, (pos_x, pos_y), 25)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
