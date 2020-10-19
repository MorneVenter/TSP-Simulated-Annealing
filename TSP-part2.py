import cv2
import numpy as np
from matplotlib import pyplot as plt
from os import system, name
import random

#----------------------------Setup---------------------------------------------#
#Plotting
# Lets make our plots pretty, we are not hooligans.
CB91_Blue = '#2CBDFE'
CB91_Green = '#47DBCD'
CB91_Pink = '#F3A0F2'
CB91_Purple = '#9D2EC5'
CB91_Violet = '#661D98'
CB91_Amber = '#F5B14C'

color_list = [CB91_Blue, CB91_Pink, CB91_Green, CB91_Amber,
              CB91_Purple, CB91_Violet]
plt.rcParams['axes.prop_cycle'] = plt.cycler(color=color_list)
plt.rcParams['figure.facecolor'] = '#0d1a26'
#------------------------------------------------------------------------------#
# Variables
pixel_stride = 2 #Length of pixel sampling.
#------------------------------------------------------------------------------#
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
#------------------------------------------------------------------------------#
#------------------------Coordinates Class-------------------------------------#
#------------------------------------------------------------------------------#
class Coordinate:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    @staticmethod
    def get_distance(a ,b):
        return np.sqrt(np.abs(a.x-b.x) + np.abs(a.y-b.y))

#------------------------------------------------------------------------------#

#----------------------------Get Image-----------------------------------------#
img = cv2.imread('test.jpg')
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 145, 255, cv2.THRESH_BINARY)

# cv2.imshow("Image",blackAndWhiteImage)
# cv2.waitKey(0)

height, width = blackAndWhiteImage.shape
all_pts = []

for x in range(0, height, pixel_stride):
    for y in range(0, width, pixel_stride):
        r = random.random()
        if blackAndWhiteImage[x,y] == 255 and r < 0.6:
            all_pts.append(Coordinate(y,-x))

#------------------------------------------------------------------------------#
#-------------------TSP Nearest Neighbour--------------------------------------#
solution = []
current_pt = 0
next_pt = np.random.randint(0, len(all_pts))
solution.append(all_pts[current_pt])

while(len(solution) != len(all_pts)):
    clear()
    print(str(round(len(solution)/len(all_pts)*100.0, 2)),'%')
    for i in range(0,len(all_pts)):
        if i != current_pt:
            dist = Coordinate.get_distance(all_pts[current_pt], all_pts[i])
            curdist = Coordinate.get_distance(all_pts[current_pt], all_pts[next_pt])
            if dist < curdist and not(all_pts[i] in solution):
                next_pt = i

    solution.append(all_pts[next_pt])
    current_pt = next_pt
    next_pt = np.random.randint(0, len(all_pts))

#------------------------------------------------------------------------------#
#----------------------------Plotting------------------------------------------#
fig = plt.figure(figsize=(4,8))
ax = fig.add_subplot()
fig.canvas.set_window_title('TSP')
linecolor = CB91_Blue

for pt1, pt2 in zip(solution[:-1], solution[1:]):
    ax.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor, linewidth=0.5)
#ax.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], linecolor, linewidth=0.5)

# for pt in solution:
#     ax.plot(pt.x,pt.y, marker='o', color=dotcolor, markersize=0.75)

plt.axis('equal')
ax.axis('tight')
ax.axis('off')
plt.show()
