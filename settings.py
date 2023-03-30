import globals

def default():
    globals.WIDTH = 120
    globals.HEIGHT = 80
    globals.SCALE = 8

def bigger():
    globals.WIDTH = globals.WIDTH * 2
    globals.HEIGHT = globals.HEIGHT * 2

def smaller():
    globals.WIDTH = globals.WIDTH * 0.5
    globals.HEIGHT = globals.HEIGHT * 0.5