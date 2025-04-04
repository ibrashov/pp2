import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Set screen dimensions and create game window
WIDTH = 400
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Load images and background music
image_background = pygame.image.load('resources/AnimatedStreet.png')
image_player = pygame.image.load('resources/Player.png')
image_enemy = pygame.image.load('resources/Enemy.png')

# Load and play background music
pygame.mixer.music.load('resources/background.wav')
pygame.mixer.music.play(-1)  # Loop forever

# Load sound effects
sound_crash = pygame.mixer.Sound('resources/crash.wav')
sound_coin = pygame.mixer.Sound('resources/coin.wav')

# Setup fonts and Game Over text
font = pygame.font.SysFont("Verdana", 60)
score_font = pygame.font.SysFont("Verdana", 20)
image_game_over = font.render("Try better", True, "black")
image_game_over_rect = image_game_over.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Define Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_player
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT
        self.speed = 5

    def move(self):
        # Check which keys are pressed and move accordingly
        keys = pygame.key.get_pressed()
        if keys[pygame.K_RIGHT]:
            self.rect.move_ip(self.speed, 0)
        if keys[pygame.K_LEFT]:
            self.rect.move_ip(-self.speed, 0)

        # Prevent player from going off-screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

# Define Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = image_enemy
        self.rect = self.image.get_rect()
        self.speed = 10
        self.gen_random_rect()  # Set random position at the top

    def gen_random_rect(self):
        # Set random x position for enemy
        self.rect.left = random.randint(0, WIDTH - self.rect.w)
        self.rect.bottom = 0

    def move(self):
        # Move enemy downward
        self.rect.move_ip(0, self.speed)
        # Reset position if it moves off the screen
        if self.rect.top > HEIGHT:
            self.gen_random_rect()

# Define Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.weight = random.choice([1, 2, 5])  # Coin value
        self.image = pygame.Surface((20, 20))
        self.image.fill((255, 223, 0))  # Yellow color
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = random.randint(3, 6)  # Random speed

    def move(self):
        # Move coin downward
        self.rect.move_ip(0, self.speed)
        # Remove coin if it goes off screen
        if self.rect.top > HEIGHT:
            self.kill()

# Game state setup
running = True
clock = pygame.time.Clock()
FPS = 60  # Frame rate

# Create player and enemy instances
player = Player()
enemy = Enemy()

# Sprite groups
coins = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemy_sprites = pygame.sprite.Group()

# Add initial entities to sprite groups
all_sprites.add(player, enemy)
enemy_sprites.add(enemy)

# Score and difficulty tracking
coin_score = 0
coin_goal = 10  # Speed up enemy after collecting 10 coins
last_speedup_score = 0  # Keep track of last speedup

# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False  # Exit game

    player.move()  # Update player movement
    screen.blit(image_background, (0, 0))  # Draw background

    # Move and draw all game objects
    for entity in all_sprites:
        if hasattr(entity, 'move'):
            entity.move()
        screen.blit(entity.image, entity.rect)

    # Random chance to spawn new coin
    if random.randint(1, 50) == 1:
        coin = Coin()
        coins.add(coin)
        all_sprites.add(coin)

    # Check for collisions between player and coins
    collected = pygame.sprite.spritecollide(player, coins, dokill=True)
    for coin in collected:
        sound_coin.play()
        coin_score += coin.weight  # Add coin value to score

    # Increase enemy speed based on score
    if coin_score - last_speedup_score >= coin_goal:
        enemy.speed += 1
        last_speedup_score = coin_score

    # Collision with enemy ends the game
    if pygame.sprite.spritecollideany(player, enemy_sprites):
        sound_crash.play()
        time.sleep(1)
        running = False  # Exit main loop
        screen.fill("red")
        screen.blit(image_game_over, image_game_over_rect)
        pygame.display.flip()
        time.sleep(3)

    # Display current score on screen
    score_text = score_font.render(f"Score: {coin_score}", True, "white")
    screen.blit(score_text, (10, 10))

    # Update the screen and tick the clock
    pygame.display.flip()
    clock.tick(FPS)

# Quit the game
pygame.quit()
