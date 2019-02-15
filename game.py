import pgzrun
import pgzero
from pgzero.actor import Actor
from pgzero.keyboard import keyboard, keys
import pygame
import pgzero.game as game
import pygame.display
import math
import random

class Camera(object):
    def __init__(self, pos=(0,0)):
        self.pos = pos

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, x):
        self._x = x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, y):
        self._y = y

    @property
    def pos(self):
        return (self._x, self._y)
    
    @pos.setter
    def pos(self, pos):
        self._x, self._y = pos

    def screen_to_world(self, world_point):
        world_x, world_y = world_point
        screen_x = world_x + self.x - (WIDTH // 2)
        screen_y = world_y + self.y - (HEIGHT // 2)
        return (screen_x,screen_y)

    def world_to_screen(self, screen_point):
        screen_x, screen_y = screen_point

        world_x = screen_x - self.x + (WIDTH // 2)
        world_y = screen_y - self.y + (HEIGHT // 2)
        return (world_x, world_y)

class TurtleActor(object):
    def __init__(self, *args, **kwargs):
        self.__dict__['_actor'] = Actor(*args, **kwargs)
        self.__dict__['camera'] = kwargs['camera']
        del kwargs['camera']
        
    def __getattr__(self, attr):
        if attr in self.__dict__:
            return object.__getattribute__(self, attr)
        else:
            return getattr(self.__dict__['_actor'], attr)
            
    def __setattr__(self, attr, value):
        if attr in self.__dict__:
            return object.__setattribute__(self, attr, value)
        else:
            return setattr(self._actor, attr, value)
        
    def forward(self, distance):
        the_angle = math.radians(self._actor.angle)
        self._actor.x += distance * math.cos(the_angle)
        # We subtract the y as our y gets bigger heading downward
        self._actor.y -= distance * math.sin(the_angle)
        
    def backward(self, distance):
        self.forward(-distance)
        
    def turnleft(self, angle):
        self._actor.angle += angle
    
    def turnright(self, angle):
        self._actor.angle -= angle

    def draw(self, camera):
        screen_pos = self.camera.world_to_screen(self.topleft)
        game.screen.blit(self._surf, screen_pos)

SPREAD = 5

class BulletActor(TurtleActor):
    def __init__ (self, angle, *args, **kwargs):
        super().__init__('9mm_bullet', *args, **kwargs)
        self.angle = angle + ((random.random()* SPREAD) - SPREAD / 2)
        self.dmg = 1

    def move(self):
        self.forward(15)

    #def onscreen(self):
       # screenrect = Rect((0,0), (screen.width, screen.height))
       # return screenrect.contains(self._rect)

ammosize = '9mm'
gun = 'mp412'

HEIGHT = 750
WIDTH = HEIGHT * 16 // 9

camera = Camera()
PlayerActor = TurtleActor('mp412_hold', camera=camera)
FloorActor = TurtleActor('floor', camera=camera)
Bullet = BulletActor(0, camera=camera)

PlayerActor.pos = (FloorActor.right//2, FloorActor.bottom//2)

print(pygame.display.list_modes())
info = pygame.display.Info()
print(info)
print(pygame.display.get_wm_info())



def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(camera.screen_to_world(pos))

def update():
    global camera
    if keyboard[keys.W]:
        PlayerActor.y = max(PlayerActor.y - 5, FloorActor.top)
    if keyboard[keys.A]:
        PlayerActor.x = max(PlayerActor.x - 5, FloorActor.left)
    if keyboard[keys.S]:
        PlayerActor.y = min(PlayerActor.y + 5, FloorActor.bottom)
    if keyboard[keys.D]:
        PlayerActor.x = min(PlayerActor.x + 5, FloorActor.right)

    # Always move the camera to the location of the player
    camera.pos = PlayerActor.center


def draw():
    screen.fill('white')
    FloorActor.draw(camera)
    PlayerActor.draw(camera)
    Bullet.draw(camera)

pgzrun.go()