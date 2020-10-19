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
pixel_stride = 5 #Length of pixel sampling.
temp = 80 #start temperature
alpha = 0.993 #alpha value
temp_init = temp #ref to start temperature
markov_chain_count = 2000 #Number of markov chains
markov_chain_length = 500 #Length of markov chains
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

    @staticmethod
    def get_total_distance(all_pts):
        dist = 0
        for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
            dist += Coordinate.get_distance(pt1, pt2)
        dist += Coordinate.get_distance(all_pts[0], all_pts[-1])
        return dist

#------------------------------------------------------------------------------#

#----------------------------Get Image-----------------------------------------#
img = cv2.imread('test.jpg')
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 30, 255, cv2.THRESH_BINARY_INV)

# cv2.imshow("Image",blackAndWhiteImage)
# cv2.waitKey(0)

height, width = blackAndWhiteImage.shape
all_pts = []

for x in range(0, height, pixel_stride):
    for y in range(0, width, pixel_stride):
        r = random.random()
        if blackAndWhiteImage[x,y] == 255 and r < 0.3:
            all_pts.append(Coordinate(y,-x))

#------------------------------------------------------------------------------#
#-------------------------------Annealing--------------------------------------#
cost0 = Coordinate.get_total_distance(all_pts)

for i in range(markov_chain_count):
    clear()
    print(i,'/',markov_chain_count,': Total Length = ', cost0)
    temp = temp*alpha

    for j in range(markov_chain_length):
        #swap two points
        r1, r2 = np.random.randint(0, len(all_pts), size=2)
        tmp = all_pts[r1]
        all_pts[r1] = all_pts[r2]
        all_pts[r2] = tmp

        cost1 = Coordinate.get_total_distance(all_pts)

        if cost1 < cost0:
            cost0 = cost1
        else:
            x = np.random.uniform()
            if x < np.exp((cost0-cost1)/temp):
                cost0 = cost1
            else:
                tmp = all_pts[r1]
                all_pts[r1] = all_pts[r2]
                all_pts[r2] = tmp

#------------------------------------------------------------------------------#
#----------------------------Plotting------------------------------------------#
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot()
fig.canvas.set_window_title('Annealing')
linecolor = CB91_Blue
dotcolor = '#ffffff'

for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
    ax.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor)
ax.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], linecolor)
# for pt in all_pts:
#     ax.plot(pt.x,pt.y, marker='o', color=dotcolor, markersize=1)

ax.axis('tight')
ax.axis('off')
plt.show()
