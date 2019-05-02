import pgzrun
import pgzero
import ptext
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.keyboard import keys
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

class PlayerActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gun = None
        
class CasingActor(TurtleActor):
    def __init__ (self, angle, *args, **kwargs):
        super().__init__('9mm_case', *args, **kwargs)
        self.angle = angle
        self.alive = True
        self.flying = True

    def killtimer(self):
        self.alive = False

    def stopfly(self):
        self.flying = False
    
    def move(self):
        self.forward(10)

ammosize = '9mm'

camera = Camera()
PlayerActor = TurtleActor('mp412_hold', camera = camera)
FloorActor = TurtleActor('floor', camera = camera)
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
SPEED = 15

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
        clock.unschedule(PlayerActor.gun.doreload)
        PlayerActor.gun.reloadscheduled = False
        currentgun = (currentgun + 1)%len(Guns)
        PlayerActor.gun = Guns[currentgun]
        PlayerActor.image = PlayerActor.gun.image
        PlayerActor.angle = saveangle
        if PlayerActor.gun.ammo == 0:
           clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)

   
    if button == mouse.WHEEL_UP:
        saveangle = PlayerActor.angle
        clock.unschedule(PlayerActor.gun.doreload)
        PlayerActor.gun.reloadscheduled = False
        currentgun = (currentgun - 1)%len(Guns)
        PlayerActor.gun = Guns[currentgun]
        PlayerActor.image = PlayerActor.gun.image
        PlayerActor.angle = saveangle
        if PlayerActor.gun.ammo == 0:
           clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)


def on_mouse_up(pos, button):
    global triggerheld
    triggerheld = False

def on_key_down(key, mod, unicode):
    if key == keys.R and PlayerActor.gun.reloadscheduled == False:
        PlayerActor.gun.reloadscheduled = True
        clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)

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
        clock.schedule(c.stopfly, (random.randint(0,50)/1000) + .075)
        if c.alive:
            live_casings.append(c)
        if c.flying:
            c.move()
        else:
            clock.schedule(c.killtimer, 15)
        casings = live_casings
     
    if canresetfire == True:
        resetfire()
  
    if triggerheld == True and canfire == True and PlayerActor.gun.ammo > 0:
        PlayerActor.gun.ammo -= 1
        if PlayerActor.gun.ammo == 0:
           clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)

        d = PlayerActor._orig_surf.get_size()[0]
        the_angle = math.radians(PlayerActor.angle)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        m = ((PlayerActor.x + x), (PlayerActor.y + y))
       
        b = BulletActor(PlayerActor.angle, camera = camera, center = m)
        bullets.append(b)
        
        d = 30
        the_angle = math.radians(PlayerActor.angle)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        p = ((PlayerActor.x + x), (PlayerActor.y + y))

        d = 5 + random.randint(0,20)
        the_angle = math.radians(PlayerActor.angle - 90)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        m = ((x + p[0]), (y + p[1]))
        
        c = CasingActor(PlayerActor.angle -90 + random.randint(-2,2), camera = camera, center = m)
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
    ptext.draw(str(PlayerActor.gun.ammo), center = (50, HEIGHT-50), color = '#767676' ) 

pgzrun.go()