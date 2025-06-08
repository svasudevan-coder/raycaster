import pygame
import math
import sys

# variables
screen_width = 640
screen_height = 480

#position variables - these define the magnitude + direction of the vectors
posX = 4.5
posY = 3.5
dirX = -1
dirY = 0
#planes are for 2d camera plane vector
planeX = 0
planeY = 0.66

# Movement
move_speed = 0.05
rot_speed = 0.03

#map: 1 is a wall, 0 is empty space

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

# initializing the screen

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height ))
clock = pygame.time.Clock()

#movement function

#raycaster function (the fun stuff :P)
def raycaster():
    for x in range(screen_width):
        cameraX = 2*x/screen_width - 1
        rayDirX = dirX+planeX * cameraX
        rayDirY = dirY + planeY * cameraX
        mapX = int(posX)
        mapY = int(posY)
        # sideDistX = None
        # sideDistY = None

        #finding length of ray

        delta_dist_x = abs(1 / rayDirX) if rayDirX != 0 else 1e30
        delta_dist_y = abs(1 / rayDirY) if rayDirY != 0 else 1e30
        # stepX = None
        # stepY = None

        hit = 0
        # side = None

        if (rayDirX < 0):
            stepX = -1
            sideDistX = (posX - mapX) * delta_dist_x
        else:
            stepX = 1
            sideDistX = (mapX + 1.0 - posX) * delta_dist_x

        if (rayDirY < 0):
            stepY = -1
            sideDistY = (posY - mapY) * delta_dist_y
        else:
            stepY = 1
            sideDistY = (mapY + 1.0 - posY) * delta_dist_y

        #dda alg
        while (hit==0):
            if(sideDistX < sideDistY):
                sideDistX += delta_dist_x
                mapX += stepX
                side = 0
            else:
                sideDistY += delta_dist_y
                mapY += stepY
                side = 1
            if (worldMap[mapY][mapX]>0):
                hit = 1
        if side == 0:
            perpWallDist = (mapX - posX + (1 - stepX) / 2) / rayDirX
        else:
            perpWallDist = (mapY - posY + (1 - stepY) / 2) / rayDirY

        line_height = int(screen_height / (perpWallDist + 0.0001))

        draw_start = max(0, -line_height // 2 + screen_height // 2)
        draw_end = min(screen_height, line_height // 2 + screen_height // 2)

        # Simple shading
        color = (255, 0, 0) if side == 0 else (128, 0, 0)

        pygame.draw.line(screen, color, (x, draw_start), (x, draw_end))

#movement
def handle_input():
    global posX, posY, dirX, dirY, planeX, planeY
    keys = pygame.key.get_pressed()

    # Move forward
    if keys[pygame.K_w]:
        next_x = posX + dirX * move_speed
        next_y = posY + dirY * move_speed
        if worldMap[int(posY)][int(next_x)] == 0:
            posX = next_x
        if worldMap[int(next_y)][int(posX)] == 0:
            posY = next_y

    # Move backward
    if keys[pygame.K_s]:
        next_x = posX - dirX * move_speed
        next_y = posY - dirY * move_speed
        if worldMap[int(posY)][int(next_x)] == 0:
            posX = next_x
        if worldMap[int(next_y)][int(posX)] == 0:
            posY = next_y

    # Rotate left
    if keys[pygame.K_a]:
        old_dir_x = dirX
        dirX = dirX * math.cos(rot_speed) - dirY * math.sin(rot_speed)
        dirY = old_dir_x * math.sin(rot_speed) + dirY * math.cos(rot_speed)
        old_plane_x = planeX
        planeX = planeX * math.cos(rot_speed) - planeY * math.sin(rot_speed)
        planeY = old_plane_x * math.sin(rot_speed) + planeY * math.cos(rot_speed)

    # Rotate right
    if keys[pygame.K_d]:
        old_dir_x = dirX
        dirX = dirX * math.cos(-rot_speed) - dirY * math.sin(-rot_speed)
        dirY = old_dir_x * math.sin(-rot_speed) + dirY * math.cos(-rot_speed)
        old_plane_x = planeX
        planeX = planeX * math.cos(-rot_speed) - planeY * math.sin(-rot_speed)
        planeY = old_plane_x * math.sin(-rot_speed) + planeY * math.cos(-rot_speed)




# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             sys.exit()

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    handle_input()
    screen.fill((0, 0, 0))
    raycaster()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


