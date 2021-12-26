import random

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
import time
import pandas as pd
from IPython import display


#read and clean data
data = pd.read_csv("ejendomspriser.csv", sep=";")
ejendomsspriser_kolonner = [f"{i}" for i in range(len(data.columns))]
data=data.rename(columns={data.columns[i]:ejendomsspriser_kolonner[i] for i in range(len(data.columns))})
data = data.drop([0,1],axis=0).reset_index(drop=True)
municipalities = list(data["2"])
data = data.drop(["0","1","2"],axis=1)
data=data.fillna(0)
rows = [0,53,78,29]
data = data.iloc[rows,:]
mun_to_disp = [municipalities[i] for i in rows]

#instanciate lines and associated legends
num_lines = len(rows)
plotcolors = []
for i in range(num_lines):
    r = random.random()
    b = random.random()
    g = random.random()
    plotcolors.append((r,b,g))


plt.style.use('dark_background')
fig = plt.figure()
ax = plt.axes()

#removes decimals from years
def xtickerformat(x,p):
    if ".25" in str(x):
        return f"{str(x).split('.')[0]} K2"
    if ".5" in str(x):
        return f"{str(x).split('.')[0]} K3"
    if ".75" in str(x):
        return f"{str(x).split('.')[0]} K4"
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
plt.ylabel("DKK")
plt.xlabel("År")


lines=[]
for index in range(num_lines):
    lobj = ax.plot([],[],lw=2,color=plotcolors[index])[0]
    lines.append(lobj)
ax.legend(handles=lines, labels=mun_to_disp,loc="upper left")


def init():
    for line in lines:
        line.set_data([], [],[])
    return lines,

# lists to store x and y axis points
axis_points_dict = {}
axis_points_dict["x1"]=[]
for i in range(num_lines):
    axis_points_dict[f"y{i}"] = []

#some rows contain ".." which will fail later in "animate"
for i in data.columns:
    try:
        data[i] = pd.to_numeric(data[i])
    except:
        pass

def animate(i):
    #0: københavn
    #1: Frederiksberg
    #53: Odense
    #78: århus

    if i==0:
        axis_points_dict["x1"].append(1992)
    else:
        axis_points_dict["x1"].append(axis_points_dict["x1"][-1]+1/4)

    for j in range(num_lines):
        axis_points_dict[f"y{j}"].append(data.iloc[j,i])

    #for dynamic axis
    #ax.set_ylim(min(y1), max(y1)+max(y1)*0.1)  # added ax attribute here
    #ax.set_xlim(x1[0],x1[i]+2)

    for lnum,line in enumerate(lines):
        line.set_data(axis_points_dict["x1"], axis_points_dict[f"y{lnum}"]) # set data for each line separately.


    return lines



plt.title('Gennemsnitlig kvm pris i danske kommuner')

# hiding the axis details
#plt.axis('off')
#plt.xticks(color="black")


anim = animation.FuncAnimation(fig, animate,frames=data.shape[1], interval=100, blit=True,repeat_delay=10000)

# save the animation as mp4 or gif file
mywriter = animation.FFMpegWriter()
anim.save('animated_graph.mp4', writer=mywriter)
#anim.save('test.gif', writer='imagemagick')
#anim.save('test.gif', dpi=200, writer=PillowWriter(fps=10))


plt.show()