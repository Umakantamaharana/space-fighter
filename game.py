import random
import sys
import pygame

pygame.init()

clock = pygame.time.Clock()

screenwidth, screenheight = (400, 300)
screen = pygame.display.set_mode((screenwidth, screenheight))


class ScrollBackground:
    def __init__(self, screen_height, image_file):
        self.img = pygame.image.load(image_file)
        self.coord = [0, 0]
        self.coord2 = [0, -screen_height]
        self.y_original = self.coord[1]
        self.y2_original = self.coord2[1]

    def show(self, surface):
        surface.blit(self.img, self.coord)
        surface.blit(self.img, self.coord2)

    def update_coord(self, speed_y, t):
        distance_y = speed_y * t
        self.coord[1] += distance_y
        self.coord2[1] += distance_y
        if self.coord2[1] >= 0:
            self.coord[1] = self.y_original
            self.coord2[1] = self.y2_original


class Jet:
    def __init__(self, screen_height, screen_width):
        self.x, self.y = screen_width / 2, screen_height - 25

    def move(self, x_value, surface):
        self.x = x_value
        pts = [(self.x - 20, self.y + 20), (self.x, self.y), (self.x + 20, self.y + 20)]
        return pygame.draw.polygon(surface, (0, 255, 0), pts, 2)

    def fire(self, x_value, surface):
        return pygame.draw.line(surface, (0, 255, 255), (x_value, self.y - 20), (x_value, 0), 2)


class Enemy:
    def __init__(self, screen_height, screen_width):
        self.x, self.y = random.randint(10, screen_width - 10), random.randint(10, screen_height / 4)

    def show(self, surface):
        return pygame.draw.circle(surface, (255, 0, 0), (self.x, self.y), 10)


class ScoreBoard:
    def __init__(self, screen_height):
        self.screen_height = screen_height
        self.color = (255, 255, 255)

    def update(self, surface, font, pts, change=''):
        if change == "+":
            self.color = (0, 255, 0)
        elif change == "-":
            self.color = (255, 0, 0)
        score = font.render("Score : " + str(pts), 1, self.color)
        surface.blit(score, (10, self.screen_height - 50))


game_bg = ScrollBackground(screenheight, "background.jpg")
jet_1 = Jet(screenheight, screenwidth)
enemy = Enemy(screenheight, screenwidth)
score_board = ScoreBoard(screenheight)

frame_rate = 60
scrolling_speed = 100
score_font = pygame.font.SysFont("monospace", 16)

points = 0

pygame.mouse.set_visible(False)
pygame.display.set_caption("Jet fighter")

while True:
    clock.tick(60)
    time = clock.tick(frame_rate) / 1000.0
    x, y = pygame.mouse.get_pos()

    game_bg.update_coord(scrolling_speed, time)
    game_bg.show(screen)

    jet_1.move(x, screen)

    alien = enemy.show(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            bullet = jet_1.fire(x, screen)
            if pygame.Rect.colliderect(alien, bullet):
                enemy = Enemy(screenheight, screenwidth)
                points += 1
                score_board.update(screen, score_font, points, "+")
            else:
                points -= 1
                score_board.update(screen, score_font, points, "-")

    score_board.update(screen, score_font, points)

    pygame.display.update()
