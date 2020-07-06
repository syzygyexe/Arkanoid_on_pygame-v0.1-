import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), "img")
snd_dir = path.join(path.dirname(__file__), "snd")

WIDTH = 1300
HEIGHT = 867
FPS = 60

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Initialize pygame/sound, create window/title, set clock
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Block Disintegrater")
clock = pygame.time.Clock()

# Define all Functions
def ball_speed_increase():
    if ball.speedx < 0 or ball.speedy < 0:
        ball.speedx += -5
        ball.speedy += -5
    elif ball.speedx > 0 or ball.speedy < 0:
        ball.speedx += 5
        ball.speedy += 5

def second_ball_speed_increase():
    if second_ball.speedx < 0 or second_ball.speedy < 0:
        second_ball.speedx += -5
        second_ball.speedy += -5
    elif second_ball.speedx > 0 or second_ball.speedy < 0:
        second_ball.speedx += 5
        second_ball.speedy += 5

# Define all classes
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
        self.image = self.spritesheet.get_image(613, 716, 166, 26).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0

    def update(self):
        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speedx = -45
        if keystate[pygame.K_RIGHT]:
            self.speedx = 45
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Blocks(pygame.sprite.Sprite):
    # x, y - Grid placement. 
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
        # Yellow Block / Red Block / Orange Block / Blue Block
        self.image = random.choice([self.spritesheet.get_image(564, 221, 82, 36), self.spritesheet.get_image(423, 221, 82, 36), 
                        self.spritesheet.get_image(132, 221, 82, 36), self.spritesheet.get_image(0, 221, 82, 36)]).convert()
        self.image.set_colorkey(WHITE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    # FIGURE OUT LATER ################################
    #def block_collision(self, xcl, xcr, yct, ycb):
        #self.rect.left = xcl
        #self.rect.right = xcr
        #self.rect.top = yct
        #self.rect.bototm = ycb
    

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
        self.image = self.spritesheet.get_image(204, 539, 26, 26).convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (14, 14))
        self.rect = self.image.get_rect()
        self.radius = 7
        # Check for hitbox when chaging the radius and size of the ball
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 800
        self.speedx = random.choice([-10, 10])
        self.speedy = 5
        self.vector_change = -1
    
    # FIGURE OUT LATER ################################
    # xcl, ycr - X-axis collision(Right/Left)
    # yct, ycb Y-axis collision(Top/Bottom)
    # def block_collision(self, xcl, xcr, yct, ycb):
     
    def update(self):
        self.rect.x += self.speedx*self.vector_change
        self.rect.y += self.speedy*self.vector_change
        if self.rect.left <= 0:
            self.speedx *= self.vector_change
        elif self.rect.right >= WIDTH:
            self.speedx *= self.vector_change
        elif self.rect.top <= 0:
            self.speedy *= self.vector_change
        elif self.rect.top >= HEIGHT:
            self.speedy *= self.vector_change

class Extra_ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
        self.image = self.spritesheet.get_image(204, 539, 26, 26).convert()
        self.image.set_colorkey(WHITE)
        self.image = pygame.transform.scale(self.image, (14, 14))
        self.rect = self.image.get_rect()
        self.radius = 7
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 800
        self.speedx = random.choice([-10, 10])
        self.speedy = 5
        self.vector_change = -1
     
    def update(self):
        self.rect.x += self.speedx*self.vector_change
        self.rect.y += self.speedy*self.vector_change
        if self.rect.left <= 0:
            self.speedx *= self.vector_change
        elif self.rect.right >= WIDTH:
            self.speedx *= self.vector_change
        elif self.rect.top <= 0:
            self.speedy *= self.vector_change
        elif self.rect.top >= HEIGHT:
            self.speedy *= self.vector_change

class Pow(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(["expander", "shrinker",
                                "shooting_paddle", "split_ball"])
        self.image = powerup_images[self.type]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT:
            self.kill()


class Spritesheet:
    # Utility class for loading and parsing spritesheets
    def __init__(self, filename):
        self.spritesheet = pygame.image.load(filename).convert()

    def get_image(self, x, y, width, height):
        # Grab an image out of a larget sprtiesheet
        image = pygame.Surface((width, height))
        # Take the chunk out of the "self.spritesheet", with the given (x,y,w,h)
        image.blit(self.spritesheet, (0, 0), (x, y, width, height))
        return image



# Load all game graphics
background = pygame.image.load(path.join(img_dir, "background.png")).convert()
background_rect = background.get_rect()

powerup_images = {}
powerup_images["expander"] = pygame.image.load(path.join(img_dir, "expander.png")).convert()
powerup_images["shrinker"] = pygame.image.load(path.join(img_dir, "shrinker.png")).convert()
powerup_images["shooting_paddle"] = pygame.image.load(path.join(img_dir, "shooting_paddle.png")).convert()
powerup_images["split_ball"] = pygame.image.load(path.join(img_dir, "split_ball.png")).convert()

# Load all game sounds
shrinker_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup.wav"))
expander_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup2.wav"))
new_ball_sound = pygame.mixer.Sound(path.join(snd_dir, "Powerup3.wav"))
gun_powerup = pygame.mixer.Sound(path.join(snd_dir, "Powerup4.wav"))
shoot_sound = pygame.mixer.Sound(path.join(snd_dir, "Laser_Shoot5.wav"))
collision_sounds = []
for snd in ["Pickup_coin10.wav", "Pickup_coin11.wav", "Pickup_coin12.wav", "Pickup_coin13.wav"]:
    collision_sounds.append(pygame.mixer.Sound(path.join(snd_dir, snd)))

pygame.mixer.music.load(path.join(snd_dir, "Fly.mp3"))
pygame.mixer.music.set_volume(0.2)
pygame.mixer.music.play(loops=-1)

# Define sprite groups
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
player = Player()
player.add(player_group)
ball_group = pygame.sprite.Group()
ball = Ball()
ball.add(ball_group)
second_ball_group = pygame.sprite.Group()
second_ball = Extra_ball()
powerups_group = pygame.sprite.Group()
all_sprites.add(player, ball)

blocks = pygame.sprite.Group()
# Block Grid (Starting, Ending point, Block itself + Gap)
for x in range(25, 1260, 90):
    for y in range(10, 421, 41):
        b = Blocks(x, y)
        blocks.add(b)
        all_sprites.add(b)


# Blocks collision groups # FIGURE OUT LATER ##############

# Other variables
# When collision count increases, speed of the ball increases
collision_count = 0
collision_count_second_ball = 0


# Game loop
running = True
while running:
    # Keep loop running at the right speed
    clock.tick(FPS)
    # 1) Process input (events)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # 2) Sprite update section
    all_sprites.update()

    # Collisions between objects
    # FIRST BALL
    hits_ball_block = pygame.sprite.spritecollide(ball, blocks, True, pygame.sprite.collide_circle)
    if hits_ball_block:
        random.choice(collision_sounds).play()
        ball.speedy *= ball.vector_change
        collision_count += 1
    for hit in hits_ball_block:
        if random.random() > 0.75:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups_group.add(pow)
        if collision_count in {100, 200, 300}:
            ball_speed_increase()

    hits_ball_player = pygame.sprite.groupcollide(ball_group, player_group, False, False)
    if hits_ball_player:
        random.choice(collision_sounds).play()
        ball.speedy *= ball.vector_change
        collision_count += 1
        if collision_count in {100, 200, 300}:
            ball_speed_increase()
    
    # SECOND BALL
    hits_second_ball_blocks = pygame.sprite.spritecollide(second_ball, blocks, True, pygame.sprite.collide_circle)
    if hits_second_ball_blocks:
        random.choice(collision_sounds).play()
        second_ball.speedy *= second_ball.vector_change
        collision_count_second_ball += 1
    for hit in hits_second_ball_blocks:
        if random.random() > 0.75:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups_group.add(pow)
        if collision_count_second_ball in {100, 200, 300}:
            second_ball_speed_increase()

    hits_second_ball_player = pygame.sprite.spritecollide(second_ball, player_group, False)
    if hits_second_ball_player:
        random.choice(collision_sounds).play()
        second_ball.speedy *= second_ball.vector_change
        collision_count_second_ball += 1
        if collision_count_second_ball in {100, 200, 300}:
            second_ball_speed_increase
    
    hits_powerup_player = pygame.sprite.groupcollide(powerups_group, player_group, True, False)
    for hit in hits_powerup_player:
        if hit.type == "expander":
            expander_sound.play()
            hit_center = hit.rect.center
            player.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
            player.image = player.spritesheet.get_image(563, 786, 216, 25).convert()
            player.rect = player.image.get_rect()
            player.image.set_colorkey(WHITE)
            # POSITION TO MAKE POWERUP WHERE IT ACTUALLY WAS HITED
            player.rect.centerx = hit.rect.x
            player.rect.bottom = HEIGHT - 10
        if hit.type == "split_ball":
            new_ball_sound.play()
            second_ball.add(second_ball_group)
            all_sprites.add(second_ball)
        if hit.type == "shrinker":
            shrinker_sound.play()
            hit_center = hit.rect.center
            player.spritesheet = Spritesheet(path.join(img_dir, "spritesheet.png"))
            player.image = player.spritesheet.get_image(664, 647, 115, 25).convert()
            player.rect = player.image.get_rect()
            player.image.set_colorkey(WHITE)
            # POSITION TO MAKE POWERUP WHERE IT ACTUALLY WAS HITED
            player.rect.centerx = hit.rect.x
            player.rect.bottom = HEIGHT - 10
        if hit.type == "shooting_paddle":
            pass


    # 3) Draw / Render section
    screen.fill(BLACK)
    # Background picture and its location(0, 0) by default
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # Background picture

    # After drawing everything, flip the display
    pygame.display.flip()

pygame.quit()
