import math
import random
from actors import BulletActor, CasingActor

class Gun (object):
    def __init__(self):
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
        self.reloadscheduled = False
        self.reserve = None
        self.reservecap = None

    def fire(self, PlayerActor):
        self.ammo -= 1
        
        d = PlayerActor._orig_surf.get_size()[0]
        the_angle = math.radians(PlayerActor.angle)
        x = d * math.cos(the_angle)
        y = -d * math.sin(the_angle)
        m = ((PlayerActor.x + x), (PlayerActor.y + y))
       
        b = BulletActor(self, PlayerActor.angle, camera = PlayerActor.camera, center = m)
        #bullets.append(b)
        
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

        return (b,), (c,)

    def doreload(self):
        if self.__class__ == MP412:
            self.ammo = self.capacity
        else:
            if self.capacity <= self.reserve:
                self.reserve -= self.capacity - self.ammo
                self.ammo = self.capacity
        
            else:
                self.ammo = self.reserve
                self.reserve = 0
        self.reloadscheduled = False

class MP412 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 16
        self.rpm = 120
        self.spread = 5
        self.velocity = 20
        self.range = 450
        self.capacity = 6
        self.ammo = self.capacity
        self.reload = 2.25
        self.image = 'mp412_hold'
        self.ammosize = '9mm'
        self.firemode = 'semi'
        self.holdslow = 4
        self.reserve = 1

class MP5 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 8
        self.rpm = 700
        self.spread = 10
        self.velocity = 20
        self.range = 450 
        self.capacity = 30
        self.ammo = self.capacity
        self.reload = 2.3
        self.image = 'mp5_hold'
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
        self.velocity = 24
        self.range = 400 
        self.capacity = 33
        self.ammo = self.capacity
        self.reload = 2.1
        self.image = 'vector_hold'
        self.ammosize = '9mm'
        self.firemode = 'auto'
        self.holdslow = 6
        self.reserve = 99
        self.reservecap = 330

class SV98 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 86
        self.rpm = 20
        self.spread = 1
        self.velocity = 45
        self.range = 625
        self.capacity = 10
        self.ammo = self.capacity
        self.reload = 3.4
        self.image = 'sv98_hold'
        self.ammosize = '7.62'
        self.firemode = 'semi'
        self.holdslow = 5
        self.reserve = 30
        self.reservecap = 90

class M249 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 9
        self.rpm = 860
        self.spread = 20
        self.velocity = 25
        self.range = 575
        self.capacity = 100
        self.ammo = self.capacity
        self.reload = 7.1
        self.image = 'm249_hold'
        self.ammosize = '5.56'
        self.firemode = 'auto'
        self.holdslow = 8
        self.reserve = 300
        self.reservecap = 600

class AUG_A1 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 10
        self.rpm = 750
        self.spread = 2
        self.velocity = 26
        self.range = 600
        self.capacity = 30
        self.ammo = self.capacity
        self.reload = 2.7
        self.image = 'auga1_hold'
        self.ammosize = '5.56'
        self.firemode = 'auto'
        self.holdslow = 6
        self.reserve = 160
        self.reservecap = 480

class M870 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 5
        self.rpm = 30
        self.spread = 15
        self.velocity = 13
        self.range = 210
        self.capacity = 5
        self.ammo = self.capacity
        self.reload = 2.7
        self.image = 'm870_hold'
        self.bulletimage = 'pellet'
        self.caseimage = 'shell'
        self.ammosize = '12g'
        self.firemode = 'semi'
        self.holdslow = 6
        self.reserve = 20
        self.reservecap = 100
        
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