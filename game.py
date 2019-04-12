import pgzrun
import pgzero
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.keyboard import keys
#from pgzero.game import screen
import math
import pgzero.game as game
import random
from guns import *

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

class BulletActor(TurtleActor):
    def __init__ (self, angle, *args, **kwargs):
        super().__init__('9mm_bullet', *args, **kwargs)
        self.dmg = PlayerActor.gun.dmg
        self.velocity = PlayerActor.gun.velocity
        self.range = PlayerActor.gun.range
        self.spread = PlayerActor.gun.spread
        self.angle = angle + ((random.random()* self.spread) - self.spread / 2)
        

    def move(self):
        self.forward(self.velocity)

    #def onscreen(self):
       # screenrect = Rect((0,0), (screen.width, screen.height))
       # return screenrect.contains(self._rect)

class PlayerActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gun = None
        
class CasingActor(TurtleActor):
    def __init__ (self, angle, *args, **kwargs):
        super().__init__('9mm_case', *args, **kwargs)
        self.angle = angle
    
    def move(self):
        self.forward(10)

ammosize = '9mm'

camera = Camera()
PlayerActor = TurtleActor('mp412_hold', camera = camera)
FloorActor = TurtleActor('floor', camera = camera)
#CasingActor = TurtleActor('9mm_case', camera = camera)
bullets = []
casings = []
canfire = True 
triggerheld = False
canresetfire = True
PlayerActor.anchor = (23,23)
Guns = [MP412(), MP5(), Vector(), SV98(), M249(), AUGa1()]
currentgun = 0
PlayerActor.gun = Guns[currentgun]

WIDTH = 750
HEIGHT = 750
SPEED = 10

PlayerActor.pos = (WIDTH/2, HEIGHT/2)

def resetfire():
    global canfire
    global canresetfire
    if PlayerActor.gun.firemode == 'auto':
        canfire = True
        canresetfire = False
    elif PlayerActor.gun.firemode == 'semi':
        if triggerheld == False:
            canfire = True
            canresetfire = False

def canresetfiretrue():
    global canresetfire
    canresetfire = True

def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(camera.camera_to_world(pos))

def on_mouse_down(pos, button):
    global triggerheld
    global currentgun
    triggerheld = True
    if button == mouse.WHEEL_DOWN:
        saveangle = PlayerActor.angle
        currentgun = (currentgun + 1)%len(Guns)
        PlayerActor.gun = Guns[currentgun]
        PlayerActor.image = PlayerActor.gun.image
        PlayerActor.angle = saveangle

def on_mouse_up(pos, button):
    global triggerheld
    triggerheld = False

def update():
    global bullets
    global casings
    global canfire
    global triggerheld
    global canresetfire

    if keyboard[keys.W]:
        PlayerActor.y = max((PlayerActor.y - SPEED + PlayerActor.gun.holdslow), FloorActor.top)
    if keyboard[keys.A]:
        PlayerActor.x = max((PlayerActor.x - SPEED + PlayerActor.gun.holdslow), FloorActor.left)
    if keyboard[keys.S]:
        PlayerActor.y = min((PlayerActor.y + SPEED - PlayerActor.gun.holdslow), FloorActor.bottom)
    if keyboard[keys.D]:
        PlayerActor.x = min((PlayerActor.x + SPEED - PlayerActor.gun.holdslow), FloorActor.right)
    live_bullets = []
    live_casings = []

    for b in bullets:
        b.move()
        dist = b.distance_to(PlayerActor.center)
        if dist < b.range:
            live_bullets.append(b)
    bullets = live_bullets

    for c in casings:
        dist = c.distance_to(PlayerActor.center)
        if dist < 100:
            c.move
            live_casings.append(c)
        casings = live_casings
     
    if canresetfire == True:
        resetfire()
    
    if triggerheld == True and canfire == True:
        b = BulletActor(PlayerActor.angle, camera = camera, center = PlayerActor.center)
        bullets.append(b)
        c = CasingActor(PlayerActor.angle + 90, camera = camera, center = PlayerActor.center)
        casings.append(c)
        canfire = False
        clock.schedule(canresetfiretrue, round(60/PlayerActor.gun.rpm, 2))
    
    camera.pos = (PlayerActor.x - (WIDTH//2), PlayerActor.y - (HEIGHT//2))

def draw():
    screen.fill('white')
    FloorActor.draw()
    for b in bullets:
        b.draw()
    for c in casings:
        c.draw()
    PlayerActor.draw()

pgzrun.go()