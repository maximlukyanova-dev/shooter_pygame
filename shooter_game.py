from pygame import *
from random import randint
from time import time as timer
win_w = 700
win_h = 500
window = display.set_mode((win_w, win_h))
display.set_caption("Shooter")
FPS = 60
background = transform.scale(image.load("galaxy.jpg"), (700, 500))
lost = 0
kill = 0
life = 3
level = 1
m = [1,2,3,5,8,13,21,34,55]
a = [1,1,2,3,5,8,13,21,34]
class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, s, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w,h))
        self.s = s
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.s
        if keys[K_RIGHT] and self.rect.x < win_w - 70:
            self.rect.x += self.s
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 15, 20)
        bullets.add(bullet)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.s
        global lost
        if self.rect.y > win_h:
            self.s = randint(2,5)
            self.rect.x = randint(0, win_w-80)
            self.rect.y = 0
            lost += 1
class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.s
        if self.rect.y > win_h:
            self.s = randint(2,5)
            self.rect.x = randint(0, win_w-80)
            self.rect.y = 0
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.s
        if self.rect.y < 0:
            self.kill()
mixer.init()
mixer.music.load("space.ogg")
mixer.music.set_volume(0.1)
mixer.music.play()
shoot = mixer.Sound("fire.ogg")
player = Player("rocket.png", 315, 400, 5, 70, 100)
monsters = sprite.Group()
for i in range(m[level]):
    monster = Enemy("ufo.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
    monsters.add(monster)
asteroids = sprite.Group()
for i in range(a[level]):
    asteroid = Asteroid("asteroid.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
    asteroids.add(asteroid)
bullets = sprite.Group()
game = True
font.init()
font36 = font.SysFont("Calibri", 36)
font70 = font.SysFont("Calibri", 70)
win = font70.render("YOU WIN!", True, (255, 215, 0))
lose = font70.render("YOU LOSE!", True, (128,0,0)) 
finish = False
rel_time = False
num_fire = 0
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN and e.key == K_SPACE or e.type == MOUSEBUTTONDOWN:
            if num_fire < 5 and rel_time == False:
                num_fire += 1
                player.fire()
                shoot.play()
            if num_fire >= 5 and rel_time == False:
                last_time = timer()
                rel_time = True
    if finish == False:
        window.blit(background, (0,0))
        player.reset()
        player.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        bullets.draw(window)
        bullets.update()
        text_lose = font36.render("Missed: " + str(lost), 1, (255, 255, 255))
        text_kill = font36.render("Killed: " + str(kill), 1, (255, 255, 255))
        window.blit(text_lose, (10,20))
        window.blit(text_kill, (10,50))
        if life == 0 or lost > 10:
            window.blit(lose, (200,200))
            finish = True
        if kill > 15:
            window.blit(win, (200,200))
            finish = True
        sprites_lists = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_lists:
            kill += 1
            monster = Enemy("ufo.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
            monsters.add(monster)
        if sprite.spritecollide(player, monsters, False) or sprite.spritecollide(player, asteroids, False):
            m_c = sprite.spritecollide(player, monsters, True)
            a_c = sprite.spritecollide(player, asteroids, True)
            for i in m_c:
                life -= 1
                monster = Enemy("ufo.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
                monsters.add(monster)
            for i in a_c:
                life -= 1
                asteroid = Asteroid("asteroid.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
                asteroids.add(asteroid)
        if life == 3:
            life_color = (0, 128, 0)
        if life == 2:
            life_color = (128, 128, 0)
        if life == 1:
            life_color = (128, 0, 0)
        text_life = font36.render(str(life), 1, life_color)
        window.blit(text_life, (650, 10))
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font36.render("Wait, reaload...", 1, (150, 0, 0))
                window.blit(reload, (260, 460))
            else:
                num_fire = 0
                rel_time = False
        display.update()
    else:
        level += 1
        kill = 0
        lost = 0
        num_file = 0
        life = 3
        finish = False
        for i in bullets:
            i.kill()
        for i in monsters:
            i.kill()
        for i in asteroids:
            i.kill()
        for i in range(m[level]):
            monster = Enemy("ufo.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
            monsters.add(monster)
        for i in range(a[level]):
            asteroid = Asteroid("asteroid.png", randint(0, win_w-80), 0, randint(2,4), 80, 50)
            asteroids.add(asteroid)
        time.delay(3000)
    time.delay(50)