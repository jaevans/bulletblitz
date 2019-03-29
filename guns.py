class Gun (object):
    def __init__(self):
        self.dmg = None
        self.rpm = None
        self.spread = None
        self.velocity = None
        self.range = None
        self.image = None
        self.ammo = None
        self.xcenter = None
        self.ycenter = None
        self.firemode = None

class MP412 (Gun):
    def __init__(self):
        self.dmg = 16
        self.rpm = 90
        self.spread = 5
        self.velocity = 15
        self.range = 300
        self.image = 'mp412_hold'
        self.ammo = '9mm'
        self.xcenter = 32
        self.ycenter = 29
        self.firemode = 'semi'

class MP5 (object):
    def __init__(self):
        self.dmg = 8
        self.rpm = 700
        self.spread = 10
        self.velocity = 15
        self.range = 425
        self.image = 'mp5_hold'
        self.ammo = '9mm'
        self.xcenter = 37
        self.ycenter = 31
        self.firemode = 'auto'