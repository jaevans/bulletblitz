from pgzero.actor import Actor
import pgzero.game as game
import math
import random
from pgzero.clock import clock

G_MP5 = 1
G_VECTOR = 2
G_SV98 = 3
G_M249 = 4
G_AUG_A1 = 5
G_M870 = 6
G_AA12 = 7

GUNS = {
    G_MP5: 'mp5',
    G_VECTOR: 'vector',
    G_SV98: 'sv98',
    G_M249: 'm249',
    G_AUG_A1: 'aug_a1',
    G_AA12: 'aa12',
    }

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
        
class ProjectileActor(TurtleActor):
    def __init__ (self, image, angle, *args, **kwargs):
        super().__init__(image, *args, **kwargs)

        self.angle = angle

class BulletActor (ProjectileActor):
    def __init__(self, gun, angle, *args, **kwargs):
        super().__init__(gun.bulletimage, angle, *args, **kwargs)
        self.dmg = gun.dmg
        self.velocity = gun.velocity
        self.range = gun.range
        self.spread = gun.spread
        self.angle = angle + ((random.random()* self.spread) - self.spread / 2)
    
    def move(self):
        self.forward(self.velocity)

class GrenadeActor (ProjectileActor):
    def __init__(self, grenade, angle, *args, **kwargs):
        super().__init__(grenade.grenadeimage, angle, *args, **kwargs)
        self.power = grenade.power
        self.angle = angle
        self.explodeimage = grenade.explodeimage
        self.fuse = grenade.fuse
        self.alive = True
        clock.schedule(self.explode, self.fuse)

    def move(self):
        if self.velocity > 0:
            self.forward(self.velocity)
            self.velocity -= 1
    
    def kill(self):
        self.alive = False
    
    def explode(self):
        self.image = self.explodeimage
        clock.schedule(self.kill, 1)

class PlayerActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.weapon = None
        
class CasingActor(TurtleActor):
    def __init__ (self, gun, angle, *args, **kwargs):
        super().__init__(gun.caseimage , *args, **kwargs)
        self.angle = angle
        self.moveangle = angle
        self.alive = True
        self.flying = True

    def killtimer(self):
        self.alive = False

    def stopfly(self):
        self.flying = False
    
    def move(self):
        self.x += 5 * math.cos(self.moveangle)
        self.y -= 5 * math.sin(self.moveangle)
        self.turnleft(15)

class AmmoActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        super().__init__('ammo_pickup', *args, **kwargs) 

class GunActor(TurtleActor):
    def __init__ (self, *args, **kwargs):
        gunnumber = random.randint(G_MP5, G_AA12)
        super().__init__(str(GUNS[gunnumber])+'_ground', *args, **kwargs)


class EnemyActor(TurtleActor):
    def __init__ (self, etype = None, *args, **kwargs):
        super().__init__('zombie_1', *args, **kwargs)
        self.hp = 100
