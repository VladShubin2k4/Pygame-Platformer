import sys
import pygame
from random import randint


class Ball:
    def __init__(self, screen_size):
        self.ball = pygame.image.load("basketball.png")
        self.geometry = self.ball.get_rect()
        self.size = self.width, self.height = screen_size[0], screen_size[1]
        self.geometry.x, self.geometry.y = self.width // 2, self.height // 2
        self.direction = [randint(1, self.geometry.x // 32), randint(1, self.geometry.y // 32)]
        self.game_over = False

    def draw(self, screen):
        self.move()
        screen.blit(self.ball, self.geometry)

    def move(self):
        if (self.geometry.x + self.geometry.width <= self.width) and (self.geometry.x >= 0):
            if (self.geometry.x + self.geometry.width == self.width) or (self.geometry.x == 0):
                self.direction[0] = -self.direction[0]
            self.geometry.x += self.direction[0]
        else:
            self.direction[0] = -self.direction[0]
            self.geometry.x += self.direction[0]

        if (self.geometry.y + self.geometry.height <= self.height) and (self.geometry.y >= 0):
            if (self.geometry.y + self.geometry.height == self.height) or (self.geometry.y == 0):
                self.direction[1] = -self.direction[1]
                self.game_over = True
            self.geometry.y += self.direction[1]
        elif self.geometry.y + self.geometry.height + self.direction[1] >= self.height:
            self.direction[0] = 0
            self.direction[1] = 0
            self.game_over = True
        else:
            self.direction[1] = -self.direction[1]
            self.geometry.y += self.direction[1]

    def resized_screen(self, screen_size):
        self.size = self.width, self.height = screen_size[0], screen_size[1]
        if self.geometry.x + self.geometry.width > self.width:
            self.geometry.x = self.width - self.geometry.width
        if self.geometry.y + self.geometry.height > self.height:
            self.geometry.y = self.height - self.geometry.height

    def collides_with_platform(self, platform):
        if (self.geometry.x + self.geometry.width >= platform.x and self.geometry.x <= platform.x + platform.w) and (
                self.geometry.y + self.geometry.height >= platform.y and self.geometry.y <= platform.y + platform.h):
            self.direction[0] = -self.direction[0]
            self.direction[1] = -self.direction[1]

    def get_over(self):
        return self.game_over

    def is_game_over(self):
        self.direction[0]=0
        self.direction[1]=0

class Platform:
    def __init__(self, screen_size, color):
        self.color = color
        self.size = self.scr_width, self.scr_height = screen_size[0], screen_size[1]
        self.x, self.y = self.scr_width // 2, self.scr_height // 2
        self.w, self.h = (120, 30)
        self.width = 0
        self.game_over = False

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h), self.width)

    def move(self, direction):
        if not self.game_over:
            if direction == 'A':
                self.cur_shift = -32
                if self.x > 0:
                    self.x += self.cur_shift
            if direction == 'D':
                self.cur_shift = 32
                if self.x + self.w < self.scr_width:
                    self.x += self.cur_shift

    def stop(self):
        self.cur_shift = 0

    def resized_screen(self, screen_size):
        self.size = self.scr_width, self.scr_height = screen_size[0], screen_size[1]
        if self.x + self.w > self.scr_width:
            self.x = self.scr_width - self.w
        if self.y + self.h > self.scr_height:
            self.y = self.scr_height - self.h

    def is_game_over(self):
        self.game_over = True


def main():
    colors = {"BLACK": (0, 0, 0), "GREEN": (0, 255, 0), "BROWN": (139, 69, 19), "RED": (255,0,0)}
    size = width, height = 800, 600
    pygame.init()
    screen = pygame.display.set_mode(size, pygame.RESIZABLE)

    ball = Ball(size)
    platform = Platform(size, colors["BROWN"])

    game_over = False

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.VIDEORESIZE:
                size = width, height = event.w, event.h
                screen = pygame.display.set_mode(size, pygame.RESIZABLE)
                ball.resized_screen(size)
                platform.resized_screen(size)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    platform.move('A')
                if event.key == pygame.K_d:
                    platform.move('D')

        screen.fill(colors["BLACK"])
        ball.draw(screen)

        if ball.get_over():
            ball.is_game_over()
            platform.is_game_over()

            pygame.font.init()
            font = pygame.font.SysFont('Comic Sans MS',50,True)

            data = "GAME OVER"
            ts = font.render(data,False,colors["RED"])
            screen.blit(ts,(width//2,height//2))

        ball.collides_with_platform(platform)
        platform.draw(screen)

        pygame.display.flip()
        pygame.time.wait(32)

    sys.exit()


if __name__ == '__main__':
    main()

