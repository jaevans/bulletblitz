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
        self.ammosize = None
        self.firemode = None
        self.holdslow = None
        self.reloadscheduled = False

    def doreload(self):
        self.ammo = self.capacity
        self.reloadscheduled = False

class MP412 (Gun):
    def __init__(self):
        super().__init__()
        self.dmg = 16
        self.rpm = 90
        self.spread = 5
        self.velocity = 20
        self.range = 450
        self.capacity = 6
        self.ammo = self.capacity
        self.reload = 3.75
        self.image = 'mp412_hold'
        self.ammosize = '9mm'
        self.firemode = 'semi'
        self.holdslow = 4

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

class AUGa1 (Gun):
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