# SnakeGame
import pygame, sys, random

pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.font.init()


class Snake:
    def __init__(self, body_img_path, length):
        # self.head_img_path = head_img_path
        self.body_img_path = body_img_path
        self.length = length
        self.snake_body_x = [12] * length
        self.snake_body_y = [12] * length
        self.speed = 24
        self.direction = 'down'
        self.rect = []
        self.body_image = pygame.image.load(body_img_path)
       # self.head_image = pygame.image.load(head_img_path)
        self.head_image_left = pygame.image.load("assets/snake_left.png")
        self.head_image_right = pygame.image.load("assets/snake_right.png")
        self.head_image_up = pygame.image.load("assets/snake_up.png")
        self.head_image_down = pygame.image.load("assets/snake.png")
        self.rect.append(self.head_image_down.get_rect())
        for i in range(1, self.length):
            self.rect.append(self.body_image.get_rect())
            self.rect[i].center = (self.snake_body_x[i], self.snake_body_y[i])

    def snake_movement(self):

        if self.direction == 'down':
            if self.rect[0].y >= 560:
                game_over()
            else:
                for i in range(self.length - 1, 0, -1):
                    self.rect[i].y = self.rect[i - 1].y
                    self.rect[i].x = self.rect[i - 1].x
                self.rect[0].y += self.speed

        if self.direction == 'up':
            if self.rect[0].y <= 0:
                game_over()
            else:
                for i in range(self.length - 1, 0, -1):
                    self.rect[i].y = self.rect[i - 1].y
                    self.rect[i].x = self.rect[i - 1].x
                self.rect[0].y -= self.speed

        if self.direction == 'right':
            if self.rect[0].x >= 560:
                game_over()
            else:
                for i in range(self.length - 1, 0, -1):
                    self.rect[i].y = self.rect[i - 1].y
                    self.rect[i].x = self.rect[i - 1].x
                self.rect[0].x += self.speed

        if self.direction == 'left':
            if self.rect[0].x <= 0:
                game_over()
            else:
                for i in range(self.length - 1, 0, -1):
                    self.rect[i].y = self.rect[i - 1].y
                    self.rect[i].x = self.rect[i - 1].x
                self.rect[0].x -= self.speed

    def snake_self_collition(self):
        for i in range(3, self.length):
            if pygame.Rect.colliderect(self.rect[0], self.rect[i]):
                game_over()

    def growing_up(self):
        self.length += 1
        self.rect.append(self.body_image.get_rect())
        # as new block should not be appear in  the middle of the game on the top so it generates outside the board
        self.rect[-1].center = (-10, -10)

    def draw_snake(self, screen):

        if self.direction == 'left':
            screen.blit(self.head_image_left, self.rect[0])
        if self.direction =='right':
            screen.blit(self.head_image_right, self.rect[0])
        if self.direction == 'up':
            screen.blit(self.head_image_up, self.rect[0])
        if self.direction == 'down':
            screen.blit(self.head_image_down, self.rect[0])
        for i in range(1, self.length):
            screen.blit(self.body_image, self.rect[i])


class Food:
    def __init__(self, img_path):
        self.food_x = random.randint(1, 24) * 24
        self.food_y = random.randint(1, 24) * 24
        self.food_eaten = 0
        self.img_path = img_path
        self.image = pygame.image.load(img_path)
        self.rect = self.image.get_rect()
        self.rect.x = self.food_x
        self.rect.y = self.food_y

    def random_food_create(self):
        self.rect.x = random.randint(1, 24) * 24
        self.rect.y = random.randint(1, 24) * 24

    def draw_food(self, screen):
        screen.blit(self.image, self.rect)

    def snake_food_collision(self):
        if pygame.Rect.colliderect(self.rect, snake.rect[0]):
            pygame.mixer.Sound.play(SCORE_SOUND)
            self.food_eaten += 1
            self.random_food_create()
            snake.growing_up()


def count_down(game_stop):
    global GAME_STATE

    if pygame.time.get_ticks() - game_stop < 1500:
        count_time = GAME_FONT.render("READY", False, (36, 89, 0))
        screen.blit(count_time, (CANVAS_WIDTH / 2 - 30, CANVAS_HEIGHT / 2 - 100))
    elif pygame.time.get_ticks() - game_stop < 2500:
        count_time = GAME_FONT.render("1", False, (36, 89, 0))
        screen.blit(count_time, (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100))
    elif pygame.time.get_ticks() - game_stop < 3500:
        count_time = GAME_FONT.render("2", False, (36, 89, 0))
        screen.blit(count_time, (CANVAS_WIDTH / 2, CANVAS_HEIGHT / 2 - 100))
    elif 3501 < pygame.time.get_ticks() - game_stop < 4000:
        count_time = GAME_FONT.render("START", False, (36, 89, 0))
        screen.blit(count_time, (CANVAS_WIDTH / 2 - 25, CANVAS_HEIGHT / 2 - 100))
    else:
        GAME_STATE = 'active'


def game_over():
    global GAME_STATE
    pygame.mixer.Sound.play(GAME_OVER_SOUND)
    GAME_STATE = 'game_over'
    food_score = GAME_FONT.render(f"FOOD EATEN : Player {food.food_eaten}", False, (25, 250, 250))


def restart_game():
    global snake, food, start_time, GAME_STATE
    del snake
    del food
    snake = Snake("assets/body.png", 3)
    food = Food('assets/apple.png')
    GAME_STATE = 'ready'
    start_time = pygame.time.get_ticks()
    count_down(start_time)


def disply_background():
    screen.blit(BACKGROUND, (0, 0))


def disply_board():
    screen.blit(BOARD, (0, 0))


def state_intro():
    global GAME_SPEED
    disply_background()
    restart = GAME_FONT.render("  Press Space  to Start", False, (36, 89, 0))
    mute = GAME_FONT_2.render("  Press 0 for Mute/Unmute", False, (36, 89, 0))
    level = GAME_FONT_2.render("  Press 1 (Easy) /2 (Medium) /3 (Hard) /4 (Insane)", False, (36, 89, 0))
    screen.blit(restart, (CANVAS_WIDTH / 2 - 120, CANVAS_HEIGHT / 2 - 20))
    screen.blit(level, (CANVAS_WIDTH / 2 - 200, 520))
    screen.blit(mute, (CANVAS_WIDTH / 2 - 120, 500))


def state_ready():
    disply_background()
    count_down(start_time)


def state_active():
    disply_board()
    snake.draw_snake(screen)
    food.snake_food_collision()
    snake.snake_self_collition()
    food.draw_food(screen)
    screen.blit(scores, (CANVAS_WIDTH / 2 - 80, CANVAS_HEIGHT - 30))


def state_game_over():
    disply_background()
    end = GAME_FONT.render("GAME OVER", False, (36, 89, 0))
    restart = GAME_FONT.render("  Press space to Restart", False, (199, 255, 199))
    mute = GAME_FONT_2.render("  Press 0 for Mute/Unmute", False, (36, 89, 0))
    level = GAME_FONT_2.render("  Press 1 (Easy) /2 (Medium) /3 (Hard) /4 (Insane)", False, (36, 89, 0))
    screen.blit(end, (CANVAS_WIDTH / 2 - 60, CANVAS_HEIGHT / 2 - 80))
    screen.blit(restart, (CANVAS_WIDTH / 2 - 120, CANVAS_HEIGHT / 2 - 20))
    screen.blit(scores, (CANVAS_WIDTH / 2 - 70, CANVAS_HEIGHT / 2 - 50))
    screen.blit(level, (CANVAS_WIDTH / 2 - 200, 520))
    screen.blit(mute, (CANVAS_WIDTH / 2 - 120, 500))


def main_logic():
    global scores
    clock.tick(FPS)
    scores = GAME_FONT.render(f"FOOD EATEN: {food.food_eaten}", False, (36, 89, 0))

    if GAME_STATE == 'game_intro':
        state_intro()

    if GAME_STATE == 'ready':
        state_ready()

    if GAME_STATE == 'active':
        state_active()

    if GAME_STATE == 'game_over':
        state_game_over()


snake = Snake("assets/body.png", 3)
food = Food('assets/apple.png')
FPS = 120
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
GAME_SPEED_EASY = 200
GAME_SPEED_MEDIUM = 100
GAME_SPEED_HARD = 50
GAME_SPEED_INSANE = 30
GAME_SPEED = GAME_SPEED_MEDIUM
GAME_STATE = 'game_intro'
GAME_FONT = pygame.font.Font("freesansbold.ttf", 20)
GAME_FONT_2 = pygame.font.Font("freesansbold.ttf", 15)
clock = pygame.time.Clock()
start_time = 0
screen = pygame.display.set_mode((CANVAS_WIDTH, CANVAS_HEIGHT))
ICON = pygame.image.load('assets/snake.png')
pygame.display.set_icon(ICON)
pygame.display.set_caption('Snake Game')
BOARD = pygame.image.load("assets/board.png")
BACKGROUND = pygame.image.load("assets/home.png")
SCORE_SOUND = pygame.mixer.Sound("assets/hish.wav")
GAME_OVER_SOUND = pygame.mixer.Sound("assets/GameOver.wav")
pygame.mixer.music.load("assets/fun.mp3")
pygame.mixer.music.play(loops=-1)
DELAY_SNAKE_MOVEMENT = pygame.USEREVENT + 0
pygame.time.set_timer(DELAY_SNAKE_MOVEMENT, GAME_SPEED)

while True:
    if __name__ == "__main__":
        main_logic()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and GAME_STATE == 'game_intro':
            state_ready()
            GAME_STATE = 'ready'

        if event.type == pygame.KEYDOWN and (GAME_STATE == 'game_intro' or GAME_STATE == 'game_over'):
            if event.key == pygame.K_1:
                GAME_SPEED = GAME_SPEED_EASY
                pygame.mixer.Sound.play(SCORE_SOUND)

            if event.key == pygame.K_2:
                GAME_SPEED = GAME_SPEED_MEDIUM
                pygame.mixer.Sound.play(SCORE_SOUND)

            if event.key == pygame.K_3:
                GAME_SPEED = GAME_SPEED_HARD
                pygame.mixer.Sound.play(SCORE_SOUND)

            if event.key == pygame.K_4:
                GAME_SPEED = GAME_SPEED_INSANE
                pygame.mixer.Sound.play(SCORE_SOUND)
            pygame.time.set_timer(DELAY_SNAKE_MOVEMENT, GAME_SPEED)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            else:
                pygame.mixer.music.play(loops=-1)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and GAME_STATE == 'game_over':
            restart_game()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            if snake.direction != 'left':
                snake.direction = 'right'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            if snake.direction != 'right':
                snake.direction = 'left'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if snake.direction != 'down':
                snake.direction = 'up'
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            if snake.direction != 'up':
                snake.direction = 'down'

        if event.type == DELAY_SNAKE_MOVEMENT and GAME_STATE == 'active':
            snake.snake_movement()

    pygame.display.update()
