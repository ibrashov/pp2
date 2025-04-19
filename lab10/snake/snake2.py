import pygame
import random
import time
import psycopg2
from color_palette import *

pygame.init()
WIDTH = 600
HEIGHT = 600
CELL = 30
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.mixer.music.load("resources/bc1.mp3")
pygame.mixer.music.play(-1)

def connect_db():
    return psycopg2.connect(
        host="localhost",
        dbname="phonebook",
        user="postgres",
        password="q1w2e3r4"
    )

def get_or_create_user(username):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            result = cur.fetchone()
            if result:
                return result[0]
            else:
                cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
                return cur.fetchone()[0]

def get_last_level(user_id):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT level FROM user_score WHERE user_id = %s ORDER BY created_at DESC LIMIT 1", (user_id,))
            result = cur.fetchone()
            return result[0] if result else 1

def save_score(user_id, score, level):
    with connect_db() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO user_score (user_id, score, level) VALUES (%s, %s, %s)", (user_id, score, level))

def draw_grid_chess():
    colors = [colorBLUE, colorGRAY]
    for i in range(HEIGHT // CELL):
        for j in range(WIDTH // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

def draw_walls(level):
    wall_color = colorWHITE
    if level >= 2:
        for x in range(0, WIDTH // CELL):
            pygame.draw.rect(screen, wall_color, (x * CELL, 0, CELL, CELL))
            pygame.draw.rect(screen, wall_color, (x * CELL, HEIGHT - CELL, CELL, CELL))
    if level >= 3:
        for y in range(1, HEIGHT // CELL - 1):
            pygame.draw.rect(screen, wall_color, (0, y * CELL, CELL, CELL))
            pygame.draw.rect(screen, wall_color, (WIDTH - CELL, y * CELL, CELL, CELL))

def wall_collision(head, level):
    if level >= 2 and (head.y == 0 or head.y == (HEIGHT // CELL - 1)):
        return True
    if level >= 3 and (head.x == 0 or head.x == (WIDTH // CELL - 1)):
        return True
    return False

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorGREEN, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            for _ in range(food.weight):
                self.body.append(Point(head.x, head.y))
            return True
        return False

class Food:
    def __init__(self):
        self.spawn([])

    def spawn(self, snake_body):
        while True:
            x = random.randint(1, WIDTH // CELL - 2)
            y = random.randint(1, HEIGHT // CELL - 2)
            if all(p.x != x or p.y != y for p in snake_body):
                break
        self.pos = Point(x, y)
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = time.time()

    def draw(self):
        pygame.draw.rect(screen, colorYELLOW, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    def expired(self):
        return time.time() - self.spawn_time > 3

username = input("Enter your username: ")
user_id = get_or_create_user(username)
level = get_last_level(user_id)
FPS = 5 + level * 2
score = 0
level_up_score = 3
clock = pygame.time.Clock()
food = Food()
snake = Snake()
running = True
font = pygame.font.SysFont("Verdana", 20)
level_counter = level - 1
score_counter = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
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
            elif event.key == pygame.K_p:
                save_score(user_id, score, level)
                print("Game paused and progress saved!")

    draw_grid_chess()
    draw_walls(level)
    snake.move()

    head = snake.body[0]
    if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL or wall_collision(head, level):
        print("Game Over: Hit the wall!")
        running = False

    if snake.check_collision(food):
        score += food.weight
        score_counter += food.weight
        if score % level_up_score == 0:
            level += 1
            level_counter += 1
            FPS += 2
            clock = pygame.time.Clock()
        food.spawn(snake.body)
    elif food.expired():
        food.spawn(snake.body)

    snake.draw()
    food.draw()

    score_text = font.render(f"Score: {score} (x{score_counter})  Level: {level} (x{level_counter})", True, colorWHITE)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
