#Создай собственный Шутер!
from pygame import *
from random import *
mixer.init()

score = 0
lost = 0
win_width = 700
win_height = 500
finish = False

#создай окно игры
window = display.set_mode((win_width, win_height))
display.set_caption("Лабиринт")


#задай фон сцены
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))
mixer.music.load("space.ogg")

font.init()
font2 = font.SysFont("verdana", 36)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, x, y, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_d] and self.rect.x < 600:
            self.rect.x += self.speed
        elif keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed

    def fire(self):
        bullet = Bullet("bullet.png",self.rect.centerx, self.rect.top, 2)
        bullets.add(bullet)
        
ufo = sprite.Group()
class Enemy(GameSprite):
    def update(self):
        global lost
        global score
        self.rect.y += self.speed
        if self.rect.y >= 660:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)
            lost +=1

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

asteroids = sprite.Group()

class Asteroid(GameSprite):
    def update(self ):
        self.rect.y += self.speed
        if self.rect.y >= 660:
            self.rect.y = 0
            self.rect.x = randint(80, win_width - 80)




hero = Player("rocket.png",250,400, 2)
treasure = GameSprite("bullet.png", 550, 400, 0)

for i in range(1,20):
    enemy = Enemy("ufo.png", randint(0, 635), 0, randint(1,3))
    ufo.add(enemy)

for i in range(1,4):
    asteroid = Asteroid("asteroid.png", randint(0,635), 0, randint(1,3))
    asteroids.add(asteroid)

#создай 2 спрайта и размести их на сцене
game = True
mixer.music.play()
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()

    if not finish:
        window.blit(background, (0,0))
        text = font2.render("Счёт: " + str(score), 1, (255,255,255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255,255,255))
        window.blit(text_lose, (10, 40))
        hero.update()
        sprites_list = sprite.groupcollide(ufo, bullets, True, True)
        bullets.draw(window)
        bullets.update()
        hero.reset()
        treasure.reset()
        ufo.draw(window)
        ufo.update()
        asteroids.draw(window)
        asteroids.update()
        if sprites_list:
            score +=1
            enemy = Enemy("ufo.png", randint(0, 635), 0, randint(1,3))
            ufo.add(enemy)
        list1 = sprite.spritecollide(hero, asteroids, True)
        if list1:
            lose = font.SysFont("verdana", 36).render("Вы проиграли!", True, (124, 252, 0))
            window.blit(lose, (150,150))
            finish = True

        if lost > 40:
            lose = font.SysFont("verdana", 36).render("Вы проиграли!", True, (124, 252, 0))
            window.blit(lose, (150,150))
            finish = True

        if score > 50:
            win = font.SysFont("verdana", 36).render("Вы выиграли!", True, (124, 252, 0))
            window.blit(win, (150,150))
            finish = True


    display.update()

    time.delay(0)
#обработай событие «клик по кнопке "Закрыть окно"