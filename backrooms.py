import pygame
import math
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Backrooms")

clock = pygame.time.Clock()

# egér lock
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Player
player_x, player_y = 3, 3
player_angle = 0

# Monster
monster_x, monster_y = 6, 6

# Map
game_map = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,0,1,0,1,0,0,1],
    [1,0,1,0,1,0,1,0,0,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,1,0,1],
    [1,1,1,1,1,1,1,1,1,1],
]

def is_wall(x, y):
    try:
        return game_map[int(y)][int(x)] == 1
    except:
        return True

def cast_rays():
    for ray in range(0, WIDTH, 2):
        angle = player_angle - math.pi/6 + (ray / WIDTH) * (math.pi/3)

        for depth in range(1, 60):
            target_x = player_x + math.cos(angle) * depth * 0.05
            target_y = player_y + math.sin(angle) * depth * 0.05

            if is_wall(target_x, target_y):
                shade = max(0, 255 - depth * 5)
                color = (shade, shade, 80)
                height = 500 / (depth * 0.1 + 0.0001)
                pygame.draw.rect(screen, color, (ray, HEIGHT//2 - height//2, 2, height))
                break

running = True
while running:
    dt = clock.tick(60)

    # flicker fény
    flicker = random.randint(-10, 10)
    screen.fill((30 + flicker, 30 + flicker, 20))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # egér kamera
    mouse_dx, _ = pygame.mouse.get_rel()
    player_angle += mouse_dx * 0.003

    keys = pygame.key.get_pressed()

    speed = 0.05
    if keys[pygame.K_LSHIFT]:
        speed = 0.09

    new_x, new_y = player_x, player_y

    # mozgás
    if keys[pygame.K_w]:
        new_x += math.cos(player_angle) * speed
        new_y += math.sin(player_angle) * speed
    if keys[pygame.K_s]:
        new_x -= math.cos(player_angle) * speed
        new_y -= math.sin(player_angle) * speed
    if keys[pygame.K_a]:
        new_x += math.cos(player_angle - math.pi/2) * speed
        new_y += math.sin(player_angle - math.pi/2) * speed
    if keys[pygame.K_d]:
        new_x += math.cos(player_angle + math.pi/2) * speed
        new_y += math.sin(player_angle + math.pi/2) * speed

    # ütközés
    if not is_wall(new_x, player_y):
        player_x = new_x
    if not is_wall(player_x, new_y):
        player_y = new_y

    # szörny AI (lassan követ)
    dx = player_x - monster_x
    dy = player_y - monster_y
    dist = math.sqrt(dx*dx + dy*dy)

    if dist > 0:
        monster_x += dx/dist * 0.01
        monster_y += dy/dist * 0.01

    # game over
    if dist < 0.5:
        print("ELKAPOTT 😱")
        running = False

    cast_rays()

    pygame.display.flip()

pygame.quit()
