import pygame
import random
from color_palette import *  # Import color constants (like colorRED, colorYELLOW)

# Initialize Pygame
pygame.init()

# Game window settings
WIDTH = 600
HEIGHT = 600
CELL = 30  # Size of each grid cell
screen = pygame.display.set_mode((HEIGHT, WIDTH))

# Load and play background music in a loop
pygame.mixer.music.load("resources/bc1.mp3")
pygame.mixer.music.play(-1)

# Draw a chessboard-like grid background
def draw_grid_chess():
    colors = [colorBLUE, colorGRAY]  # Alternate between blue and gray
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

# Point class for grid-based coordinates
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def __str__(self):
        return f"{self.x}, {self.y}"

# Snake class
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]  # Initial snake body
        self.dx = 1  # Direction: right
        self.dy = 0

    # Move snake by shifting all body segments
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    # Draw snake on the screen
    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))  # Head is red
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorGREEN, (segment.x * CELL, segment.y * CELL, CELL, CELL))  # Body is green

    # Check if the snake eats the food
    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            print("Got food!")
            self.body.append(Point(head.x, head.y))  # Grow the snake
            food.spawn(self.body)  # Reposition food
            return True
        return False

# Food class
class Food:
    def __init__(self):
        self.spawn([])  # Spawn food randomly not on the snake

    def spawn(self, snake_body):
        while True:
            x = random.randint(1, WIDTH // CELL - 2)
            y = random.randint(1, HEIGHT // CELL - 2)
            if all(p.x != x or p.y != y for p in snake_body):  # Avoid spawning on the snake
                break
        self.pos = Point(x, y)

    # Draw food as yellow square
    def draw(self):
        pygame.draw.rect(screen, colorYELLOW, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# Game variables
FPS = 5  # Initial speed
level = 1
score = 0
level_up_score = 3  # Increase level every 3 points
clock = pygame.time.Clock()
food = Food()
snake = Snake()
running = True
font = pygame.font.SysFont("Verdana", 20)
level_counter = 0  # Times level increased
score_counter = 0  # Times score increased

# Main game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # Handle key presses to change direction
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP:
                snake.dx = 0
                snake.dy = -1

    draw_grid_chess()   # Draw background
    snake.move()        # Move the snake

    # Wall collision ends the game
    head = snake.body[0]
    if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
        print("Game Over: Hit the wall!")
        running = False

    # If snake eats the food
    if snake.check_collision(food):
        score += 1
        score_counter += 1
        if score % level_up_score == 0:
            level += 1
            level_counter += 1
            FPS += 2  # Increase speed
            clock = pygame.time.Clock()
            print(f"Level up! Now at level {level} with speed {FPS}")

    snake.draw()  # Draw the snake
    food.draw()   # Draw the food

    # Show score and level
    score_text = font.render(f"Score: {score} (x{score_counter})  Level: {level} (x{level_counter})", True, colorWHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()  # Update screen
    clock.tick(FPS)        # Control game speed

# Quit the game
pygame.quit()
