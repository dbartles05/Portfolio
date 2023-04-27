# Back From Summer Game                                                                             Start Date: 8/22/22
# Dustyn Bartles                                                                                   Finish Date: 8/29/22
# Sr
# --------------------------


# HOW TO PLAY: Collect all the cannonballs you can while going back and forth the ocean without
# getting hit by an enemy pirate ship! can you beat all 5 levels?


import sys
import pygame
import time


class PlayerShip(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 50
        self.y = HEIGHT / 2
        self.vel = 4
        self.width = 100
        self.height = 50

        # Images
        self.ship1 = pygame.image.load("images/ShipUp.png")
        self.ship2 = pygame.image.load("images/ShipDown.png")
        self.ship3 = pygame.image.load("images/ShipLeft.png")
        self.ship4 = pygame.image.load("images/ShipRight.png")

        self.image = self.ship1
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.movement()
        self.stayonscreen()
        self.checkCollision()
        self.rect.center = (self.x, self.y)


    def movement(self):
        keys = pygame.key.get_pressed()

        # Movement
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
            self.image = self.ship3

        elif keys[pygame.K_RIGHT]:
            self.x += self.vel
            self.image = self.ship4

        if keys[pygame.K_UP]:
            self.y -= self.vel
            self.image = self.ship1

        elif keys[pygame.K_DOWN]:
            self.y += self.vel
            self.image = self.ship2


    def stayonscreen(self):
        # Left
        if self.x - self.width / 3.1 < 0:
            self.x = self.width / 3.1
        # Right
        elif self.x + self.width / 1.3 > WIDTH:
            self.x = WIDTH - self.width / 1.3
        # Up
        if self.y - self.height / .9 < 0:
            self.y = self.height / .9
        # Down
        elif self.y + self.height / .9 > HEIGHT:
            self.y = HEIGHT - self.height / .9


    def checkCollision(self):
        enemy_check = pygame.sprite.spritecollide(self, enemy_group, False, pygame.sprite.collide_mask)
        if enemy_check:
            explosion.explode(self.x, self.y)

class EnemyShip(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()

        self.EnemyShip1 = pygame.image.load("images/EnemyShipUp.png")
        self.EnemyShip2 = pygame.image.load("images/EnemyShipDown.png")

        if number == 1:
            self.x = 190
            self.image = pygame.image.load("images/EnemyShipUp.png")
            self.vel = -4

        else:
            self.x = 460
            self.image = pygame.image.load("images/EnemyShipDown.png")
            self.vel = 5

        self.y = HEIGHT / 2
        self.width = 50
        self.height = 50
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        self.movement()
        self.rect.center = (self.x, self.y)


    def movement(self):
        self.y += self.vel
        if self.y - self.height / .9 < 0:
            self.y = self.height / .9
            self.vel *= -1
            self.image = self.EnemyShip2

        elif self.y + self.height / .9 > HEIGHT:
            self.y = HEIGHT - self.height / .9
            self.vel *= -1
            self.image = self.EnemyShip1


class CBall(pygame.sprite.Sprite):
    def __init__(self, number):
        super().__init__()
        self.number = number

        if self.number == 1:
            self.image = pygame.image.load("images/Cannonball.png")
            self.visable = False
            self.x = 50

        else:
            self.image = pygame.image.load("images/Cannonball.png")
            self.visable = True
            self.x = 570

        self.y = HEIGHT / 2
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        if self.visable:
            self.collision()
            self.rect.center = (self.x, self.y)


    def collision(self):
        global SCORE, ship
        cball_hit = pygame.sprite.spritecollide(self, ship_group, False, pygame.sprite.collide_mask)

        if cball_hit:
            self.visable = False
            cball_collect.play()

            if self.number == 1:
                new_cball.visable = True

                if SCORE < 5:
                    SwitchLevel()

                else:
                    ship_group.empty()
                    DeleteOtherItems()

                    EndScreen(1)
            else:
                old_cball.visable = True


class Explosion(object):
    def __init__(self):
        self.costume = 1
        self.width = 140
        self.height = 140
        self.image = pygame.image.load("images/explosion" + str(self.costume) + ".png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))

    def explode(self, x, y):
        x = x - self.width / 2
        y = y - self.height / 1.5
        DeletePlayerShip()
        ship_explosion.play()

        while self.costume < 26:
            self.image = pygame.image.load("images/explosion" + str(self.costume) + ".png")
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
            win.blit(self.image, (x, y))
            pygame.display.update()

            self.costume += 1
            time.sleep(0.1)

        DeleteOtherItems()
        EndScreen(0)


def Score():
    global gameOn

    if gameOn:
        score_text = score_font.render(str(SCORE) + ' / 5', True, (255, 255, 255))
        win.blit(score_text, (270, 5))


def checkCBalls():
    for cball in cballs:
        if not cball.visable:
            cball.kill()
        else:
            if not cball.alive():
                cball_group.add(cball)


def SwitchLevel():
    global SCORE

    if slow_ship.vel < 0:
        slow_ship.vel -= 1

    else:
        slow_ship.vel += 1

    if fast_ship.vel < 0:
        fast_ship.vel -= 1

    else:
        fast_ship.vel += 1

    SCORE += 1


def DeletePlayerShip():
    global ship

    ship.kill()
    enemy_group.draw(win)
    cball_group.draw(win)

    enemy_group.update()
    cball_group.update()

    pygame.display.update()


def DeleteOtherItems():
    enemy_group.empty()
    cball_group.empty()
    cballs.clear()


def EndScreen(n):
    global gameOn

    gameOn = False

    if n == 0:
        GameOverScreen = score_font.render("YOU DIED!", 1, WHITE)
        win.fill((15, 212, 203))
        win.blit(GameOverScreen, (WIDTH - 410, 200))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()

    elif n == 1:
        YouWonScreen = score_font.render("YOU WON!", 1, WHITE)
        win.fill((15, 212, 203))
        win.blit(YouWonScreen, (WIDTH - 410, 200))
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()


WIDTH = 640
HEIGHT = 480


# Sounds

pygame.mixer.init()

cball_collect = pygame.mixer.Sound("sounds/zapsplat_multimedia_game_sound_building_blocks_bricks_collect_click_001_70219.mp3")
ship_explosion = pygame.mixer.Sound("sounds/zapsplat_explosion_big_heavy_dynomite_001_62660.mp3")

cball_collect.set_volume(0.5)
ship_explosion.set_volume(0.5)

pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pirate Cross")
clock = pygame.time.Clock()

RED = (255, 6, 0)
GREEN = (0,255,0)
WHITE = (255,255,255)

SCORE = 0
                                           # Size
score_font = pygame.font.SysFont("comicsans", 30, True)

ship = PlayerShip()
ship_group = pygame.sprite.Group()
ship_group.add(ship)

slow_ship = EnemyShip(1)
fast_ship = EnemyShip(2)
enemy_group = pygame.sprite.Group()
enemy_group.add(slow_ship, fast_ship)

old_cball = CBall(1)
new_cball = CBall(2)
cball_group = pygame.sprite.Group()
cball_group.add(old_cball, new_cball)
cballs = [old_cball, new_cball]

explosion = Explosion()

gameOn = True
run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    win.fill((15, 212, 203))

    Score()
    checkCBalls()

    enemy_group.draw(win)
    ship_group.draw(win)
    cball_group.draw(win)


    enemy_group.update()
    ship_group.update()
    cball_group.update()


    pygame.display.update()

pygame.quit()
