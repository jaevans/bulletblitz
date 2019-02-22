import pgzrun
import pgzero
import math
import pgzero.game as game
import random

class Camera(object):
    def __init__(self):
        self.pos = (0,0)

    def camera_to_world(self, point):
        x = self.pos[0] + point[0]
        y = self.pos[1] + point[1]
        return (x,y)

    def world_to_camera(self, point):
        x = -self.pos[0] + point[0]
        y = -self.pos[1] + point[1]
        return (x,y)

class TurtleActor(object):
    def __init__(self, *args, **kwargs):
        self.__dict__['_actor'] = Actor(*args, **kwargs)
        self.__dict__['camera'] = kwargs['camera']
        
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
    
    def draw(self):
        newpos = self.camera.world_to_camera(self.topleft)
        game.screen.blit(self._surf, newpos)

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

camera = Camera()
PlayerActor = TurtleActor('mp412_hold', camera = camera)
FloorActor = TurtleActor('floor', camera = camera)
Bullet = BulletActor(0, camera = camera)

WIDTH = 750
HEIGHT = 750

PlayerActor.pos = (WIDTH/2, HEIGHT/2)

def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(camera.camera_to_world(pos))

def update():
    if keyboard[keys.W]:
        PlayerActor.y = max(PlayerActor.y - 5, FloorActor.top)
    if keyboard[keys.A]:
        PlayerActor.x = max(PlayerActor.x - 5, FloorActor.left)
    if keyboard[keys.S]:
        PlayerActor.y = min(PlayerActor.y + 5, FloorActor.bottom)
    if keyboard[keys.D]:
        PlayerActor.x = min(PlayerActor.x + 5, FloorActor.right)
    
    camera.pos = (PlayerActor.x - (WIDTH//2), PlayerActor.y - (HEIGHT//2))

def draw():
    screen.fill('white')
    FloorActor.draw()
    PlayerActor.draw()
    Bullet.draw()

pgzrun.go()