import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

#----------------------------Setup---------------------------------------------#
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

all_pts = []

#Variables
temp = 30 #start temperature
alpha = 0.99 #alpha value
temp_init = temp #ref to start temperature
markov_chain_count = 1000 #Number of markov chains
markov_chain_length = 250 #Length of markov chains
number_of_points = 20 #Total number of points
fig = plt.figure(figsize=(7,7))
ax = fig.add_subplot()
fig.canvas.set_window_title('Annealing')

#---------------------------------Utility--------------------------------------#
def clear():

    # for windows
    if name == 'nt':
        _ = system('cls')

    # for mac and linux(here, os.name is 'posix')
    else:
        _ = system('clear')
#------------------------------------------------------------------------------#

#------------------------------Methods-----------------------------------------#
def plot_data_anim():
    linecolor = CB91_Blue
    dotcolor = '#ffffff'

    for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
        ax.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor)
    ax.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], linecolor)


    for pt in all_pts:
        ax.plot(pt.x,pt.y,marker='o', color= linecolor,markersize=18)
        ax.plot(pt.x,pt.y, marker='o', color=dotcolor, markersize=12)


    ax.axis('tight')
    ax.axis('off')

    txt = "Length = " + str(round(cost0,2))
    txt2 = "Temp = " + str(round(temp,2))
    ax.text(0, 1, txt, style='oblique', color='#ffffff',
            bbox={'facecolor': '#21415f', 'alpha': 1.0, 'pad': 10})

    ax.text(0, 0.9, txt2, style='oblique', color='#ffffff',
            bbox={'facecolor': '#21415f', 'alpha': 1.0, 'pad': 10})
    plt.draw()
    plt.pause(0.000005)
    ax.clear()

def plot_data_final():

    plt.close(fig)
    fig2 = plt.figure(figsize=(7,7))
    fig2.canvas.set_window_title('Annealing')
    ax2 = fig2.add_subplot()
    linecolor = CB91_Blue
    dotcolor = '#ffffff'

    for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
        ax2.plot([pt1.x, pt2.x], [pt1.y, pt2.y], linecolor)
    ax2.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], linecolor)


    for pt in all_pts:
        ax2.plot(pt.x,pt.y,marker='o', color= linecolor,markersize=18)
        ax2.plot(pt.x,pt.y, marker='o', color=dotcolor, markersize=12)


    ax2.axis('tight')
    ax2.axis('off')

    txt = "Length = " + str(round(cost0,2))
    txt2 = "Temp = " + str(round(temp,2))
    ax2.text(0, 1, txt, style='oblique', color='#ffffff',
            bbox={'facecolor': '#21415f', 'alpha': 1.0, 'pad': 10})

    ax2.text(0, 0.9, txt2, style='oblique', color='#ffffff',
            bbox={'facecolor': '#21415f', 'alpha': 1.0, 'pad': 10})

    plt.show()

#------------------------------------------------------------------------------#
for i in range(number_of_points): # set total numper of points
    all_pts.append(Coordinate(np.random.uniform(),np.random.uniform()))

cost0 = Coordinate.get_total_distance(all_pts)

for i in range(markov_chain_count):
    clear()
    print(i,': Total Length = ', cost0)
    plot_data_anim()
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

plot_data_final()
#------------------------------------------------------------------------------#
