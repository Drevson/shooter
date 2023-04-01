#Создай собственный Шутер!

from pygame import *
from random import randint

#фоновая музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

font.init()
font1 = font.Font(None, 70)
font2 = font.Font(None, 36)
score = 0
lost = 0
win = font1.render("YOU WIN", True, (230,120,46))
lose = font1.render("YOU LOSE", True, (230,120,46))

#картинки:
img_back = "galaxy.jpg" #фон игры
img_hero = "rocket.png" #герой
img_enemy = "ufo.png" # враг
img_bullet = 'bullet.png' #пуля
img_asteroid = 'asteroid.png' #астероид

class GameSprite(sprite.Sprite):
    #конструктор класса
    def __init__(self, player_image, player_x, player_y, player_speed):
        #Вызываем конструктор класса (Sprite):
        super().__init__()

        #каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (65,65))
        self.speed = player_speed

        #каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    #метод, отрисовывающий героя на окне
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    #метод для управления спрайтом стрелками клавиатуры
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self. rect.top, -15) 
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost = lost + 1

class Bullet(GameSprite):
    def __init__(self, player_image, player_x, player_y, player_speed): 
        super().__init__(player_image, player_x, player_y, player_speed) 
        self.image = transform.scale(image.load(player_image), (15,15))
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

win_width = 700
win_height = 500
FPS = 60
display.set_caption("Shooter")
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
clock = time.Clock()

ship = Player(img_hero, 5, win_height - 100, 10)

monsters = sprite.Group()
for i in range(1,6):
    monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 3))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    asteroid = Enemy(img_asteroid, randint(80, win_width-80), -40, randint(1,7)) 
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
num_fire = 0
rel_time = False

run = True #флаг сбрасывается кнопкой закрытия окна
while run:
    #событие нажатия на кнопку Закрыть
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN: 
            if num_fire < 5 and rel_time == False: 
                num_fire += 1 
                fire_sound.play()
                ship.fire()
            if e.key == K_SPACE: 
                fire_sound.play() 
                ship.fire()
    if not finish:
        #обновляем фон
        window.blit(background,(0,0))
        text = font2.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
        text_lose = font2.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))
        ship.update()
        monsters.update()
        bullets.update()
        asteroids.update()
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)
        if rel_time == True:
            now_timer = timer()
            if now_timer - last_time < 3:
                reload = font2.render("RELOAD", True, (150,0,0))
                window.blit(reload, (350, 500))
            else:
                num_fire = 0
                rel_time = False
        asteroids.draw(window)
        collides = sprite.groupcollide(monsters, bullets, True, True) 
        for c in collides:
            score += 1
            monster = Enemy(img_enemy, randint(80, win_width - 80), -40, randint(1, 3)) 
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, True):
            finish = True
            window.blit(lose, (200,200))
        display.update()

    clock.tick(FPS)

