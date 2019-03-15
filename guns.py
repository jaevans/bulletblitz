class Gun (object):
    def __init__(self):
        self.dmg = None
        self.rpm = None
        self.spread = None
        self.velocity = None
        self.range = None
        self.image = None
        self.ammo = None

class MP412 (Gun):
    def __init__(self):
        self.dmg = 16
        self.rpm = 85
        self.spread = 5
        self.velocity = 15
        self.range = 300
        self.image = 'mp412_hold'
        self.ammo = '9mm'
