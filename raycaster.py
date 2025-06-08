import math
import pygame
import sys

#screen variables
#length
screen_width = 640
screen_height = 480
#init stuff
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.init()
pygame.init()
running = True
clock = pygame.time.Clock()
#map
# worldMap = [
#     [1,1,1,1,1,1,1,1],
#     [1,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1],
#     [1,0,0,0,0,0,0,1],
#     [1,1,1,1,1,1,1,1],
# ]
worldMap = [
    [1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,0,1],
    [1,0,1,0,0,1,1,1],
    [1,0,0,0,0,0,0,1],
    [1,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,0,1],
    [1,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1],
]

#starter variables
posX = 6.5
posY = 5.5
dirX = -1
dirY = 0
planeX = 0
planeY = 0.66
moveSpeed = 0.05
rotSpeed = 0.03

#raycaster function
def raycaster():
    for x in range(screen_width):
        # Using a for loop that iterates through each pixel of the screen's width,
        # the location where the ray intersects with the camera plane (the screen)
        # is calculated(cameraX). The X and Y components of the ray are calculated
        # using the direction vector(direction player is facing---this is a unit
        # vector), its orthogonal camera plane vector(which just represents the
        # plane on which the 2d player can see), and the cameraX as a scale value.
        # The map square the player is in is calculated as the player's position
        # as an integer (if posX is 3.5, mapX is 3).
        cameraX = 2 * x / screen_width - 1
        rayDirX = dirX + planeX * cameraX
        rayDirY = dirY + planeY * cameraX
        mapX = int(posX)
        mapY = int(posY)
        # sideDistX = None
        # sideDistY = None
        deltaDistX = abs(1 / rayDirX) if rayDirX != 0 else 1e30
        deltaDistY = abs(1 / rayDirY) if rayDirY != 0 else 1e30
        # perpWallDist = None
        # stepX = None
        # stepY = None
        hit = 0
        # side = None

        if (rayDirX < 0):
            stepX = -1
            sideDistX = (posX - mapX) * deltaDistX
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * deltaDistX
        if (rayDirY < 0):
            stepY = -1
            sideDistY = (posY - mapY) * deltaDistY
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * deltaDistY

        while (hit == 0):
            if (sideDistX < sideDistY):
                sideDistX += deltaDistX
                mapX += stepX
                side = 0
            else:
                sideDistY += deltaDistY
                mapY += stepY
                side = 1
            if (worldMap[mapY][mapX] == 1):
                hit = 1
        # if (side == 0):
        #     #this was a challenge. Lode's code was only correct for the ray when cameraX
        #     # = 0. you actually have to find the projection length, which is adotb/bdotb
        #     #this is the perp wall dist for any ray.
        if side == 0:
            perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
        else:
            perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

        # perpWallDist = (rayDirX * dirX + rayDirY * dirY)/(math.sqrt(dirX**2 + dirY**2))
        # perpWallDist = (rayDirX * dirX + rayDirY * dirY)/(math.sqrt(dirX**2 + dirY**2))



        lineHeight = (int)(screen_height / perpWallDist)
        drawStart = -lineHeight / 2 + screen_height / 2
        if (drawStart < 0):
            drawStart = 0
        drawEnd = lineHeight / 2 + screen_height / 2
        if (drawEnd >= screen_height):
            drawEnd = screen_height - 1
        color = (255, 0, 0)
        if side == 1:
            color = (180,0,0)
        pygame.draw.line(screen, color, [x,drawStart], [x,drawEnd])

#movement loop
def movement():
    #errors: did false instead of zero, wrong event.get function iteration
    #swapped x and y indexes in worldMap
    global posX, posY, dirX, dirY, planeX, planeY
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if worldMap[int(posY)][int(posX + dirX * moveSpeed)] == 0:
            posX += dirX * moveSpeed
        if worldMap[int(posY + dirY * moveSpeed)][int(posX)] == 0:
            posY += dirY * moveSpeed
        #if your current position does not equal how much you've "moved" added to
        #your current position, then change your position, moving you around.
    if keys[pygame.K_s]:
        if worldMap[int(posY)][int(posX - dirX * moveSpeed)] == 0:
            posX -= dirX * moveSpeed
        if worldMap[int(posY - dirY * moveSpeed)][int(posX)] == 0:
            posY -= dirY * moveSpeed
    if keys[pygame.K_d]:  # rotate left
        oldDirX = dirX
        dirX = dirX * math.cos(-rotSpeed) - dirY * math.sin(-rotSpeed)
        dirY = oldDirX * math.sin(-rotSpeed) + dirY * math.cos(-rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(-rotSpeed) - planeY * math.sin(-rotSpeed)
        planeY = oldPlaneX * math.sin(-rotSpeed) + planeY * math.cos(-rotSpeed)
        #transformation matrix * dir vector and plane vector
    if keys[pygame.K_a]:
        oldDirX = dirX
        dirX = dirX * math.cos(rotSpeed) - dirY * math.sin(rotSpeed)
        dirY = oldDirX * math.sin(rotSpeed) + dirY * math.cos(rotSpeed)
        oldPlaneX = planeX
        planeX = planeX * math.cos(rotSpeed) - planeY * math.sin(rotSpeed)
        planeY = oldPlaneX * math.sin(rotSpeed) + planeY * math.cos(rotSpeed)


#while loop

while running:
    for event in pygame.event.get():
        # Check for QUIT event
        if event.type == pygame.QUIT:
            running = False
    movement()
    screen.fill((0, 0, 0))  # Clear previous frame
    raycaster()
    pygame.display.flip()  # Update the screen
    clock.tick(60)  # Cap to 60 FPS
