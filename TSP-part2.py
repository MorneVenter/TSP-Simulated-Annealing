import cv2
import numpy as np
from matplotlib import pyplot as plt


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
pixel_stride = 3
#------------------------------------------------------------------------------#

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
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, 65, 255, cv2.THRESH_BINARY)

# cv2.imshow("Image",blackAndWhiteImage)
# cv2.waitKey(0)

height, width = blackAndWhiteImage.shape
all_pts = []

for x in range(0, height, pixel_stride):
    for y in range(0, width, pixel_stride):
        if blackAndWhiteImage[x,y] == 255:
            all_pts.append(Coordinate(y,-x))

#------------------------------------------------------------------------------#
#----------------------------Plotting------------------------------------------#
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot()
fig.canvas.set_window_title('Annealing')
linecolor = CB91_Blue
dotcolor = '#ffffff'

for pt in all_pts:
    ax.plot(pt.x,pt.y, marker='o', color=dotcolor, markersize=1)

ax.axis('tight')
ax.axis('off')
plt.show()
