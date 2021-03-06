import cv2
import numpy as np
import matplotlib
matplotlib.use('Agg')
from matplotlib import pyplot as plt
import os
from os import system, name
import random
import enum
import time

#------------------------Imgage Selection--------------------------------------#
anim = False #set to true if snapshots of the process should be saved every 5 secs
class Images(enum.Enum):
   Hitler = 1
   Sam = 2
   Riaan = 3

#Set your image here!
#   -Images.Hitler
#   -Images.Sam
#   -Images.Riaan
selected_image = Images.Riaan

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
#--------------------------------Images----------------------------------------#
image_name = "hitler.jpg" #Name of image
thresh = 145 #Threshold boundry 0-255
ignore_chance = 0.6 #Chance a sample point will be ignored
pixel_stride = 2 #Length of pixel sampling.
figure_size = (4.5,8) #Figure size
savepath = "Result/Hitler/" #Save path for slideshow

# Set Variables
if selected_image == Images.Hitler:
    image_name = "Finals/hitler.jpg"
    thresh = 145
    thresh_type = cv2.THRESH_BINARY
    ignore_chance = 0.6
    pixel_stride = 2
    figure_size = (4.5,8)
    savepath = "Result/Hitler/"
elif selected_image == Images.Sam:
    image_name = "Finals/sam.jpg"
    thresh = 45
    thresh_type = cv2.THRESH_BINARY_INV
    ignore_chance = 0.6
    pixel_stride = 3
    figure_size = (5,7)
    savepath = "Result/Sam/"
elif selected_image == Images.Riaan:
    image_name = "Finals/riaan.jpg"
    thresh = 140
    thresh_type = cv2.THRESH_BINARY_INV
    ignore_chance = 0.4
    pixel_stride = 2
    figure_size = (6,8)
    savepath = "Result/Riaan/"

if anim:
    os.system('rm -rf '+ savepath)
    os.system('mkdir ' + savepath)

#------------------------------------------------------------------------------#
#----------------------------Plotting------------------------------------------#
fig = plt.figure(figsize=figure_size)
ax = fig.add_subplot()
fig.canvas.set_window_title('TSP')

def plot_data_save():

    fig = plt.figure(figsize=figure_size)
    ax = fig.add_subplot()
    fig.canvas.set_window_title('TSP')
    linecolor = CB91_Blue

    for pt1, pt2 in zip(solution[:-1], solution[1:]):
        ax.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor, linewidth=0.5)

    plt.axis('equal')
    ax.axis('tight')
    ax.axis('off')
    plt.savefig(savepath+str(round(time.time()))+".png")

def plot_data_final():
    matplotlib.use('TkAgg')
    fig2 = plt.figure(figsize=figure_size)
    ax2 = fig2.add_subplot()
    fig2.canvas.set_window_title('TSP')
    linecolor = CB91_Blue

    for pt1, pt2 in zip(solution[:-1], solution[1:]):
        ax2.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor, linewidth=0.5)

    ax2.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], linecolor, linewidth=0.5)

    plt.axis('equal')
    ax2.axis('tight')
    ax2.axis('off')
    plt.show()

#---------------------------------Utility--------------------------------------#
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
img = cv2.imread(image_name)
grayImage = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
(thresh, blackAndWhiteImage) = cv2.threshold(grayImage, thresh, 255, thresh_type)

# cv2.imshow("Image",blackAndWhiteImage)
# cv2.waitKey(0)

height, width = blackAndWhiteImage.shape
all_pts = []

for x in range(0, height, pixel_stride):
    for y in range(0, width, pixel_stride):
        r = random.random()
        if blackAndWhiteImage[x,y] == 255 and r < ignore_chance:
            all_pts.append(Coordinate(y,-x))

#------------------------------------------------------------------------------#
#-------------------TSP Nearest Neighbour--------------------------------------#

solution = []
current_pt = np.random.randint(0, len(all_pts))
next_pt = np.random.randint(0, len(all_pts))
if next_pt == current_pt:
    if next_pt == 0:
        next_pt = current_pt + 1
    else:
        next_pt = current_pt - 1
solution.append(all_pts[current_pt])
last_save = 0

while(len(solution) != len(all_pts)):
    clear()
    print("This might take a while. Please be patient.")
    comp = round(len(solution)/len(all_pts)*100.0,2)
    print("Progress: ",str(comp),'%')
    if last_save < time.time() and anim:
        plot_data_save()
        last_save = time.time()+5.0
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
plot_data_final()
