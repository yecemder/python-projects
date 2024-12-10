import numpy as np
from math import sqrt
import pygame
from pygame.locals import *
import sys
import random
import time

# ----------------------------------------------

def VerletUpdate(obj, deltaTime): # only to be used on verlet generated objects that have properties
    # currentPosition, lastPosition, velocity, accel
    obj["velocity"] = obj["currentPosition"] - obj["lastPosition"]
    

    obj["lastPosition"] = obj["currentPosition"]
    obj["currentPosition"] = obj["currentPosition"] + obj["velocity"] + (obj["accel"] * deltaTime * deltaTime)
    obj["accel"] = np.array([float(0), float(0)])
        
def accelerate(thing, acc):
    thing["accel"][0] += acc[0]
    thing["accel"][1] += acc[1]
        
def update(objList, dt):

    applyGravity(objList)
    applyConstraints(objList)
    updatePosition(objList, dt)

def updatePosition(objList, dt):
    for i in objList:
        VerletUpdate(i, dt)

def applyGravity(objList):
    for obj in objList:
        accelerate(obj, gravity)

def applyConstraints(objList):
    
    for obj in objList:
        distTo = obj["currentPosition"] - centrePosition
        distance = sqrt((distTo[0]*distTo[0])+(distTo[1]*distTo[1]))
        if distance > (radius - obj["diameter"] / 2):        
            n = (distTo[0] / distance), (distTo[1] / distance)
            n = np.array(n)
            obj["currentPosition"] = centrePosition + (n * (radius - (obj["diameter"] / 2)))
            
pygame.init()

screen_width = 1000
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("joe mama")

clock = pygame.time.Clock()

font = pygame.font.Font("freesansbold.ttf", 24)


centrePosition = (float(screen_width / 2), float(screen_height / 2))
radius = 250
constrictionColor = ((20, 20, 20))
circles = []
gravity = np.array([0, 1000])


running = True
startTime = time.time()

while running:
    screen.fill((200,200,200))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mousePos = pygame.mouse.get_pos()
            circle = {
                "currentPosition": np.array(mousePos),
                "lastPosition": np.array(mousePos),
                "velocity": np.array([float(0), float(0)]),
                "accel": np.array([float(0), float(0)]),
                "diameter": random.uniform(20,30),
                "color": [random.randint(50,220), random.randint(50,220), random.randint(50,220)]
            }
            circles.append(circle)
    changeTime = (time.time()) - startTime
    update(circles, changeTime)
    startTime = time.time()
    pygame.draw.circle(screen, constrictionColor, centrePosition, radius)
    for i in circles:
        pygame.draw.circle(screen, i["color"], i["currentPosition"], i["diameter"] / 2)
    objectCount = font.render(f"Objects Spawned: {len(circles)}", True, (0,0,0))
    screen.blit(objectCount,(850 - objectCount.get_width() // 2, 100 - objectCount.get_height() // 2))
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
sys.exit()
    
