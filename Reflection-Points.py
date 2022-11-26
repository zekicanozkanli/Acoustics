import numpy as np
import math


#TODO 
# add error of measurement


#global inputs
global_width = 3.43
global_length = 5.45
global_height = 2.60
#   distance from left, front, floor wall
global_speaker = [1.0, 0.80, 1.10, math.degrees(60)]


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

speakers = [speaker_1, speaker_2]
walls = [w1, w2, w3, w4, w5, w6]

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

def mirror_image_2(speaker, wall1, wall2):
    return mirror_image((mirror_image(speaker, wall1)), wall2)

#TODO
#sometimes p.dot(n, u)=0. solve this error 
def intersection(p1, p2, wall):
    u = np.subtract(p2, p1) 
    n = normal(wall)
    t = -(np.dot(n, p1) - wall[3])/(np.dot(n, u))
    return np.add(p1, np.dot(t, u))

def frp(speaker, listener, wall):
    r1 = intersection(
        mirror_image(speaker, wall),
        listener,
        wall
    )
    r1 = np.around(r1, 3)
    return r1

def srp(speaker, listener, wall1, wall2):
    r2 = intersection(
        mirror_image_2(speaker, wall1, wall2),
        listener,
        wall2
    )
    r1 = intersection(
        r2,
        mirror_image(speaker, wall1),
        wall1
    )
    r1 = np.around(r1, 3)
    r2 = np.around(r2, 3)
    if np.array_equal(wall1, wall2):
        return ["No Solution - Since wall1 = wall2"]
    elif ((r1[0] or r2[0]) < 0) or ((r1[0] or r2[0]) > global_width):
        return ["No Solution - Since x is out of domain"]
    elif ((r1[1] or r2[1]) < 0) or ((r1[1] or r2[1]) > global_length):
        return ["No Solution - Since y is out of domain"]
    elif ((r1[2] or r2[2]) < 0) or ((r1[2] or r2[2]) > global_height):
        return ["No Solution - Since z is out of domain"]
    else:
        return [r1, r2]
    #return [r1, r2]

def first_reflection_points(speakers, listener, walls):
    s=0
    w=0
    index = 0
    for i in speakers:
        s+=1
        for j in walls:
            index +=1
            if w<6:
                w+=1
            else:
                w=1
            print(
                "Index:", index,
                "Speaker:", s,
                "Wall:", w,
                "r1", frp(i, listener, j), "\n"
            )

def second_reflection_points(speakers, listener, walls):
    s=0
    w1=0
    w2=0
    index = 0
    l = []
    for i in speakers:
        s+=1
        for j in walls:
            if w1<6:
                w1+=1
            else:
                w1=1
            for k in walls:
                index+=1
                if w2<6:
                    w2+=1
                else:
                    w2=1
                l += [(s, w1, w2, srp(i, listener, j, k))]
    return l
                #print(
                #    "Index:", index,
                #    "Speaker:", s,
                #    "Wall 1:", w1,
                #    "Wall 2:", w2,
                #    "r1:", srp(i, listener, j, k)[0],
                #    "r2:", srp(i, listener, j, k)[1], "\n"
                #)

#print("First Fucking Reflections")
#first_reflection_points(speakers, listener, walls) 
#print("Second Fucking Reflections")
q = second_reflection_points(speakers, listener, walls)

#for i in range(len(q)):
#    print(q[i])

print(q[-2])
print(q[-2][3])
print(q[-2][3][0])
print(q[-2][3][0][0])

