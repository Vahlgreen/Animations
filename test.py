import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
import time
import pandas as pd
from IPython import display

plt.style.use('dark_background')

fig = plt.figure()
ax = plt.axes(xlim=(0, 150), ylim=(5000, 8000))
ax.set_frame_on(False)
ax.axes.get_xaxis().set_visible(False)


line, = ax.plot([], [], lw=2)
plotcols=["red","blue","green"]
lines=[]
plt.ylabel("kr")
for index in range(3):
    lobj = ax.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)


def init():
    # creating an empty plot/frame
    for line in lines:
        line.set_data([], [],[])
    return lines,


# lists to store x and y axis points
x1 = []
y1, y2, y3 = [], [], []

data = pd.read_csv("ejendomspriser.csv", sep=";")
ejendomsspriser_kolonner = [f"{i}" for i in range(len(data.columns))]
data=data.rename(columns={data.columns[i]:ejendomsspriser_kolonner[i] for i in range(len(data))})
data = data.drop([0,1],axis=0).reset_index(drop=True)
data = data.drop(["0","1","2"],axis=1)
data=data.fillna(0)
# animation function
ax.legend(handles=lines, labels=["København","Odense","Århus"],loc="best")
def animate(i):
    #0: københavn
    #1: Frederiksberg
    #53: Odense
    #78: århus

    # appending new points to x, y axes points list

    x1.append(i)
    y1.append(int(data.iloc[0,i]))
    y2.append(int(data.iloc[53,i]))
    y3.append(int(data.iloc[78,i]))
    ax.set_ylim(min(y1), max(y1)+max(y1)*0.1)  # added ax attribute here

    ylist = [y1, y2, y3]
    for lnum,line in enumerate(lines):
        line.set_data(x1, ylist[lnum]) # set data for each line separately.


    return lines


# setting a title for the plot
plt.title('Gennemsnitlig kvm pris i danske kommuner')
# hiding the axis details
#plt.axis('off')
plt.xticks(color="black")
# call the animator


anim = animation.FuncAnimation(fig, animate,frames=data.shape[1], interval=150, blit=True,repeat_delay=10000)






# save the animation as mp4 video file
#anim.save('test.gif', writer='imagemagick')
anim.save('test.gif', dpi=200, writer=PillowWriter(fps=10))


plt.show()