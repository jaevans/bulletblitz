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
from actors import *

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
Guns = [MP412(), MP5(), Vector(), SV98(), M249(), AUG_A1(), M870()]
currentgun = 0
PlayerActor.gun = Guns[currentgun]
pickup = None
enemy = None
frames = 0

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
    clock.schedule(createenemy, random.randint(5,15))
    enemy.center = (random.randint(10, (FloorActor.width - 10) + FloorActor.left), random.randint(10, (FloorActor.height - 10) + FloorActor.top))
    enemies.append(enemy)

def update():
    global bullets
    global casings
    global enemies
    global canfire
    global triggerheld
    global canresetfire
    global pickup
    global frames
    
    frames += 1

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
        degs = e.angle_to(PlayerActor.pos)
        degs = (360 + (degs - e.angle)) % 360
        if degs > 10:
            if degs >180:
                e.angle -= 5
            elif degs <180:
                e.angle += 5
        if e.hp > 1:
            live_enemies.append(e)
        if e.distance_to(PlayerActor.center) > 75:
            e.forward(2)
        #if frames % 10 == 0:
            #e.forward(3)   
        #else:
            #e.forward(1)
    enemies = live_enemies

    for b in bullets:
        b.move()
        dist = b.distance_to(PlayerActor.center)
        for e in enemies:
            dist = b.distance_to(e.center)
            if dist < 24:
                e.hp -= PlayerActor.gun.dmg
            elif dist < b.range:
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

    if PlayerActor.gun.ammo == 0 and PlayerActor.gun.reloadscheduled == False:
            PlayerActor.gun.reloadscheduled = True
            clock.schedule(PlayerActor.gun.doreload, PlayerActor.gun.reload)
  
    if triggerheld == True and canfire == True and PlayerActor.gun.ammo > 0:
        b,c = PlayerActor.gun.fire(PlayerActor)
        bullets.extend(b)
        casings.extend(c)
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
    pygame.draw.rect(screen.surface, pygame.Color('#116d5d'), Rect(0, HEIGHT-100, 120, 100))
    if PlayerActor.gun.reloadscheduled == False:
        ptext.draw(str(PlayerActor.gun.ammo), center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
    elif PlayerActor.gun.reserve > 0:
        ptext.draw('Reloading', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
    elif PlayerActor.gun.reserve == 0:
        ptext.draw('0', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    ptext.draw('Ammo', center = (35, HEIGHT-50), color = '#c5c5c5', fontsize = 20 )
    ptext.draw('Reserve', center = (90, HEIGHT-50), color = '#c5c5c5', fontsize = 20)
    if PlayerActor.gun.__class__ == MP412:
        ptext.draw('Inf.', center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    else: 
        ptext.draw(str(PlayerActor.gun.reserve), center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    ptext.draw((str(PlayerActor.gun.__class__.__name__)).replace('_', ' '), center = (55, HEIGHT-75), color = '#c5c5c5', fontsize = 20)
    PlayerActor.draw()
    for e in enemies:
        e.draw()

clock.schedule(createpickup, 1)
clock.schedule(createenemy, random.randint(1,2))

pgzrun.go()
