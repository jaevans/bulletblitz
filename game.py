import pgzero
import math

PlayerActor = Actor('mp412_hold')

WIDTH = 750
HEIGHT = 750

def on_mouse_move(pos):
    PlayerActor.angle = PlayerActor.angle_to(pos)

def update():
    if keyboard[keys.W]:
        PlayerActor.y = max(PlayerActor.y -5, 0)
    if keyboard[keys.A]:
        PlayerActor.x = max(PlayerActor.x -5, 0)
    if keyboard[keys.S]:
        PlayerActor.y = min(PlayerActor.y +5, HEIGHT)
    if keyboard[keys.D]:
        PlayerActor.x = min(PlayerActor.x +5, WIDTH)

def draw():
    screen.fill('black')
    PlayerActor.draw()

