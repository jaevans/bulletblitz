from pgzero.actor import Actor
import pgzero.game as game
import math
import random

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
    def __init__ (self, gun, angle, *args, **kwargs):
        super().__init__(gun.bulletimage, *args, **kwargs)
        self.dmg = gun.dmg
        self.velocity = gun.velocity
        self.range = gun.range
        self.spread = gun.spread
        self.angle = angle + ((random.random()* self.spread) - self.spread / 2)
        
    def move(self):
        self.forward(self.velocity)

class PlayerActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.gun = None
        
class CasingActor(TurtleActor):
    def __init__ (self, gun, angle, *args, **kwargs):
        super().__init__(gun.caseimage , *args, **kwargs)
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
