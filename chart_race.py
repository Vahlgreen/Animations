
import matplotlib
import bar_chart_race as bcr
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.animation import PillowWriter
import numpy as np
import time
import pandas as pd
from IPython import display


data = pd.read_csv("ejendomspriser.csv", sep=";")
ejendomsspriser_kolonner = [f"{i}" for i in range(len(data.columns))]
data=data.rename(columns={data.columns[i]:ejendomsspriser_kolonner[i] for i in range(len(data.columns))})
data = data.drop([0,1],axis=0).reset_index(drop=True)
municipalities = list(data["2"])
data = data.drop(["0","1","2"],axis=1)
data=data.fillna(0)

#rows to display:
# 0: københavn
# 1: Frederiksberg
# 53: Odense
# 78: århus
rows = [0,2,3,4,5,6,10,12,13,15,16,17,20,23,24,25,26,27,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51,52,53,54,57,59,60,61,62,63,64,65,66,67,68,69,70,71,72,73]
data = data.iloc[rows,:]
mun_to_disp = [municipalities[i] for i in rows]
for i in data.columns:
    try:
        data[i] = pd.to_numeric(data[i])
    except:
        pass
dates = []
for i in range(117):
    if i%4==0:
        dates.append(f"{int(1992+i/4)} k1")
    if i%4==1:
        dates.append(f"{int(1992+i/4)} k2")
    if i%4==2:
        dates.append(f"{int(1992+i/4)} k3")
    if i%4==3:
        dates.append(f"{int(1992+i/4)} k4")


data=data.transpose()
data.set_index(np.array(dates), drop=True, inplace=True)
data = data.rename(columns={data.columns[i]:mun_to_disp[i] for i in range(len(mun_to_disp))})

bcr.bar_chart_race(
    df=data,
    filename='barchart_race(many mun).mp4',
    orientation='h',
    sort='desc',
    label_bars=True,
    steps_per_period=10,
    figsize=(6.5, 3.5),
    cmap='dark24',
    title='Gennemsnitlig kvm pris i DKK',
    bar_label_size=7,
    tick_label_size=7,
    dpi=200,
    fig=None)