#!/usr/bin/python3

import numpy as np
import math
import pandas as pd
import random as rn
from states import States



class SampleGeneration:

	def __init__(self):
		
		s = States()
		self.groupSize = s.returnConfig("SampleDefaults", "groupSize", int)
		self.state = s.status
		self.colors = s.stateColors
		self.sampleSize = s.returnConfig("SampleDefaults", "sampleSize", float)
		self.x = s.returnConfig("SampleDefaults", "xLimit", int)
		self.y = s.returnConfig("SampleDefaults", "yLimit", int)

	def pointFunction(self):
		pointX = np.random.uniform(0, self.x)
		pointY = np.random.uniform(0, self.y)
		return pointX, pointY

	def generate(self):
		df = pd.DataFrame(columns='X,Y,State,Day'.split(','))
		for i in range(self.groupSize):
			df.loc[i, 'X'], df.loc[i, 'Y'] = self.pointFunction()
			df.loc[i, 'State'] = 0
		sampleSize = math.floor(self.groupSize * self.sampleSize)
		MoversList = df.sample(n=sampleSize).index.values.tolist()

		StatofDay = pd.DataFrame(columns='Healthy,Covid-19(+),Hospitalized,Cured,Self Cured,Dead,Limbo,Total Cured'.split(','))
		return df, StatofDay, MoversList

