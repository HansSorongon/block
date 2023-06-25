import numpy as np
import pygame
import sys

import pygame_widgets
from pygame_widgets.slider import Slider
from pygame_widgets.toggle import Toggle

def connect_points(point_a, point_b):
    pygame.draw.line(screen, 'green', (point_a[0], point_a[1]),
                     (point_b[0], point_b[1]), 3)

fps = 0
fpsClock = pygame.time.Clock()

(width, height) = (1000, 800)
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Block")

pygame.init()

zoom_slider = Slider(screen, width - 220, 20, 200, 20, min = 0.001, max = 8, step = 0.01,
        colour='white', handleRadius=8)

speed_slider = Slider(screen, width - 220, 60, 200, 20, min = 0.00005, max =
        0.005,
        step = 0.00001,
        colour='white', handleRadius=8)

rot_slider_y = Slider(screen, width - 220, 100, 200, 20, min = 1, max =
        10,
        step = 0.001,
        colour='white', handleRadius=8)

rot_slider_z = Slider(screen, width - 220, 140, 200, 20, min = 1, max =
        10,
        step = 0.001,
        colour='white', handleRadius=8)

rot_slider_x = Slider(screen, width - 220, 180, 200, 20, min = 1, max =
        10,
        step = 0.001,
        colour='white', handleRadius=8)

free_toggle = Toggle(screen, width - 50, 225, 30, 20, startOn = True)

font = pygame.font.Font(None, 16)
zoom_text = font.render('Zoom', True, 'white')
speed_text = font.render('Speed', True, 'white')
zoom_text_rect = (width - 220, 5)
speed_text_rect = (width - 220, 45)

# Variables

points = []

angle = 0

projection_matrix = [[1, 0, 0], [0, 1, 0]]

projection_matrix = np.array(projection_matrix)

distance = 20

origin = [screen.get_width() / 2, screen.get_height() / 2]
v1 = [origin[0] - 50, origin[1] - 50, -50]
v2 = [origin[0] + 50, origin[1] - 50, -50]
v3 = [origin[0] + 50, origin[1] + 50, -50]
v4 = [origin[0] - 50, origin[1] + 50, -50]
v5 = [origin[0] - 50, origin[1] - 50, 50]
v6 = [origin[0] + 50, origin[1] - 50, 50]
v7 = [origin[0] + 50, origin[1] + 50, 50]
v8 = [origin[0] - 50, origin[1] + 50, 50]

v1 = np.array(v1)
v2 = np.array(v2)
v3 = np.array(v3)
v4 = np.array(v4)
v5 = np.array(v5)
v6 = np.array(v6)
v7 = np.array(v7)
v8 = np.array(v8)

points.append(v1)
points.append(v2)
points.append(v3)
points.append(v4)
points.append(v5)
points.append(v6)
points.append(v7)
points.append(v8)

# Game loop.

while True:

    screen.fill((0, 0, 0))

    screen.blit(zoom_text, zoom_text_rect)
    screen.blit(speed_text, speed_text_rect)

    dist = zoom_slider.getValue()

    events = pygame.event.get()

    for event in events:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                pygame.quit()
                sys.exit()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEWHEEL:
            if (event.y == 1):
                if (zoom_slider.value < zoom_slider.max - 0.2):
                    zoom_slider.value += 0.3
            elif (event.y == -1):
                if (zoom_slider.value > zoom_slider.min + 0.1):
                    zoom_slider.value -= 0.3


  # Update.

    speed = speed_slider.value
    y_angle = rot_slider_y.value
    z_angle = rot_slider_z.value
    x_angle = rot_slider_x.value

    if (free_toggle.value):
        angle += 1 * speed

        rot_slider_x.setValue(5.5)
        rot_slider_y.setValue(5.5)
        rot_slider_z.setValue(5.5)

        y_angle = angle
        z_angle = angle
        x_angle = angle

    rotation_matrix_z = [[np.cos(z_angle), -np.sin(z_angle), 0],
                         [np.sin(z_angle), np.cos(z_angle), 0], [0, 0, 1]]

    rotation_matrix_x = [[1, 0, 0], [0, np.sin(x_angle), np.cos(x_angle)],
                         [0, np.cos(x_angle), -np.sin(x_angle)]]

    rotation_matrix_y = [[np.cos(y_angle), 0, -np.sin(y_angle)], [0, 1, 0],
                         [np.sin(y_angle), 0, np.cos(y_angle)]]

    np.array(rotation_matrix_x)
    np.array(rotation_matrix_y)
    np.array(rotation_matrix_z)

    projected_points = []

  # Draw.

    for point in points:

    # translate vector to origin

        translate = [point[0] - origin[0], point[1] - origin[1],
                     point[2]]

    # rotate vector about origin

        rotated = np.matmul(rotation_matrix_y, translate)
        rotated = np.matmul(rotation_matrix_z, rotated)
        rotated = np.matmul(rotation_matrix_x, rotated)

    # translate back rotated

        rotated_translated = [rotated[0] + 1 / dist * origin[0],
                              rotated[1] + 1 / dist * origin[1], 0]

        z = dist - rotated_translated[2]
        projection_matrix = [[z, 0, 0], [0, z, 0]]
        projection_matrix = np.array(projection_matrix)

    # project matrix

        projected = np.matmul(projection_matrix, rotated_translated)

        projected_points.append(projected)

    connect_points(projected_points[0], projected_points[1])
    connect_points(projected_points[1], projected_points[2])
    connect_points(projected_points[2], projected_points[3])
    connect_points(projected_points[0], projected_points[3])

    connect_points(projected_points[4], projected_points[5])
    connect_points(projected_points[5], projected_points[6])
    connect_points(projected_points[6], projected_points[7])
    connect_points(projected_points[7], projected_points[4])

    connect_points(projected_points[0], projected_points[4])
    connect_points(projected_points[1], projected_points[5])
    connect_points(projected_points[2], projected_points[6])
    connect_points(projected_points[3], projected_points[7])

    for projected_point in projected_points:
        pygame.draw.circle(screen, 'blue', [projected_point[0],
                           projected_point[1]], 5)

  # connect_points(points[0], points[1])

    pygame_widgets.update(events)
    pygame.display.update()
    fpsClock.tick(fps)
