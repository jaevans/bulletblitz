class Gun (object):
    def __init__(self):
        self.dmg = None
        self.rpm = None
        self.spread = None
        self.velocity = None
        self.range = None
        self.image = None
        self.ammo = None
        self.firemode = None
        self.holdslow = None

class MP412 (Gun):
    def __init__(self):
        self.dmg = 16
        self.rpm = 90
        self.spread = 5
        self.velocity = 20
        self.range = 450
        self.image = 'mp412_hold'
        self.ammo = '9mm'
        self.firemode = 'semi'
        self.holdslow = 1

class MP5 (Gun):
    def __init__(self):
        self.dmg = 8
        self.rpm = 700
        self.spread = 10
        self.velocity = 20
        self.range = 670
        self.image = 'mp5_hold'
        self.ammo = '9mm'
        self.firemode = 'auto'
        self.holdslow = 2

class Vector (Gun):
    def __init__(self):
        self.dmg = 6
        self.rpm = 1200
        self.spread = 5
        self.velocity = 24
        self.range = 400
        self.image = 'vector_hold'
        self.ammo = '9mm'
        self.firemode = 'auto'
        self.holdslow = 3

class SV98 (Gun):
    def __init__(self):
        self.dmg = 86
        self.rpm = 20
        self.spread = 1
        self.velocity = 45
        self.range = 625
        self.image = 'sv98_hold'
        self.ammo = '7.62'
        self.firemode = 'semi'
        self.holdslow = 4

class M249 (Gun):
    def __init__(self):
        self.dmg = 9
        self.rpm = 860
        self.spread = 20
        self.velocity = 25
        self.range = 450
        self.image = 'm249_hold'
        self.ammo = '5.56'
        self.firemode = 'auto'
        self.holdslow = 6

class AUGa1 (Gun):
    def __init__(self):
        self.dmg = 10
        self.rpm = 750
        self.spread = 2
        self.velocity = 26
        self.range = 600
        self.image = 'auga1_hold'
        self.ammo = '5.56'
        self.firemode = 'auto'
        self.holdslow = 4