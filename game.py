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
grenades = []
canFire = True 
canResetFire = True
triggertemp = False
PlayerActor.anchor = (23,23)
Guns = [MP412(), MP5(), Vector(), SV98(), M249(), AUG_A1(), M870(), AA12()]
Throwables = [Grenade()]
previousWeapon = Throwables[0]
currentGun = 0
PlayerActor.weapon = Guns[currentGun]
pickup = None
enemy = None
gunitem = None
frames = 0
weaponTypeSelected = 'gun'
WIDTH = 750
HEIGHT = 750
SPEED = 15
mouse_buttons = [False] * (mouse.WHEEL_DOWN + 1)

PlayerActor.pos = (WIDTH/2, HEIGHT/2)

def resetfire():
    global canFire
    global canResetFire
    if isinstance(PlayerActor.weapon, Gun):
        if PlayerActor.weapon.firemode == 'auto':
            canFire = True
            canResetFire = False
        elif PlayerActor.weapon.firemode == 'semi':
            if PlayerActor.weapon.triggerHeld == False:
                canFire = True
                canResetFire = False

def canResetFiretrue():
    global canResetFire
    canResetFire = True

def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(camera.camera_to_world(pos))

def on_mouse_down(pos, button):
    global currentGun
    global triggertemp
    mouse_buttons[button] = True
    triggertemp = True
    PlayerActor.weapon.triggerHeld = True
  
    if button == mouse.WHEEL_DOWN:
        saveangle = PlayerActor.angle
        if isinstance(PlayerActor.weapon, Gun):
            clock.unschedule(PlayerActor.weapon.doReload)
            PlayerActor.weapon.reloadScheduled = False
            currentGun = (currentGun + 1)%len(Guns)
            PlayerActor.weapon = Guns[currentGun]
            PlayerActor.image = PlayerActor.weapon.holdimage
            PlayerActor.angle = saveangle
            if PlayerActor.weapon.ammo == 0:
                clock.schedule(PlayerActor.weapon.doReload, PlayerActor.weapon.reload)

   
    if button == mouse.WHEEL_UP:
        saveangle = PlayerActor.angle
        if isinstance(PlayerActor.weapon, Gun):
            clock.unschedule(PlayerActor.weapon.doReload)
            PlayerActor.weapon.reloadScheduled = False
            currentGun = (currentGun - 1)%len(Guns)
            PlayerActor.weapon = Guns[currentGun]
            PlayerActor.image = PlayerActor.weapon.holdimage
            PlayerActor.angle = saveangle
            if PlayerActor.weapon.ammo == 0:
                clock.schedule(PlayerActor.weapon.doReload, PlayerActor.weapon.reload)

def on_mouse_up(pos, button):
    global triggertemp
    mouse_buttons[button] = False
    triggertemp = True
    PlayerActor.weapon.triggerHeld = False

def on_key_down(key, mod, unicode):
    global weaponTypeSelected
    global previousWeapon
    if isinstance(PlayerActor.weapon, Gun):
        if key == keys.R and PlayerActor.weapon.reloadScheduled == False and not PlayerActor.weapon.reserve == 0:
            PlayerActor.weapon.reloadScheduled = True
            clock.schedule(PlayerActor.weapon.doReload, PlayerActor.weapon.reload)
    if key == keys.G:
        saveangle = PlayerActor.angle
        t = previousWeapon
        previousWeapon = PlayerActor.weapon
        PlayerActor.weapon = t
        PlayerActor.image = PlayerActor.weapon.holdimage
        PlayerActor.angle = saveangle

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

def creategun():
    global gunitem
    try:
        gunitem = GunActor(camera = camera)
        gunitem.center = (random.randint(10, (FloorActor.width - 10) + FloorActor.left), random.randint(10, (FloorActor.height - 10) + FloorActor.top))
    except:
        pass
    clock.schedule(creategun, random.randint(5,5))

def update():
    global bullets
    global casings
    global enemies
    global grenades
    global canFire
    global canResetFire
    global pickup
    global frames
    global triggertemp

    frames += 1

    if pickup is not None and pickup.distance_to(PlayerActor.center) < 64 and isinstance(PlayerActor.weapon, Gun):
        if not PlayerActor.weapon.__class__ == MP412:
            if PlayerActor.weapon.reserve < PlayerActor.weapon.reservecap:
                pickup = None
                PlayerActor.weapon.reserve += random.randint(round(PlayerActor.weapon.capacity * 1.5), PlayerActor.weapon.capacity * 3)

    if keyboard[keys.W]:
        PlayerActor.y = max((PlayerActor.y - SPEED + PlayerActor.weapon.holdslow), FloorActor.top)
    if keyboard[keys.A]:
        PlayerActor.x = max((PlayerActor.x - SPEED + PlayerActor.weapon.holdslow), FloorActor.left)
    if keyboard[keys.S]:
        PlayerActor.y = min((PlayerActor.y + SPEED - PlayerActor.weapon.holdslow), FloorActor.bottom)
    if keyboard[keys.D]:
        PlayerActor.x = min((PlayerActor.x + SPEED - PlayerActor.weapon.holdslow), FloorActor.right)
    if isinstance(PlayerActor.weapon, Throwable):
        if triggertemp == True:
            # If the user just pressed/released the mouse
            if mouse_buttons[mouse.LEFT]:
                # they just pressed the left button
                saveangle = PlayerActor.angle
                PlayerActor.image = PlayerActor.weapon.chargeimage
                if PlayerActor.weapon.power >= 0:
                    PlayerActor.weapon.power = 10
                    PlayerActor.weapon.increasepower()
                PlayerActor.angle = saveangle
            else:
                # they released some button, but I don't know what
                g = PlayerActor.weapon.throw(PlayerActor)
                grenades.append(g)
                
        else:
            if mouse_buttons[mouse.LEFT]:
                # The user is *holding* down the left button for at least 1 frame
                saveangle = PlayerActor.angle
                PlayerActor.image = PlayerActor.weapon.chargeimage
                PlayerActor.angle = saveangle
            else:
                # the left mouse button is not pressed
                saveangle = PlayerActor.angle
                PlayerActor.image = PlayerActor.weapon.holdimage
                PlayerActor.angle = saveangle
                if isinstance(PlayerActor.weapon, Throwable):
                    PlayerActor.weapon.power = 0
    
    live_bullets = []
    live_casings = []
    live_enemies = []
    live_grenades = []

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
    enemies = live_enemies

    for b in bullets:
        b.move()
        dist = b.distance_to(PlayerActor.center)
        for e in enemies:
            dist = b.distance_to(e.center)
            if dist < 36:
                crit = random.randint(1, 10)
                if crit == 1:
                    e.hp -= PlayerActor.weapon.dmg * PlayerActor.weapon.critmult
                    e.backward(PlayerActor.weapon.knockback  * 1.5)
                else:
                    e.hp -= PlayerActor.weapon.dmg
                    e.backward(PlayerActor.weapon.knockback)
            elif dist < b.range:
                live_bullets.append(b)
        dist = b.distance_to(PlayerActor.center)
        if isinstance(PlayerActor.weapon, Gun) and (len(enemies) == 0) and (dist < PlayerActor.weapon.range):
           live_bullets.append(b)
       
    bullets = live_bullets

    for g in grenades:
        g.move()
        for e in enemies:
            dist = e.distance_to(g.center)
            if dist < 32 and g.image == g.explodeimage:
                e.hp -= 15
        if g.alive == True:
            live_grenades.append(g)
    
    grenades = live_grenades

    for c in casings:
        clock.schedule(c.stopfly, (random.randint(0,50)/1000) + 1.0)
        if c.alive:
            live_casings.append(c)
        if c.flying:
            c.move()
            #c.x += 5 * math.cos(c.moveangle)
            #c.y -= 5 * math.sin(c.moveangle)
            #c.turnleft(15)
        else:
            clock.schedule(c.killtimer, 15)
        casings = live_casings
     
    if canResetFire == True:
        resetfire()
    if isinstance(PlayerActor.weapon, Gun):
        if PlayerActor.weapon.ammo == 0 and PlayerActor.weapon.reloadScheduled == False:
                #if not PlayerActor.weapon.ejectsonfire:
                 #   for i in range (PlayerActor.weapon.capacity):
                  #      c = CasingActor(self, (PlayerActor.angle - 90.0) + random.randint(-2,2), camera = PlayerActor.camera, center = m)
                   #     casings.append(c)
                PlayerActor.weapon.reloadScheduled = True
                clock.schedule(PlayerActor.weapon.doReload, PlayerActor.weapon.reload)
    
        if PlayerActor.weapon.triggerHeld == True and canFire == True and PlayerActor.weapon.ammo > 0:
            projectiles = PlayerActor.weapon.fire(PlayerActor)
            bullets.extend(projectiles[0])
            if len(projectiles) > 1:
                casings.extend(projectiles[1])
            canFire = False
            clock.schedule(canResetFiretrue, round(60/PlayerActor.weapon.rpm, 2))
        
        if (not PlayerActor.weapon.__class__ == MP412):
            if PlayerActor.weapon.reserve > PlayerActor.weapon.reservecap:
                PlayerActor.weapon.reserve = PlayerActor.weapon.reservecap

    triggertemp = False
    camera.pos = (PlayerActor.x - (WIDTH//2), PlayerActor.y - (HEIGHT//2))

def draw():
    screen.fill('white')
    FloorActor.draw()
    if gunitem is not None:
        gunitem.draw()
    for b in bullets:
        b.draw()
    for c in casings:
        if c.moves > 25:
            c.draw()
    for g in grenades:
        g.draw()
    if pickup is not None:
        pickup.draw()
    pygame.draw.rect(screen.surface, pygame.Color('#116d5d'), Rect(0, HEIGHT-100, 120, 100))
    if isinstance(PlayerActor.weapon, Gun):
        if PlayerActor.weapon.reloadScheduled == False:
            ptext.draw(str(PlayerActor.weapon.ammo), center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
        elif PlayerActor.weapon.reserve > 0:
            ptext.draw('Reloading', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20) 
        elif PlayerActor.weapon.reserve == 0:
            ptext.draw('0', center = (35, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
        if PlayerActor.weapon.__class__ == MP412:
            ptext.draw('Inf.', center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
        else: 
            ptext.draw(str(PlayerActor.weapon.reserve), center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    else:
        ptext.draw(str(PlayerActor.weapon.power), center = (90, HEIGHT-25), color = '#c5c5c5', fontsize = 20)
    gname = getattr(PlayerActor.weapon, 'name', str(PlayerActor.weapon.__class__.__name__))
    ptext.draw(gname, center = (55, HEIGHT-75), color = '#c5c5c5', fontsize = 20)
    ptext.draw('Ammo', center = (35, HEIGHT-50), color = '#c5c5c5', fontsize = 20 )
    ptext.draw('Reserve', center = (90, HEIGHT-50), color = '#c5c5c5', fontsize = 20)
    PlayerActor.draw()
    for c in casings:
        if c.moves <= 25:
            c.draw()
    for e in enemies:
        e.draw()

clock.schedule(createpickup, random.randint(15, 20))
clock.schedule(createenemy, random.randint(1,2))
clock.schedule(creategun, 1)

pgzrun.go()
