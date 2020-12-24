import time
import pygame
import math

pygame.init()

# images and caption
screen = pygame.display.set_mode((730, 500))

pygame.display.set_caption("Plane Visualizer")
logo = pygame.image.load('globe.png')
pygame.display.set_icon(logo)

snow = pygame.image.load('background.jpeg')
snow = pygame.transform.scale(snow, (490, 490))

plane_art = pygame.image.load('plane.png')
plane_art = pygame.transform.scale(plane_art, (30, 30))
#scale to plot x and y positions
scale_x = .424
scale_y = .86
# file location --- should be set here
coordinates = "D:\LOG.TXT"
dest = "D:\DES.TXT"

# trajectory_list
trajectory = []

# functions
def int_finder(alpha, pos_x, pos_y):
    font = pygame.font.Font('freesansbold.ttf', 20)
    display = font.render(str(alpha[pos_x][pos_y]), True, (31, 28, 28))
    return screen.blit(display, ((pos_x * 30) + 35, (pos_y * 30) + 10))


def background():
    screen.fill((5, 14, 57))


def recieve_input(string):
    x_pos = ""
    y_pos = ""
    for x in range(len(string)):
        if (string[x] == ',' or string[x] == ' '):
            for y in range(x + 1, len(string)):
                y_pos += (string[y])
            break
        x_pos += string[x]
    return float(x_pos), float(y_pos)


def display_stat(stat, pos_x, pos_y):
    font = pygame.font.Font('freesansbold.ttf', 15)
    display = font.render(str(stat), True, 'white')
    return screen.blit(display, ((pos_x), (pos_y)))


def format_time(to_format):
    return str(int(to_format // 60)) + "." + str(round(to_format % 60, 2))


def print_trajectory(alpha):
    font = pygame.font.Font('freesansbold.ttf', 20)
    for i in alpha:
        display = font.render(".", True, (255, 255, 0))
        screen.blit(display, (i[0] + 245, i[1] + 430))
def position(lon2, lat2):
  des_list = []
  dx = ((original_x - lon2) * 40000 * math.cos((original_y + lat2) * math.pi / 360) / 360) * 1000
  dy = ((original_y - lat2) * 40000 / 360) *1000
  des_list.append(dx)
  des_list.append(dy)
  return des_list

# array (this does not have a function right now)
graph_length = 15
beta = []
alpha = []
for t in range(graph_length):
    beta.append('.')
for x in range(len(beta)):
    alpha.append(beta)

# plane position
original_coor = open(coordinates)
coor_str = original_coor.readlines()
omega = recieve_input(coor_str[0])
original_x = omega[0]
original_y = omega[1]

#destination position
dest_coor = open(dest)
destinations = dest_coor.readlines()
last_dest = recieve_input(destinations[-1])
dest_x = last_dest[0]
dest_y = last_dest[1]
dest_x_y_values = position(dest_x, dest_y)#list of x y values for destination
#can you make it so there that in position dest[0] and dest[1] displays,like the code below used for the plane art
# screen.blit(plane_art, (233 + pos_x*scale_x, 430 - (pos_y*scale_y)))

pygame.draw.circle(screen, (0,0,255), (150, 50), 15, 1)
pos_x = 0.0
pos_y = 0.0

# Stats (these are to be taken with meters and seconds)
velocity = 0.0
altitude = 0.0
time_from_destination = 0.0
time_elapsed = 0.0
distance_traveled = 0.0
distance_remaining = 0.0

t0 = time.time()  # starts time
checker = 1  # time checker

# game_loop
runner = True
while runner:
    background()
    screen.blit(snow, (5, 5))
    pygame.draw.rect(screen, (14, 38, 125), (505, 10, 215, 290))
    pygame.draw.line(screen, 'black', (35, 445), (460, 445), 2)
    pygame.draw.line(screen, 'black', (247, 20), (247, 445), 2)
    screen.blit(plane_art, (233 + pos_x*scale_x, 430 - (pos_y*scale_y)))
    # add pos_x to 233 and pos_y to 430 for changes
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runner = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                checker = 0
                t0 = time.time()
                trajectory = []
                coor_file = open(coordinates)
                current = coor_file.readlines()
                temp = recieve_input(current[-1])
                original_x = temp[0]
                original_y = temp[1]

    # Changes_in_Stats

    t1 = time.time()
    time_elapsed = t1 - t0
    time_elapsed = format_time(round(time_elapsed, 1))

    display_stat("Time Elpased:", 510, 30)
    display_stat(time_elapsed, 670, 30)

    display_stat("Average Velocity:", 510, 70)
    display_stat(velocity, 670, 70)

    display_stat("Distance Traveled:", 510, 110)
    display_stat(distance_traveled, 670, 110)

    display_stat("Distance Remaining:", 510, 150)
    display_stat(distance_remaining, 670, 150)

    display_stat("Altitude:", 510, 190)
    display_stat(altitude, 670, 190)

    # prints trajectory. Stores coordinates for trajectory on line 135
    print_trajectory(trajectory)

    # change in position
    coor_file = open(coordinates)
    current = coor_file.readlines()
    temp = recieve_input(current[-1])  # last values of long and lat in the file
    temp_list = position(temp[0], temp[1])
    pos_x = 500
    pos_y = 430
    print(pos_x, pos_y)

    if int(t1 - t0) == checker:
        checker += 3
        temp = [int(pos_x), int(pos_y)]
        trajectory.append(temp)

    '''for x in range (len(alpha)):
    if x == 7: continue
    for y in range (len(alpha[0])):
      if y == 14: continue
      int_finder(alpha, x, y)'''
    pygame.display.update()

