import numpy as np
import math


#TODO 
# add error of measurement


#global inputs
global_width = float(3.45)
global_length = float(5.45)
global_height = float(2.60)
#   distance from left, front, floor wall
global_speaker = [float(1.0), float(0.80), float(1.10), float(math.degrees(60))]


#edge vectors
origin = [0, 0, 0]
width = [global_width, 0, 0]
length = [0, global_length, 0]
height = [0, 0, global_height]
floor_diagonal = np.add(width, length)
side_diagonal = np.add(length, height)
rear_diagonal = np.add(width, height)
body_diagonal = np.add(height, floor_diagonal)
#location points
speaker_1 = [global_speaker[0], global_length-global_speaker[1], global_speaker[2]]
speaker_2 = [global_width-speaker_1[0], speaker_1[1], speaker_1[2]]
listener = [
    width[0]/2,
    speaker_1[1]-((width[0]/2 - speaker_1[0]) * (3 ** 0.5)),
    speaker_1[2]
]

#finds plane eq: ax+by+cz=d
#TODO
#give a simplest coefficient eq
def plane(p1, p2, p3):
    p1p2 = np.subtract(p2, p1)
    p1p3 = np.subtract(p3, p1)
    n = np.cross(p1p2, p1p3)
    d = np.dot(p1, n)
    eq = [n[0], n[1], n[2], d]
    return eq

#front wall
w1 = plane(length, floor_diagonal, body_diagonal)
#right wall
w2 = plane(body_diagonal, floor_diagonal, width)
#rear wall
w3 = plane(height, rear_diagonal, origin)
#left wall
w4 = plane(origin, length, height)
#ceiling
w5 = plane(height, side_diagonal, body_diagonal)
#floor
w6 = plane(origin, width, length)

#since ax+by+cz=d -> n=(a,b,c)
def normal(wall):
    return wall[:3]

def norm(wall):
    return (np.dot(normal(wall), normal(wall)))**0.5

def unit_normal(wall):
    return np.dot(1/norm(wall), normal(wall))

#p' = p + 2t(n)
def mirror_image(speaker, wall):
    n = normal(wall)
    t = (wall[3]-np.dot(n, speaker))/(np.dot(n, n))
    return np.add(speaker, np.dot(2, np.dot(t, n)))

def intersection(speaker, listener, wall):
    i = mirror_image(speaker, wall) 
    u = np.subtract(listener, i) 
    n = normal(wall)
    t = -(np.dot(n, i) - wall[3])/(np.dot(n, u))
    return np.add(i, np.dot(t, u))

def mirror_image_2(speaker, wall1, wall2):
    return mirror_image((mirror_image(speaker, wall1)), wall2)


a = speaker_2
w = w4
print(
    speaker_2, "\n",
    mirror_image_2(speaker_2, w3, w4)
)



