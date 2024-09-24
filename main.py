from typing import Any
import pygame
# from os.path import join, dirname
from random import randint, uniform
import pygame.locals
from pygame.sprite import Group, Group
from pathlib import Path




class Player(pygame.sprite.Sprite):
    
    def __init__(self, groups):
        
        super().__init__(groups)
        self.image = pygame.image.load(base_path  / 'images' / 'player.png' ).convert_alpha()
        self.rect = self.image.get_rect(center = (win_width/2, win_height/2))
        self.direction = pygame.Vector2()
        self.speed = 300

        self.can_shoot = True
        self.laser_shoot_time = 0
        self.cooldown_duration = 100

        self.player_life = 3
        self.points = 0
        
        self.mask = pygame.mask.from_surface(self.image)
        


    def laser_time(self):
        if not self.can_shoot:
            current_time = pygame.time.get_ticks()
            if current_time - self.laser_shoot_time >= self.cooldown_duration:
                self.can_shoot = True

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.direction.x = int(keys[pygame.K_RIGHT]) - int(keys[pygame.K_LEFT]) #bool -> int:(1-0 -> Right, 0 - 1 -> Left)
        self.direction.y = int(keys[pygame.K_DOWN]) - int(keys[pygame.K_UP]) 
        self.direction = self.direction.normalize() if self.direction else self.direction
        self.rect.center += self.direction * self.speed * dt
      

class Laser(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(midbottom = pos)
      

        
    
    def update(self, dt):
        
        self.rect.centery -= 400 * dt
        if self.rect.bottom < 0:
            self.kill()
        
    
class Meteor(pygame.sprite.Sprite):

    def __init__(self, surf, pos, groups):
        super().__init__(groups)
        self.original_surf = surf
        self.image = surf
        self.rect = self.image.get_rect(center = pos)
        self.start_time = pygame.time.get_ticks()
        self.lifetime = 3000
        self.direction = pygame.Vector2(uniform(-0.5, 0.5), 1)
        self.speed =randint(400,500)
        self.rotation_speed = randint(40, 80)
        self.rotation = 0
        

    def update(self, dt):
        self.rect.center += self.direction * self.speed * dt
        if pygame.time.get_ticks() - self.start_time >= self.lifetime:
            self.kill()
        self.rotation += self.rotation_speed * dt
        self.image = pygame.transform.rotozoom(self.original_surf, self.rotation, 1)
        self.rect = self.image.get_rect(center = self.rect.center)


class AnimatedEx(pygame.sprite.Sprite):

    def __init__(self, frames, pos, groups):
        super().__init__(groups)
        self.frames = frames
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect(center = pos)
        explosion_sound.play()


    def update(self, dt) -> None:

        self.frame_index += 20 * dt
        if self.frame_index < len(self.frames):
            self.image = self.frames[int(self.frame_index) % len(self.frames)]
        else:
            self.kill()


def collisions():
    global gameplay
    

    collision_sprites = pygame.sprite.spritecollide(player, meteor_sprites, True)  
    if collision_sprites:
        damage_sound.play()
        player.player_life -= 1
        if player.player_life == 0:
            gameplay = False
            
        

    for laser in laser_sprites:
        collided_sprites =  pygame.sprite.spritecollide(laser, meteor_sprites, True, pygame.sprite.collide_mask)

        if collided_sprites:
            laser.kill()
            AnimatedEx(explosion_frames, laser.rect.midtop, all_sprites)
            player.points += 10


def display_score():
    current_time = (pygame.time.get_ticks() - start_time) // 100
    text_surf = font1.render(str(current_time), True, WHITE)
    text_rect = text_surf.get_rect(midbottom=(win_width / 2, win_height - 50))
    display_surface.blit(text_surf, text_rect)
    pygame.draw.rect(display_surface, WHITE, text_rect.inflate(20, 10).move(0, -2), 3, 10)


def player_life():
    text_surf = font1.render(f'Life:{str(player.player_life)}', True, WHITE)
    text_rect = text_surf.get_rect(topright=(win_width - 20,20))
    display_surface.blit(text_surf, text_rect)

def player_points():
    text_surf = font1.render(f'Points:{str(player.points)}', True, WHITE)
    text_rect = text_surf.get_rect(topright=(win_width - 20,60))
    display_surface.blit(text_surf, text_rect)

def game_score():

    lose_label = font2.render(f'END GAME!!! score:{player.points}', False, BLACK)
    lose_label_rect = lose_label.get_rect(topleft=(180,350))
    display_surface.blit(lose_label, lose_label_rect)



pygame.init()
win_width, win_height = 1280, 720
base_path = Path(__file__).parent
display_surface = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption('Galaxy Shooter')
pygame.display.set_icon(pygame.image.load(base_path / 'images' / 'logo.png').convert_alpha())
running = True 
gameplay = True
clock = pygame.time.Clock()


    

WHITE = (240,240,240)
BLACK = (0, 0, 0)
GREY = (115, 132, 148)


#import
fon_d = pygame.image.load(base_path  / 'images' / 'Fon1.jpg').convert_alpha()
meteor_surf = pygame.image.load(base_path / 'images'/ 'meteor.png').convert_alpha()
laser_surf = pygame.image.load(base_path/'images'/'laser.png').convert_alpha()
font1 = pygame.font.Font(base_path/'images'/ 'Oxanium-Bold.ttf', 40)
font2 = pygame.font.Font(base_path/'images'/'text.ttf', 40)
explosion_frames = [pygame.image.load(base_path  / 'images' / 'explosion'/ f'{i}.png').convert_alpha() for i in range(21)]
fon_2 = pygame.image.load(base_path/ 'images'/ 'Fon2.jpg').convert_alpha()

# sound
laser_sound = pygame.mixer.Sound(base_path/ 'audio'/ 'laser.wav')
laser_sound.set_volume(0.1)
explosion_sound = pygame.mixer.Sound(base_path/ 'audio'/'explosion.wav')
explosion_sound.set_volume(0.3)
damage_sound = pygame.mixer.Sound(base_path/ 'audio'/ 'damage.ogg')
game_music = pygame.mixer.Sound(base_path/ 'audio'/'Lobby.mp3')
game_music.set_volume(0.3)
game_music.play(loops = -1)

#sprite
all_sprites = pygame.sprite.Group()
meteor_sprites = pygame.sprite.Group()
laser_sprites = pygame.sprite.Group()
player = Player(all_sprites)

#game rest
restart_label = font2.render('Restart Game', False, BLACK)
rest_lab_rect = restart_label.get_rect(topleft=(180,400))

#custom events -> meteor event
meteor_event = pygame.event.custom_type()
pygame.time.set_timer(meteor_event, 500)

start_time = pygame.time.get_ticks()

bg = 0
#game(general) loop
while running:

    dt = clock.tick() / 1000
 
    #event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.can_shoot:
                    Laser(laser_surf, player.rect.midtop, (all_sprites, laser_sprites))
                    laser_sound.play()
                player.can_shoot = False
                player.laser_shoot_time = pygame.time.get_ticks()
        player.laser_time()

        if event.type == meteor_event:
            x, y = randint(0, win_width), randint(-200, -100)
            Meteor(meteor_surf, (x, y), (all_sprites, meteor_sprites))


    if gameplay:
        #draw the game 
        display_surface.blit(fon_d,(0, bg ))
        display_surface.blit(fon_d,(0, bg - 720))

        bg += 80 * dt
        if int(bg) == 720:
            bg = 0

        # update
        all_sprites.update(dt)
        collisions()
        display_score()
        player_life()
        player_points()
        all_sprites.draw(display_surface)

    else:
        display_surface.blit(fon_2, (0,0))
        game_score()
       
        display_surface.blit(restart_label, rest_lab_rect)

        game_music.stop()
        mouse = pygame.mouse.get_pos()
        if rest_lab_rect.collidepoint(mouse) and pygame.mouse.get_pressed()[0]:
            gameplay = True
            player.player_life = 3
            player.points = 0
            start_time = pygame.time.get_ticks()
            game_music.play()
            meteor_sprites.empty()
            laser_sprites.empty()
            
            player.rect = player.image.get_rect(center = (win_width/2, win_height/2))

    pygame.display.update()

#quit game
pygame.quit()