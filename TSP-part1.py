import numpy as np
import matplotlib.pyplot as plt

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


all_pts = []

def start_anneal():
    for i in range(20): #total numper of points
        all_pts.append(Coordinate(np.random.uniform(),np.random.uniform()))

    fig = plt.figure(figsize=(10,5))
    ax1 = fig.add_subplot(121)

    for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
        ax1.plot([pt1.x, pt2.x], [pt1.y, pt2.y], 'b')
    ax1.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], 'b')

    for pt in all_pts:
        ax1.plot(pt.x,pt.y, 'ro')

    #plt.show()

    cost0 = Coordinate.get_total_distance(all_pts)

    #Variables
    temp = 30 #temperature
    alpha = 0.99 #alpha value
    temp_init = temp

    for i in range(1000): #Set
        print(i,': cost= ', cost0)

        temp = temp*alpha

        for j in range(500): #Set
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

    ax2 = fig.add_subplot(122)
    for pt1, pt2 in zip(all_pts[:-1], all_pts[1:]):
        ax2.plot([pt1.x, pt2.x], [pt1.y, pt2.y], 'b')
    ax2.plot([all_pts[0].x,all_pts[-1].x],[all_pts[0].y,all_pts[-1].y], 'b')

    for pt in all_pts:
        ax2.plot(pt.x,pt.y, 'ro')
    plt.show()


def main():
    start_anneal()

if __name__ == '__main__':
    main()
