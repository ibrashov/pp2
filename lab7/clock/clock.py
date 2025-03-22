import pygame
import datetime
import os

pygame.init()
window = pygame.display.set_mode((920, 700))
timer = pygame.time.Clock()

assets = os.path.dirname(__file__)
background = pygame.image.load(os.path.join(assets, 'clockclock.png'))
background = pygame.transform.scale(background, (600, 600))

hand_min = pygame.image.load(os.path.join(assets, 'righthand.png'))
hand_min = pygame.transform.scale(hand_min, (300, 200))

hand_sec = pygame.image.load(os.path.join(assets, 'lefthand.png'))
hand_sec = pygame.transform.scale(hand_sec, (300, 200))

running = True

while running:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    hr = now.hour % 12
    mn = now.minute
    sc = now.second

    angle_hr = -((hr + mn / 60) * 30)
    angle_mn = -(mn * 6) - 10
    angle_sc = -(sc * 6) - 5

    img_min = pygame.transform.rotate(hand_min, angle_mn)
    img_sec = pygame.transform.rotate(hand_sec, angle_sc)

    window.fill((255, 255, 255))
    window.blit(background, (100, 100))
    window.blit(img_sec, (400 - img_sec.get_width() // 2, 400 - img_sec.get_height() // 2))
    window.blit(img_min, (400 - img_min.get_width() // 2, 400 - img_min.get_height() // 2))

    pygame.display.update()
    timer.tick(60)

pygame.quit()
