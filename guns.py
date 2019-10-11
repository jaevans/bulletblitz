import math
from pgzero.clock import clock
import random
from pgzero.loaders import sounds
from actors import BulletActor, GrenadeActor, CasingActor

class Weapon (object):
    def __init__(self):
        self.triggerHeld = False

class Gun (Weapon):
    def __init__(self):
        super().__init__()
        self.dmg = None
        self.rpm = None
        self.spread = None
        self.velocity = None
        self.range = None
        self.capacity = None
        self.ammo = None
        self.reload = None
        self.image = None
        self.bulletimage = 'bullet'
        self.caseimage = 'case'
        self.ammosize = None
        self.firemode = None
        self.holdslow = None
        self.reloadScheduled = False
        self.reserve = None
        self.reservecap = None
        self.knockback = 3
        t = sounds.load('mp412_shot')
        self.gun_sound = sounds.mp412_shot
        self.critmult = 1.5

    def fire(self, PlayerActor):
        self.ammo -= 1
        self.gun_sound.play()
        
        d = PlayerActor._orig_surf.get_size()[0]
        the_angle = math.radians(PlayerActor.angle)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        m = ((PlayerActor.x + x), (PlayerActor.y + y))
       
        b = BulletActor(self, PlayerActor.angle, camera = PlayerActor.camera, center = m)
        
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
        
        c = CasingActor(self, (PlayerActor.angle - 90.0) + random.randint(-2,2), camera = PlayerActor.camera, center = m)
        #casings.append(c)

        return (b,), (c,)

    def doReload(self):
        if self.__class__ == MP412:
            self.ammo = self.capacity
        else:
            if self.capacity <= self.reserve:
                self.reserve -= self.capacity - self.ammo
                self.ammo = self.capacity
        
            else:
                self.ammo = self.reserve
                self.reserve = 0
        self.reloadScheduled = False

class MP412 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 16
        self.rpm = 120
        self.spread = 5
        self.velocity = 18
        self.range = 450
        self.capacity = 6
        self.ammo = self.capacity
        self.reload = 2.25
        self.holdimage = 'mp412_hold'
        self.sound = 'mp412_shot'
        self.ammosize = '9mm'
        self.firemode = 'semi'
        self.holdslow = 4
        self.reserve = 1
        self.critmult = 2
        self.knockback = 7

class MP5 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 8
        self.rpm = 700
        self.spread = 10
        self.velocity = 18
        self.range = 450 
        self.capacity = 30
        self.ammo = self.capacity
        self.reload = 2.3
        self.holdimage = 'mp5_hold'
        self.ammosize = '9mm'
        self.firemode = 'auto'
        self.holdslow = 5
        self.reserve = 90
        self.reservecap = 300

class Vector (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 6
        self.rpm = 1200
        self.spread = 5
        self.velocity = 18
        self.range = 400 
        self.capacity = 33
        self.ammo = self.capacity
        self.reload = 2.1
        self.holdimage = 'vector_hold'
        self.ammosize = '9mm'
        self.firemode = 'auto'
        self.holdslow = 6
        self.reserve = 99
        self.reservecap = 330

class SV98 (Gun):
    def __init__(self):
        super().__init__()
        self.name = 'SV-98'
        self.dmg = 86
        self.rpm = 20
        self.spread = 1
        self.velocity = 20
        self.range = 625
        self.capacity = 10
        self.ammo = self.capacity
        self.reload = 3.4
        self.holdimage = 'sv98_hold'
        self.ammosize = '7.62'
        self.firemode = 'semi'
        self.holdslow = 5
        self.reserve = 30
        self.reservecap = 90
        self.knockback = 10

class M249 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 9
        #self.rpm = 860
        self.rpm = 120
        self.spread = 20
        self.velocity = 18
        self.range = 575
        self.capacity = 100
        self.ammo = self.capacity
        self.reload = 7.1
        self.holdimage = 'm249_hold'
        self.ammosize = '5.56'
        self.firemode = 'auto'
        self.holdslow = 8
        self.reserve = 300
        self.reservecap = 600
        self.critmult = 1.15

class AUG_A1 (Gun):
    def __init__(self):
        super().__init__()
        self.name = 'AUG A1'
        self.dmg = 10
        self.rpm = 750
        self.spread = 2
        self.velocity = 18
        self.range = 600
        self.capacity = 30
        self.ammo = self.capacity
        self.reload = 2.7
        self.holdimage = 'auga1_hold'
        self.ammosize = '5.56'
        self.firemode = 'auto'
        self.holdslow = 6
        self.reserve = 160
        self.reservecap = 480

class Shotgun (Gun):
    def fire(self, PlayerActor):
        self.ammo -= 1
        pellets = []
        for i in range(9):
            d = PlayerActor._orig_surf.get_size()[0] + random.randint(-5,5)
            the_angle = math.radians(PlayerActor.angle)
            x = d * math.cos(the_angle)
            y = -d * math.sin(the_angle)
            m = ((PlayerActor.x + x), (PlayerActor.y + y))
       
            b = BulletActor(self, PlayerActor.angle, camera = PlayerActor.camera, center = m)
            pellets.append(b)
        
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
        
        c = CasingActor(self, PlayerActor.angle -90 + random.randint(-2,2), camera = PlayerActor.camera, center = m)
        #casings.append(c)

        return pellets, (c,)

class M870 (Shotgun):
    def __init__(self):
        super().__init__()
        self.dmg = 7
        self.rpm = 45
        self.spread = 15
        self.velocity = 13
        self.range = 410
        self.capacity = 5
        self.ammo = self.capacity
        self.reload = 2.7
        self.holdimage = 'm870_hold'
        self.bulletimage = 'pellet'
        self.caseimage = 'shell'
        self.ammosize = '12g'
        self.firemode = 'semi'
        self.holdslow = 5
        self.reserve = 20
        self.reservecap = 100
        self.critmult = 1.15
        self.knockback = 3

class AA12 (Shotgun):
    def __init__(self):
        super().__init__()
        self.name = 'AA-12'
        self.dmg = 7
        self.rpm = 300
        self.spread = 22
        self.velocity = 13
        self.range = 410
        self.capacity = 20
        self.ammo = self.capacity
        self.reload = 4.0
        self.holdimage = 'aa12_hold'
        self.bulletimage = 'pellet'
        self.caseimage = 'shell'
        self.ammosize = '12g'
        self.firemode = 'auto'
        self.holdslow = 7
        self.reserve = 40
        self.reservecap = 100
        self.critmult = 1
        self.knockback = 3
    
class Throwable (Weapon):
    def __init__ (self):
        super().__init__()
        self.dmg = 100
        self.fuse = 5
        self.blastradius = 128
        self.power = 0

class Grenade (Throwable):
    def __init__ (self):
        super().__init__()
        self.holdslow = 4
        self.fuse = 2
        self.holdimage = 'grenade_hold'
        self.chargeimage = 'grenade_charge'
        self.grenadeimage = 'grenade'
        self.explodeimage = 'explosion'
        self.reserve = 5
        self.reservecap = 15
    
    def increasepower(self):
        if self.power < 20 and self.triggerHeld:
            self.power += 3
            clock.schedule(self.increasepower, .033)

    def throw(self, PlayerActor):
    
        d = 30
        the_angle = math.radians(PlayerActor.angle)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        p = ((PlayerActor.x + x), (PlayerActor.y + y))

        g = GrenadeActor(self, PlayerActor.angle, camera = PlayerActor.camera, center = p)
        g.velocity = g.power
        return g
