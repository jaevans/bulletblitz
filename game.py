import pgzrun
import pgzero
import pgzero.game as game
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

class TurtleActor(object):
    def __init__(self, *args, **kwargs):
        self.__dict__['_actor'] = Actor(*args, **kwargs)
        
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
        pos = (self.topleft[0] - camera.x, self.topleft[1] - camera.y)
        game.screen.blit(self._surf, pos)

SPREAD = 5

class BulletActor(TurtleActor):
    def __init__ (self, angle):
        super().__init__('9mm_bullet')
        self.angle = angle + ((random.random()* SPREAD) - SPREAD / 2)
        self.dmg = 1

    def move(self):
        self.forward(15)

    #def onscreen(self):
       # screenrect = Rect((0,0), (screen.width, screen.height))
       # return screenrect.contains(self._rect)

ammosize = '9mm'
gun = 'mp412'

PlayerActor = TurtleActor('mp412_hold')
FloorActor = TurtleActor('floor')
Bullet = BulletActor(0)

WIDTH = 750
HEIGHT = 750

PlayerActor.pos = (WIDTH/2, HEIGHT/2)
camera = Camera((0,0))

def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(pos)

def update():
    if keyboard[keys.W]:
        FloorActor.y = max(FloorActor.y +5, 0)
    if keyboard[keys.A]:
        FloorActor.x = max(FloorActor.x +5, 0)
    if keyboard[keys.S]:
        FloorActor.y = FloorActor.y - 5
    if keyboard[keys.D]:
        FloorActor.x = FloorActor.x - 5

def draw():
    screen.fill('white')
    FloorActor.draw(camera)
    PlayerActor.draw(camera)
    Bullet.draw(camera)

pgzrun.go()