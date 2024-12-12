import numpy as np
import pygame
from pygame.locals import *
import sys
import random
import time
from collections import defaultdict

class Circle:
    def __init__(self, position, velocity, diameter, color):
        self.position = np.array(position, dtype=float)
        self.velocity = np.array(velocity, dtype=float)
        self.diameter = diameter
        self.radius = diameter / 2
        self.color = color
        self.accel = np.zeros(2, dtype=float)
        self.bounce_damping = 1  # Damping factor to simulate energy loss

    def update(self, delta_time):
        # Update velocity with acceleration
        self.velocity += self.accel * delta_time
        # Update position with velocity
        self.position += self.velocity * delta_time
        # Reset acceleration
        self.accel.fill(0)

    def apply_gravity(self, gravity):
        self.accel += gravity

    def apply_constraints(self, screen_width, screen_height):
        # Check for collision with the floor
        if self.position[1] > screen_height - self.radius:
            self.position[1] = screen_height - self.radius
            self.velocity[1] *= -self.bounce_damping
        
        # Check for collision with the ceiling
        if self.position[1] < self.radius:
            self.position[1] = self.radius
            self.velocity[1] *= -self.bounce_damping
        
        # Check for collision with the right wall
        if self.position[0] > screen_width - self.radius:
            self.position[0] = screen_width - self.radius
            self.velocity[0] *= -self.bounce_damping
        
        # Check for collision with the left wall
        if self.position[0] < self.radius:
            self.position[0] = self.radius
            self.velocity[0] *= -self.bounce_damping

def update(circles, dt, gravity, screen_width, screen_height, cell_size):
    spatial_hash = defaultdict(list)
    for circle in circles:
        circle.apply_gravity(gravity)
        circle.update(dt)
        circle.apply_constraints(screen_width, screen_height)
        add_circle_to_hash(circle, spatial_hash, cell_size)

    handle_collisions(spatial_hash, cell_size)

def add_circle_to_hash(circle, spatial_hash, cell_size):
    min_x = int((circle.position[0] - circle.radius) // cell_size)
    max_x = int((circle.position[0] + circle.radius) // cell_size)
    min_y = int((circle.position[1] - circle.radius) // cell_size)
    max_y = int((circle.position[1] + circle.radius) // cell_size)

    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            spatial_hash[(x, y)].append(circle)

def handle_collisions(spatial_hash, cell_size):
    for cell in spatial_hash.values():
        num_circles = len(cell)
        for i in range(num_circles):
            circle1 = cell[i]
            for j in range(i + 1, num_circles):
                circle2 = cell[j]
                dist_vec = circle1.position - circle2.position
                distance = np.linalg.norm(dist_vec)
                min_distance = circle1.radius + circle2.radius

                if distance < min_distance:
                    # Collision detected
                    overlap = min_distance - distance
                    direction = dist_vec / distance

                    # Separate the circles
                    circle1.position += direction * overlap / 2
                    circle2.position -= direction * overlap / 2

                    # Calculate the new velocities
                    v1 = circle1.velocity
                    v2 = circle2.velocity
                    m1 = circle1.diameter ** 2
                    m2 = circle2.diameter ** 2

                    new_v1 = v1 - (2 * m2 / (m1 + m2)) * np.dot(v1 - v2, direction) * direction
                    new_v2 = v2 - (2 * m1 / (m1 + m2)) * np.dot(v2 - v1, direction) * direction

                    circle1.velocity = new_v1
                    circle2.velocity = new_v2

pygame.init()

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Circle Bounce Simulation")

font = pygame.font.Font("freesansbold.ttf", 24)

circles = []
preview = None
gravity = np.array([0, 1000], dtype=float)
cell_size = 40  # Size of each cell in the spatial grid
max_circles = 200  # Maximum number of circles

running = True
start_time = time.time()
mouse_down = False
initial_mouse_pos = None

# Performance tracking variables
fps = 0
delta_time = 0
frame_count = 0
fps_update_time = 1

while running:
    screen.fill((200, 200, 200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            initial_mouse_pos = pygame.mouse.get_pos()
            mouse_down = True
            preview = Circle(initial_mouse_pos, [0, 0], 25, [0, 0, 0])
        elif event.type == pygame.MOUSEBUTTONUP and mouse_down:
            preview = None
            final_mouse_pos = pygame.mouse.get_pos()
            mouse_down = False
            speed = (np.array(final_mouse_pos) - np.array(initial_mouse_pos))
            if len(circles) < max_circles:
                circle = Circle(
                    position=initial_mouse_pos,
                    velocity=-speed,
                    diameter=random.uniform(20, 30),
                    color=[random.randint(50, 180), random.randint(50, 180), random.randint(50, 180)]
                )
                circles.append(circle)

    # Calculate frame time
    current_time = time.time()
    change_time = current_time - start_time
    start_time = current_time

    update(circles, change_time, gravity, screen_width, screen_height, cell_size)

    # Render the circles
    for circle in circles:
        pygame.draw.circle(screen, circle.color, circle.position.astype(int), int(circle.radius))
    if preview:
        pygame.draw.circle(screen, preview.color, preview.position.astype(int), int(preview.radius))

    object_count = font.render(f"Objects Spawned: {len(circles)}", True, (0, 0, 0))
    screen.blit(object_count, (850 - object_count.get_width() // 2, 100 - object_count.get_height() // 2))

    # Render performance metrics
    fps_display = font.render(f"FPS: {fps:.2f}", True, (0, 0, 0))
    screen.blit(fps_display, (850 - fps_display.get_width() // 2, 50 - fps_display.get_height() // 2))

    pygame.display.flip()

    # Calculate FPS
    frame_count += 1
    delta_time += change_time
    if delta_time >= fps_update_time:
        fps = frame_count / delta_time
        frame_count = 0
        delta_time = 0

pygame.quit()
sys.exit()
