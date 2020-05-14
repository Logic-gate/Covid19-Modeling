import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from states import States



class Draw:
    def __init__(self, df, path):
        self.path = path
        self.fig, self.axs = plt.subplots(2, figsize=(10, 8))
        self.fig.suptitle('Covid-19 Epidemic Sample Model', fontsize=16)
        self.ld =  ['Healthy', 
        'Covid-19(+)', 
        'Hospitalized', 
        'Cured', 
        'Self Cured',
        'Death Toll', 
        'Limbo', 
        'Total Cured']
        self.df = df[0]
        self.stateOfDay = df[1]
        self.MoversList = df[2]
        self.state = States()
        self.dayLimit = self.state.returnConfig('SampleDefaults', 'dayLimit', int)
        self.x = self.state.returnConfig('SampleDefaults', 'xLimit', int)
        self.y = self.state.returnConfig('SampleDefaults', 'yLimit', int)
        self.groupsize = self.state.returnConfig('SampleDefaults', 'groupSize', int)
        self.sampleSize = self.state.returnConfig('SampleDefaults', 'sampleSize', float)
        self.distance = self.state.returnConfig('SampleDefaults', 'distance', float)
        self.beds = self.state.returnConfig('SampleDefaults', 'numberOfBeds', float)
        self.distanceLimit = self.state.returnConfig("SampleDefaults", "distance", float)


    def setup_plot(self, day):
        self.axs[0].cla()
        self.scat = self.axs[0].scatter(self.df['X'], self.df['Y'], s=1, c=self.plt1color())
        for i in self.MoversList:
        	self.axs[0].scatter(self.df.loc[i,'X'], self.df.loc[i, 'Y'], s=6, 
        		facecolors='none', edgecolors='black')
        	self.axs[0].text(self.df.loc[i, 'X'] + 0.02, self.df.loc[i, 'Y'] +
                    0.02, str(i), fontsize=5)
        sDay = str(day)
        title = f"Day={sDay}, Group Size={self.groupsize}, Movers={self.sampleSize * 100}%, Infection Distance={self.distance}"
        self.axs[0].set_title(title, loc='center')
        title2 = f"Healthy={len(self.df[self.df['State'] == 0])}, Infected={len(self.df[self.df['State'] == 1])}, Dead={len(self.df[self.df['State'] == 3])}"
        self.axs[0].set_xlabel(title2)
        self.axs[0].set_yticklabels([])
        self.axs[0].set_xticklabels([])
        self.axs[0].tick_params(
	        which='both',     
	        bottom=False,     
	        top=False,        
	        right=False,      
	        left=False,         
	        labelbottom=True)  
     
        self.axs[1].set_yticklabels([])
        self.axs[1].set_xticklabels([])
        self.axs[1].cla()
        self.axs[1].plot(self.stateOfDay.Healthy, label=self.ld[0], color=self.plt2color()[0])
        self.axs[1].plot(self.stateOfDay['Covid-19(+)'], label=self.ld[1], color=self.plt2color()[1])
        self.axs[1].plot(self.stateOfDay.Hospitalized, label=self.ld[2], color=self.plt2color()[2])
        self.axs[1].plot(self.stateOfDay.Cured, label=self.ld[3], color=self.plt2color()[3])
        self.axs[1].plot(self.stateOfDay['Self Cured'], label=self.ld[4], color=self.plt2color()[4])
        self.axs[1].plot(self.stateOfDay.Dead, label=self.ld[5], color=self.plt2color()[5])
        self.axs[1].plot(self.stateOfDay.Limbo, label=self.ld[6], color=self.plt2color()[6])
        self.axs[1].plot(self.stateOfDay['Total Cured'], label=self.ld[7], color=self.plt2color()[7])
        self.axs[1].set_prop_cycle(color=self.plt2color())
        self.axs[1].legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.) 
        plt.tight_layout(rect=[0, 0.03, 1, 0.95])  
        plt.ion()
        plt.pause(0.5)
        plt.xlabel("Days")
        if day < 10:
            sDay = '0' + sDay
        title = f"{self.path}/days/Day{sDay}.png"
        plt.savefig(title)
        return

    

    def plt1color(self):
        cols = []
        for l in self.df.index:
            if self.df.loc[l, 'State'] == 1:  # Infected
                cols.append(self.state.stateColors(1))
            elif self.df.loc[l, 'State'] == 3:  # Dead
                cols.append(self.state.stateColors(3))
            elif self.df.loc[l, 'State'] == 2:  # Hospitalized
                cols.append(self.state.stateColors(2))
            elif self.df.loc[l, 'State'] == 4:  # Cured
                cols.append(self.state.stateColors(4))
            elif self.df.loc[l, 'State'] == 5:  # Limbo
                cols.append(self.state.stateColors(5))
            elif self.df.loc[l, 'State'] == 100:  #Total Cured
                cols.append(self.state.stateColors(100))
            else:
                cols.append('blue')  # Healthy
        return cols


    def plt2color(self):
        cols = []
        for i in self.stateOfDay.columns:
            if i == 'Covid-19(+)':  # Infected
                cols.append('red')
            elif i == 'Dead':  # Dead
                cols.append('black')
            elif i == 'Hospitalized':  # Hospitalized
                cols.append('orange')
            elif i == 'Cured':  # Cured
                cols.append('green')
            elif i == 'Self Cured':  # limbo
                cols.append('cyan')
            elif i == 'Limbo':  # limbo
                cols.append('yellow')
            elif i == 'Total Cured':  # limbo
                cols.append('lime')
            else:
                cols.append('blue')  # Healthy
        return cols

