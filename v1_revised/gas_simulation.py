
import pygame as pg
import random
import math


class Particle:
    """
    A class used to represent Particle

    ...

    Attributes
    ----------
    x : int
        position on x axes
    y : int 
        position on y axes
    size : int
        size of a particle in pixels

    Methods
    -------
    move()
        Move particle on canvas, change position

    drawCircle(screen)
        Draw particle as a circle on canvas
    """
    def __init__(self, x, y, size):
        """"""
        # left upper corner [0,0]
        self.x = x
        self.y = y
        self.size = size
        # color RGB
        self.color = (0, 0, 255)
        # thickness of a particle border
        self.thickness = 1
        # speed of a particle
        self.speed = 0
        # angle y is pi/2 to x
        self.angle = 0

    def move(self):
        # timestep, per default time_step from config
        self.dT = 1
        # change x, y coordinates, polar system
        self.x += math.sin(self.angle) * self.speed * self.dT
        self.y -= math.cos(self.angle) * self.speed * self.dT

    def drawCircle(self,screen):
        # draw
        pg.draw.circle(screen, self.color, (self.x, self.y), self.size, self.thickness)

    
    

class Environment:
    """
    A class used to make Environment for particles

    ...

    Attributes
    ----------
    width : int
        width of canvas
    height : int 
        height of canvas
    particles : list
        list for storing particles and their property
    color : tuple
        store color in RGB

    Methods
    -------
    bounce(particle)
        Collisions with borders

    addParticles(screen)
        Create new particle and match the properties

    update()
        update state of simulation, resolve collisions

    draw(screen)
        draw particles on canvas

    collide(p1,p2)
        resolve collisions between particles
    """
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

    # Create a new particle, default 1
    def addParticles(self, n=1, **kwargs):
        for i in range(n):
            # default random size
            size = kwargs.get('size', random.randint(10, 20))
            # default random coordinates
            x = kwargs.get('x', random.uniform(size, self.width - size))
            y = kwargs.get('y', random.uniform(size, self.height - size))

            # instance of Particle class
            particle = Particle(x, y, size)
            # set initial speed
            # set particle color
            particle.color = kwargs.get('color', (0, 0, 255))
            # set velocity, uniform division (here could be maxwell-boltzmann)
            particle.speed = kwargs.get('speed', random.uniform(1,5))
            # set angle
            particle.angle = kwargs.get('angle', random.uniform(0, math.pi*2))
            # add instance of particle to list of particles
            self.particles.append(particle)

    def update(self):
        # go through particles
        for i, p in enumerate(self.particles):
            # move particle
            p.move()
            # check collisions with borders
            self.bounce(p)
            # check collisions between all particles
            for p2 in self.particles[i+1:]:
                # resolve collision
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
            # check how much they overlap
            overlap = (p1.size + p2.size) - distance
            # calculate angle at the point of contact
            tangent = math.atan2(dy, dx)
            angle = 0.5* math.pi + tangent
            
            # calculate new angle for particle
            p1.angle = 2 * tangent - p1.angle
            p2.angle = 2 * tangent - p2.angle

            # change speed (assumming all energy transforms), elsasticity
            (p1.speed, p2.speed) = (p2.speed, p1.speed)
            # correction (particles goes to indefinite loop)
            # step by step simulation, collisions are not verified
            # in the real time, discrete simulation
            # move particle slightly by the overlapping distance
            if overlap >= 0:
                p1.x += math.sin(angle)*(overlap)
                p1.y -= math.cos(angle)*(overlap)
                p2.x -= math.sin(angle)*(overlap)
                p2.y += math.cos(angle)*(overlap)