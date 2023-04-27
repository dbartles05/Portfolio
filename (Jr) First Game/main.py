# This is a code for First Game            |
# Dustyn Bartles                           |
# 2/14/2022                                |
# Jr                                       |
# -----------------------------------------|

# Controls: Use the Arrow Keys (Left & Right) to move, and the Space Bar to shoot.

import sys
import time

import pygame
import random
import sqlite3
from sqlite3 import Error
import GameLogon as GL

from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    KEYUP,
    K_SPACE,
    QUIT,
)

SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800


class Player(pygame.sprite.Sprite):
    moveCount = 0
    isMoving = False
    speed = 5
    HP = 100


    def setMoving(self, value):
        self.isMoving = value

    def increaseSpeed(self, increase):
        self.speed += increase

    def __init__(self):
        super(Player, self).__init__()

        self.health = 100
        self.surf = pygame.image.load("images/survivor1_gun.png").convert_alpha()

        self.rect = self.surf.get_rect(
            center=(
                (SCREEN_WIDTH / 2),
                (SCREEN_HEIGHT - 64),
            )
        )

    def update(self, pressed_keys):
        playerAnimation = ["images/survivor1_gun.png"]

        if self.moveCount > len(playerAnimation) - 1:
            self.moveCount = 0
        self.surf = pygame.image.load(playerAnimation[self.moveCount]).convert_alpha()
        self.moveCount += 1

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-self.speed, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(self.speed, 0)

        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Zombie(pygame.sprite.Sprite):
    isDying = False
    def __init__(self):
        super(Zombie, self).__init__()
        self.surf = pygame.image.load("images/zoimbie1_hold.png").convert_alpha()
        self.rect = self.surf.get_rect(

            center=(
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(10, 10),
            ))
        self.dieCount = 30
        self.rotateAngle = 1
        self.speed = random.randint(4, 10)
        self.etype = "zombie"


    def update(self):
        if not self.isDying:
            self.rect.move_ip(0, 2)
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()
        else:
            if self.dieCount == 0:
                self.kill()
            else:
                self.surf = pygame.transform.rotate(pygame.image.load("images/zoimbie1_hold.png").convert_alpha(),self.rotateAngle)
                self.rotateAngle += 30
                self.rect.move_ip(0, -2)
                self.dieCount -= 1


class Robot(pygame.sprite.Sprite):
    isDying = False
    def __init__(self):
        super(Robot, self).__init__()
        self.surf = pygame.image.load("images/robot1_gun.png").convert_alpha()
        self.rect = self.surf.get_rect(

            center=(
                random.randint(100, SCREEN_WIDTH - 100),
                random.randint(10, 10),
            ))
        self.dieCount = 30
        self.rotateAngle = 1
        self.speed = random.randint(4, 10)
        self.etype = "robot"


    def update(self):
        if not self.isDying:
            self.rect.move_ip(0, 2)
            if self.rect.top >= SCREEN_HEIGHT:
                self.kill()
        else:
            if self.dieCount == 0:
                self.kill()
            else:
                self.surf = pygame.transform.rotate(pygame.image.load("images/robot1_gun.png").convert_alpha(),self.rotateAngle)
                self.rotateAngle += 30
                self.rect.move_ip(0, -2)
                self.dieCount -= 1


class PBullet(pygame.sprite.Sprite):
    def __init__(self):
        super(PBullet, self).__init__()
        self.PBulletCount = 0
        self.item = random.choice(["PBullets"])
        self.etype = ""
        if self.item == "PBullets":
            self.etype = "PBullets"
        if self.etype == "PBullets":
            self.surf = pygame.image.load("images/bulletYellow_outline.png")
        self.rect = self.surf.get_rect(
            # Left / Right                 # Up / Down
            center=(player.rect.left + 31, player.rect.bottom - 46),
        )
        self.speed = random.randint(10, 10)

    def update(self):
        PBulletAnimation = ["images/bulletYellow_outline.png", "images/bulletYellowSilver_outline.png"]
        if self.etype == "PBullets":
            if self.PBulletCount > len(PBulletAnimation) - 1:
                self.PBulletCount = 0
            self.surf = pygame.image.load(PBulletAnimation[self.PBulletCount]).convert_alpha()
            self.PBulletCount += 1

            if self.rect.bottom <= 0:
                self.kill()
            else:
                self.rect.move_ip(0, -self.speed)


def getDbConnection():
    conn = None
    try:
        conn = sqlite3.connect("GameStats.db")
    except Error as e:

        print(e)

    return conn


def saveGameStats(UserName,HighScore):
    try:
        conn = getDbConnection()
        curr = conn.cursor()
        updateSql = "UPDATE Stats set HighScore = ? WHERE UserID = ?"
        record = (HighScore,UserName)
        curr.execute(updateSql,record)
        conn.commit()
        conn.close()
    except Error as e:
        print(e)


user_name = GL.GameLogon()
con = getDbConnection()
curr = con.cursor()


rows = curr.execute("SELECT * FROM Stats WHERE UserID = ?", (user_name,)).fetchall()
if len(rows) == 0:
    record = (user_name,0,0,0,0)
    sql = "INSERT INTO Stats (UserId,HighScore,TimesPlayed,EnemyKilled,FruitEaten) values(?,?,?,?,?)"
    curr.execute(sql,record)
    con.commit()
    HighScore = 0
else:
     for row in rows:
         HighScore = row[1]

# Sounds
pygame.mixer.init()
walking = pygame.mixer.Sound("sounds/walking.wav")
walking.set_volume(0.5)


pygame.init()

# Colors
black = (0, 0, 0)
white = (255,255,255)
red = 71
green = 134
blue = 2

GREEN = (0,255,0)
BLUE = (0,191,255)
YELLOW = (255,233,0)
ORANGE = (255,130,0)
RED = (255,6,0)

score = 0
HP = 100
Level = 0


preHighScore = 0
if HighScore > 0:
    preHighScore = HighScore



myFont = pygame.font.SysFont("", 25)

scoreLabel = myFont.render("Score: ",1,white)
scoreValue = myFont.render(str(score),1,white)

HighScoreLabel = myFont.render("High Score:",1, white)
HighScoreValue = myFont.render(str(HighScore),1,white)

HPLabel = myFont.render("HP: ",1,GREEN)
HPValue = myFont.render(str(HP),1,GREEN)

NameLabel = myFont.render("User: ",1,white)
NameValue = myFont.render(str(user_name),1,white)

LevelLabel = myFont.render("Level: ",1,white)
LevelValue = myFont.render(str(Level),1,white)


clock = pygame.time.Clock()


background_image = pygame.image.load("images/City.png")

background_image = pygame.transform.scale(background_image, (600, 800))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption(f"Survive The Waves")

ADDZOMBIE = pygame.USEREVENT + 1
pygame.time.set_timer(ADDZOMBIE, 3000)

ADDROBOT = pygame.USEREVENT + 2
pygame.time.set_timer(ADDROBOT, 31500)


player = Player()


all_sprites = pygame.sprite.Group()
zombie_sprites = pygame.sprite.Group()
weapons_sprites = pygame.sprite.Group()
robot_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True

while running:
    for event in pygame.event.get():

        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

            if event.key == K_LEFT or event.key == K_RIGHT:
                if not player.isMoving:
                    player.setMoving(True)
                    walking.play()

            if event.key == K_SPACE:
                weapon = PBullet()
                weapons_sprites.add(weapon)
                all_sprites.add(weapon)

        if event.type == KEYUP:
            if event.key == K_LEFT or event.key == K_RIGHT:
                player.setMoving(False)
                walking.stop()

        if event.type == ADDZOMBIE:
            newZombie = Zombie()
            zombie_sprites.add(newZombie)
            all_sprites.add(newZombie)

        if event.type == ADDROBOT:
            newRobot = Robot()
            robot_sprites.add(newRobot)
            all_sprites.add(newRobot)

        elif event.type == QUIT:
            if HighScore > preHighScore:
                saveGameStats(user_name,HighScore)
            running = False

    screen.blit(background_image, [0, 0])

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    zombie_sprites.update()
    robot_sprites.update()
    weapons_sprites.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)


    for entity in weapons_sprites:
        newZombie = pygame.sprite.spritecollideany(entity,zombie_sprites)
        if newZombie != None:
           newZombie.isDying = True
           entity.kill()
           score += 50

        NewRobot = pygame.sprite.spritecollideany(entity,robot_sprites)
        if NewRobot != None:
           NewRobot.isDying = True
           entity.kill()
           score += 100

    ZombieHit = pygame.sprite.spritecollideany(player,zombie_sprites)
    if ZombieHit is not None:
        HP -= 25
        ZombieHit.kill()
    RobotHit = pygame.sprite.spritecollideany(player,robot_sprites)

    if RobotHit is not None:
        HP -= 50
        RobotHit.kill()

    HPValue = myFont.render(str(HP),1,GREEN)

    if HP < 76:
        HPValue = myFont.render(str(HP),1,YELLOW)
        HPLabel = myFont.render("HP: ", 1, YELLOW)

    if HP < 51:
        HPValue = myFont.render(str(HP),1,ORANGE)
        HPLabel = myFont.render("HP: ", 1, ORANGE)

    if HP < 26:
        HPValue = myFont.render(str(HP),1,RED)
        HPLabel = myFont.render("HP: ", 1, RED)

    if HP < 1:
        GameOverScreen = myFont.render("YOU DIED!", 1, RED)
        LevelScreen = myFont.render(f"on Level {Level}", 1, white)
        ScoreScreen = myFont.render(f"Your score was {score}",1, white)
        HighScoreScreen = myFont.render(f"(Highscore {HighScore})",1,white)
        UserScreen = myFont.render(f"User: {user_name}", 1, white)

        screen.fill((0, 0, 0))
        screen.blit(GameOverScreen, (SCREEN_WIDTH - 380, 400))
        screen.blit(ScoreScreen, (SCREEN_WIDTH - 360, 430))
        screen.blit(HighScoreScreen, (SCREEN_WIDTH - 360, 460))
        screen.blit(LevelScreen, (SCREEN_WIDTH - 285, 400))
        screen.blit(UserScreen, (SCREEN_WIDTH - 330, 490))

        walking.stop()
        pygame.display.update()
        time.sleep(5)
        pygame.quit()
        sys.exit()


    if score > HighScore:
        HighScore = score
        HighScoreValue = myFont.render(str(HighScore),1,white)
    scoreValue = myFont.render(str(score),1,white)


    screen.blit(scoreLabel,(SCREEN_WIDTH - 142,2))
    # ^ Text
    screen.blit(scoreValue,(SCREEN_WIDTH - 85, 2))
    # ^ Score


    screen.blit(HighScoreLabel,(SCREEN_WIDTH - 185,30))
    # ^ Text
    screen.blit(HighScoreValue,(SCREEN_WIDTH - 85,30))
    # ^ Score

    screen.blit(HPLabel, (SCREEN_WIDTH - 590, 770))

    screen.blit(HPValue, (SCREEN_WIDTH - 555, 770))

    screen.blit(NameLabel, (SCREEN_WIDTH - 590, 10))

    screen.blit(NameValue, (SCREEN_WIDTH - 540, 10))

    screen.blit(LevelLabel, (SCREEN_WIDTH - 330, 10))

    screen.blit(LevelValue, (SCREEN_WIDTH - 275, 10))

    pygame.display.flip()

    clock.tick(30)
    # ^ Fps
