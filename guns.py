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

