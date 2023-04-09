import pygame
import random

class Particle:
    def __init__(self, position, velocity, color, size, life=1):
        self.position = position
        self.velocity = velocity
        self.color = color
        self.size = size
        self.lifespan = life
        self.life = life
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.position[0], self.position[1], self.size, self.size))
        
class ParticleEmitter:
    def __init__(self, position, num_particles, size_range, velocity_x_range, velocity_y_range, colors, life):
        self.position = position
        self.num_particles = num_particles
        self.size_range = size_range
        self.velocity_x_range = velocity_x_range
        self.velocity_y_range = velocity_y_range
        self.colors = colors
        self.life = life
        self.particles = []
        
        self.create_particles()
        
    def create_particles(self):
        for i in range(self.num_particles):
            size = random.randint(self.size_range[0], self.size_range[1])
            # random float velocity
            vx = random.uniform(self.velocity_x_range[0], self.velocity_x_range[1])
            vy = random.uniform(self.velocity_y_range[0], self.velocity_y_range[1])
            velocity = pygame.math.Vector2(vx, vy)
            color = random.choice(self.colors)
            self.particles.append(Particle(self.position.copy(), velocity, color, size, self.life))
            
    def rebirth(self, particle):
        particle.life = particle.lifespan
        particle.position = self.position.copy()
        vx = random.uniform(self.velocity_x_range[0], self.velocity_x_range[1])
        vy = random.uniform(self.velocity_y_range[0], self.velocity_y_range[1])
        particle.velocity.x = vx
        particle.velocity.y = vy
        particle.color = random.choice(self.colors)
        size = random.randint(self.size_range[0], self.size_range[1])
        particle.size = size        
        
    def update(self, dt):
        for particle in self.particles:
            particle.life -= dt
            if (particle.life <= 0):
                self.rebirth(particle)
            else:
                particle.position += particle.velocity * dt
            
    def draw(self, surface):
        for particle in self.particles:
            particle.draw(surface)