import pygame as pg
import random
import math


class Particle:
    def __init__(self, x, y, size):
        # left upper corner [0,0]
        self.x = x
        self.y = y
        self.size = size
        # color RGB
        self.color = (0, 0, 255)
        self.thickness = 1
        # self.v = pg.math.Vector2(random.choice([-0.2,-0.1,0.1,0.2]),random.choice([-0.2,-0.1,0.1,0.2]))
        # speed vector
        # LM: consider polar coordinates
        self.v = pg.math.Vector2(
            random.randint(10, 100), random.randint(-100, 100))

    def move(self):
        # timestep, per default time_step from config
        self.dT = 0.1
        # change x, y coordinates
        self.x += self.v[0] * self.dT
        self.y += self.v[1] * self.dT
    
    def drawCircle(self,screen):
        pg.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

    
    

class Environment:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        # store particles
        self.particles = []
        # environment background color
        self.color = (255, 255, 255)

    def bounce(self, particle):
        # when the particle touch the walls
        # right border
        # LM: careful about width vs self.width
        if particle.x > self.width - particle.size:
            particle.v = pg.math.Vector2(-particle.v[0], particle.v[1])
        # left border
        elif particle.x < particle.size:
            particle.v = pg.math.Vector2(-particle.v[0], particle.v[1])
        # floor
        if particle.y > self.height - particle.size:
            particle.v = pg.math.Vector2(particle.v[0], -particle.v[1])
        # ceiling
        elif particle.y < particle.size:
            particle.v = pg.math.Vector2(particle.v[0], -particle.v[1])

    # Create a new particle
    # LM: 'kwargs' is the standard name
    def addParticles(self, n=1, **kargs):
        for i in range(n):
            # default random size
            # LM: cool use of defaults!
            size = kargs.get('size', random.randint(10, 20))
            # default random coordinates
            x = kargs.get('x', random.uniform(size, self.width - size))
            y = kargs.get('y', random.uniform(size, self.height - size))

            # instance of Particle class
            particle = Particle(x, y, size)
            # set initial speed
            particle.v = kargs.get('v', pg.math.Vector2(
                random.randint(10, 100), random.randint(10, 100)))
            # set particle color
            particle.color = kargs.get('color', (0, 0, 255))
            # add instance of particle to list of particles
            self.particles.append(particle)

    def update(self):
        # update state of simulation, resolve collisions

        # LM: 'for p in self.particles:' if you want only particles,
        #     'for i, p in enumerate(self.particles):' if you want both id and the particle
        for p in self.particles:
            # move particle
            p.move()
            # check collisions with borders
            self.bounce(p)
    def draw(self,screen):
         for p in self.particles:
            p.drawCircle(screen)
    
    
