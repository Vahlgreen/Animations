import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
import time
import pandas as pd
from IPython import display

plt.style.use('dark_background')


fig = plt.figure()
ax = plt.axes()
#removes decimals from years
def xtickerformat(x,p):
    if ".25" in str(x):
        return f"{str(x).split('.')[0]} K1"
    if ".5" in str(x):
        return f"{str(x).split('.')[0]} K2"
    if ".75" in str(x):
        return f"{str(x).split('.')[0]} K3"
    if ".0" in str(x):
        return str(x).split(".")[0]

#format axis and frame
ax.set_frame_on(False)
#ax.axes.get_xaxis().set_visible(False)
ax.set_ylim(0,60000)
ax.set_xlim(1992,2021)
ax.get_yaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, p: format(int(x), ',').replace(",",".")))
#ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,p: int(x)))
ax.get_xaxis().set_major_formatter(matplotlib.ticker.FuncFormatter(xtickerformat))
plt.ylabel("danske kroner")
plt.xlabel("år")

#instanciate lines and associated legend
plotcols=["red","blue","green"]
lines=[]
for index in range(3):
    lobj = ax.plot([],[],lw=2,color=plotcols[index])[0]
    lines.append(lobj)
ax.legend(handles=lines, labels=["København","Odense","Århus"],loc="upper left")

def init():
    for line in lines:
        line.set_data([], [],[])
    return lines,


# lists to store x and y axis points
x1, y1, y2, y3 = [], [], [], []

#read and clean data
data = pd.read_csv("ejendomspriser.csv", sep=";")
ejendomsspriser_kolonner = [f"{i}" for i in range(len(data.columns))]
data=data.rename(columns={data.columns[i]:ejendomsspriser_kolonner[i] for i in range(len(data))})
data = data.drop([0,1],axis=0).reset_index(drop=True)
data = data.drop(["0","1","2"],axis=1)
data=data.fillna(0)


def animate(i):
    #0: københavn
    #1: Frederiksberg
    #53: Odense
    #78: århus

    if i==0:
        x1.append(1992)
    else:
        x1.append(x1[-1]+1/4)
    y1.append(int(data.iloc[0,i]))
    y2.append(int(data.iloc[53,i]))
    y3.append(int(data.iloc[78,i]))

    #for dynamic axis
    #ax.set_ylim(min(y1), max(y1)+max(y1)*0.1)  # added ax attribute here
    #ax.set_xlim(x1[0],x1[i]+2)

    ylist = [y1, y2, y3]
    for lnum,line in enumerate(lines):
        line.set_data(x1, ylist[lnum]) # set data for each line separately.


    return lines



plt.title('Gennemsnitlig kvm pris i danske kommuner')

# hiding the axis details
#plt.axis('off')
#plt.xticks(color="black")
# call the animator


anim = animation.FuncAnimation(fig, animate,frames=data.shape[1], interval=50, blit=True,repeat_delay=10000)

# save the animation as mp4 or gif file
mywriter = animation.FFMpegWriter()
anim.save('three_largest.mp4', writer=mywriter)
#anim.save('test.gif', writer='imagemagick')
#anim.save('test.gif', dpi=200, writer=PillowWriter(fps=10))


plt.show()