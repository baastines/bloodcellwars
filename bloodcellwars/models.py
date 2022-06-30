from turtle import position
from pygame.math import Vector2
from utils import load_sprite
from pygame.transform import rotozoom
from utils import load_sprite, wrap_position, get_random_velocity, load_sound
import math, time
from pygame.locals import *
import pygame, random

UP = Vector2(0, -1)
DOWN = Vector2(0, 1)
LEFT = Vector2(-1, 0)
RIGHT = Vector2(1, 0)
ti = time.time()

class GameObject:

    def __init__(self, position, sprite, velocity):

        self.position = Vector2(position)
        self.sprite = sprite
        self.radius = sprite.get_width() / 2
        self.velocity = Vector2(velocity)

    def draw(self, surface):
        
        blit_position = self.position - Vector2(self.radius)

        surface.blit(self.sprite, blit_position)

    def move(self, surface):
        self.position = wrap_position(self.position + self.velocity, surface)

    def collides_with(self, other_obj):

        distance = self.position.distance_to(other_obj.position)

        return distance < self.radius + other_obj.radius

class TKillerCell(GameObject):

    MANEUVERABILITY = 3
    ACCELERATION = 0.25
    BULLET_SPEED = 6
    
    
    def __init__(self, position, create_bullet_callback):

        self.create_bullet_callback = create_bullet_callback
        self.directionforward = Vector2(UP)
        self.directionbackward = Vector2(DOWN)
        self.directionleftward = Vector2(LEFT)
        self.directionrightward = Vector2(RIGHT)

        super().__init__(position, load_sprite("lymphocytet"), Vector2(0))
        self.position = position
        self.zap_sound = load_sound("zap")
        
    def rotate(self, clockwise=True):
        sign = 1 if clockwise else -1
        angle = self.MANEUVERABILITY * sign
        self.directionforward.rotate_ip(angle)

    def draw(self, surface):

        angle = self.directionforward.angle_to(UP)
        rotated_surface = rotozoom(self.sprite, angle, 1.0)
        rotated_surface_size = Vector2(rotated_surface.get_size())
        blit_position = self.position - rotated_surface_size * 0.5
        surface.blit(rotated_surface, blit_position)
    
    def accelerate(self):

        self.velocity += self.directionforward

    def deaccelerate(self):

        self.velocity += self.directionbackward

    def accelerateleftward(self):

        self.velocity += self.directionleftward 

    def acceleraterightward(self):

        self.velocity += self.directionrightward 

    def shoot(self):
        bullet_velocity = self.directionforward * self.BULLET_SPEED + self.velocity
        bullet = Bullet(self.position, bullet_velocity)
        self.create_bullet_callback(bullet)
        self.zap_sound.play()
    
    def get_position(self):
        print (self.position)
        return self.position
        pass

class Virus(GameObject):
    def __init__(self, position, create_virus_callback, size=3):
        self.create_virus_callback = create_virus_callback

        self.size = size

        size_to_scale = {
            3: 1,
            2: 0.5,
            1: 0.25,
        }
        scale = size_to_scale[size]
        sprite = rotozoom(load_sprite("virus"), 0, scale)

        super().__init__(
            position, sprite, get_random_velocity(1, 3)
        )

    def split(self):
        if self.size > 1:
            for _ in range(2):
                virus = Virus(
                    self.position, self.create_virus_callback, self.size - 1
                )
                self.create_virus_callback(virus)

    #def move(self, surface):
        
    #    angle = math.atan2(TKillerCell.position.y-self.position.y, TKillerCell.position.x-self.position.x)
    #    self.normal = self.velocity.normalize()

    #    self.dx = math.cos(angle) * self.normal
    #    self.dy = math.sin(angle) * self.normal

    #    self.position.x = self.position.x + self.dx * self.normal
    #    self.position.y = self.position.y + self.dy * self.normal

class Bullet(GameObject):
    def __init__(self, position, velocity):
        super().__init__(position, load_sprite("bullet"), velocity)

        mx, my = pygame.mouse.get_pos()
        
        angle = math.atan2(my-self.position.y, mx-self.position.x)
        
        #print('Angle value:', int(angle*180/math.pi))
        self.dx = math.cos(angle) * self.velocity
        self.dy = math.sin(angle) * self.velocity
  
    def move(self, surface):

        bullspeed = self.velocity/math.pi
        self.position.x = self.position.x + self.dx * bullspeed
        self.position.y = self.position.y + self.dy * bullspeed