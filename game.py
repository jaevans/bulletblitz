import pgzrun
import pygame
import pygame.draw
import pgzero
import ptext
from pgzero.actor import Actor
from pgzero.keyboard import keyboard
from pgzero.keyboard import keys
import math
import pgzero.game as game
import random
from guns import *

def dot(A, B):
    return A[0] * B[0] + A[1] * B[1]

def magnitude(A):
    return math.sqrt(dot(A, A))

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

    def angleto(self, p):
        the_angle = math.radians(self._actor.angle)
        A = (self._actor.x + math.cos(the_angle), self._actor.y - math.sin(the_angle))
        #print(A)
        # B = ((self._actor.x + p[0]), (self._actor.y + p[1]))
        B = ((p[0]), (p[1]))
        #print(B)
        d = dot(A,B)
        m_a = magnitude(A)
        m_b = magnitude(B)
        print("d = %r, m_a = %r, m_b = %r" % (d, m_a, m_b))
        ret = math.degrees(math.acos(dot(A,B) / (magnitude(A) * magnitude(B))))
        #print(ret)
        return ret
        
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

class AmmoActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__('ammo_pickup', *args, **kwargs) 

class EnemyActor(TurtleActor):
    def __init__ (self, etype = None, *args, **kwargs):
        super().__init__('zombie_1', *args, **kwargs)
        self.hp = 100

ammosize = '9mm'

camera = Camera()
PlayerActor = TurtleActor('mp412_hold', camera = camera)
FloorActor = TurtleActor('floor', camera = camera)
bullets = []
casings = []
enemies = []
canfire = True 
triggerheld = False
canresetfire = True
PlayerActor.anchor = (23,23)
Guns = [MP412(), MP5(), Vector(), SV98(), M249(), AUGa1()]
currentgun = 0
PlayerActor.gun = Guns[currentgun]
pickup = None
enemy = None

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
    if key == keys.R and PlayerActor.gun.reloadscheduled == False and not PlayerActor.gun.reserve == 0:
        PlayerActor.gun.reloadscheduled = True
        clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)
    if key == keys.P:
        createpickup()

def createpickup():
    global pickup
    pickup = AmmoActor(camera = camera)
    clock.schedule(createpickup, random.randint(5,15))
    pickup.center = (random.randint(10, (FloorActor.width - 10) + FloorActor.left), random.randint(10, (FloorActor.height - 10) + FloorActor.top))

def createenemy():
    enemy = EnemyActor(camera = camera)
    clock.schedule(createpickup, random.randint(5,15))
    enemy.center = (random.randint(10, (FloorActor.width - 10) + FloorActor.left), random.randint(10, (FloorActor.height - 10) + FloorActor.top))
    enemies.append(e)

def update():
    global bullets
    global casings
    global canfire
    global triggerheld
    global canresetfire
    global pickup

    if pickup is not None and pickup.distance_to(PlayerActor.center) < 64:
        if not PlayerActor.gun.__class__ == MP412:
            if PlayerActor.gun.reserve < PlayerActor.gun.reservecap:
                pickup = None
                PlayerActor.gun.reserve += random.randint(round(PlayerActor.gun.capacity * 1.5), PlayerActor.gun.capacity * 3)

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
    live_enemies = []

    for e in enemies:
        angleto = enemy.angleto(PlayerActor.center)
        #print(angleto)
        enemy.angle = (angleto)
        #enemy.forward(10)
        # print(enemy.angle_to(PlayerActor.center)+enemy.angle)
        # if (enemy.angle_to(PlayerActor.center) + enemy.angle) % 360 > 5:
        #    enemy.angle += 3
        # elif (enemy.angle_to(PlayerActor.center)  + enemy.angle) % 360 < -5:
        #    enemy.angle -= 3

    for b in bullets:
        b.move()
        dist = b.distance_to(PlayerActor.center)
        if dist < b.range:
            live_bullets.append(b)
        for e in enemies:
            dist = b.distance_to(e.center)
            if dist < 23:
                
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

    if PlayerActor.gun.ammo == 0 and PlayerActor.gun.reloadscheduled == False:
            PlayerActor.gun.reloadscheduled = True
            clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)
  
    if triggerheld == True and canfire == True and PlayerActor.gun.ammo > 0:
        PlayerActor.gun.ammo -= 1

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
    
    if (not PlayerActor.gun.__class__ == MP412):
        if PlayerActor.gun.reserve > PlayerActor.gun.reservecap:
            PlayerActor.gun.reserve = PlayerActor.gun.reservecap

    camera.pos = (PlayerActor.x - (WIDTH//2), PlayerActor.y - (HEIGHT//2))

def draw():
    screen.fill('white')
    FloorActor.draw()
    for b in bullets:
        b.draw()
    for c in casings:
        c.draw()
    if not pickup == None:
        pickup.draw()
    if not enemy == None:
        enemy.draw()
    pygame.draw.rect(screen.surface, pygame.Color('#116d5d'), Rect(0, HEIGHT-75, 120, 75))
    if PlayerActor.gun.reloadscheduled == False:
        ptext.draw(str(PlayerActor.gun.ammo), center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
    elif PlayerActor.gun.reserve > 0:
        ptext.draw('Reloading', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
    elif PlayerActor.gun.reserve == 0:
        ptext.draw('0', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    ptext.draw('Ammo', center = (35, HEIGHT-50), color = '#c5c5c5', fontsize = 20 )
    ptext.draw('Reserve', center = (90, HEIGHT-50), color = '#c5c5c5', fontsize = 20)
    if PlayerActor.gun.__class__ == MP412:
        ptext.draw('Inf.', center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20 )
    else: 
        ptext.draw(str(PlayerActor.gun.reserve), center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20 )
    PlayerActor.draw()

clock.schedule(createpickup, 1)
clock.schedule(createenemy, random.randint(1,2))

pgzrun.go()
