
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
        #self.v = pg.math.Vector2(
            #random.randint(-100, 100), random.randint(-100, 100))
        self.speed = 0
        self.angle = 0

    def move(self):
        # timestep, per default time_step from config
        self.dT = 1
        # change x, y coordinates
        self.x += math.sin(self.angle) * self.speed * self.dT
        self.y -= math.cos(self.angle) * self.speed * self.dT

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
        # right border
        if particle.x > self.width - particle.size:
            particle.x = 2*(self.width - particle.size) - particle.x
            particle.angle = - particle.angle
        # left border
        elif particle.x < particle.size:
            particle.x = 2*particle.size - particle.x
            particle.angle = - particle.angle
        # floor
        if particle.y > self.height - particle.size:
            particle.y = 2*(self.height - particle.size) - particle.y
            particle.angle = math.pi - particle.angle
        # ceiling
        elif particle.y < particle.size:
            particle.y = 2*particle.size - particle.y
            particle.angle = math.pi - particle.angle

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
            #particle.v = kargs.get('v', pg.math.Vector2(
                #random.randint(10, 100), random.randint(10, 100)))
            # set particle color
            particle.color = kargs.get('color', (0, 0, 255))
            particle.speed = kargs.get('speed', random.uniform(1,5))
            particle.angle = kargs.get('angle', random.uniform(0, math.pi*2))
            # add instance of particle to list of particles
            self.particles.append(particle)

    def update(self):
        # update state of simulation, resolve collisions

        # LM: 'for p in self.particles:' if you want only particles,
        #     'for i, p in enumerate(self.particles):' if you want both id and the particle
        for i, p in enumerate(self.particles):
            # move particle
            p.move()
            # check collisions with borders
            self.bounce(p)
            # check collisions between all particles
            for p2 in self.particles[i+1:]:
                self.collide(p, p2)

    def draw(self,screen):
         for p in self.particles:
            p.drawCircle(screen)
    
    def collide(self,p1,p2):
        # define difference
        dx = p1.x - p2.x
        dy = p1.y - p2.y
    
        # calculate the size of a vector sqrt(dx**2+dy**2)
        distance = math.hypot(dx, dy)
        # check if there is a contact 
        if distance < p1.size + p2.size:
            overlap = (p1.size + p2.size) - distance
            tangent = math.atan2(dy, dx)
            angle = 0.5* math.pi + tangent
            
            
            # calculate new angle
            p1.angle = 2 * tangent - p1.angle
            p2.angle = 2 * tangent - p2.angle
            # change speed (assumming all energy transforms)
            (p1.speed, p2.speed) = (p2.speed, p1.speed)
            # correction (particles goes to indefinite loop)
            # step by step simulation, collisions are not verified
            # in the real time
            if overlap >= 0:
                p1.x += math.sin(angle)*(overlap)
                p1.y -= math.cos(angle)*(overlap)
                p2.x -= math.sin(angle)*(overlap)
                p2.y += math.cos(angle)*(overlap)
            '''angle = 0.5* math.pi + tangent
            # sligtly move the x, y coordinates in case the particles are overlapping
            p1.x += math.sin(angle)
            p1.y -= math.cos(angle)
            p2.x -= math.sin(angle)
            p2.y += math.cos(angle)'''