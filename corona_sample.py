import data
import process
import random
from sim import Draw
import matplotlib.pyplot as plt
from states import States
import random as rn
import math
from PIL import Image
import glob
import os
from datetime import datetime
import sys


"""
This is a refactor of a script by Sadegh Maghsoudi
Original script: https://towardsdatascience.com/building-your-own-covid-19-epidemic-simple-model-using-python-e39788fbda55

"""


class SampleModel:
	def __init__(self, day, generateFunc, processFunc, plotFunc, path):
		self.day = day
		self.path = path
		self.s = States()
		self.dayLimit = self.s.returnConfig('SampleDefaults', 'dayLimit', int)
		self.x = self.s.returnConfig('SampleDefaults', 'xLimit', int)
		self.y = self.s.returnConfig('SampleDefaults', 'yLimit', int)
		self.groupsize = self.s.returnConfig('SampleDefaults', 'groupSize', int)
		self.sampleSize = self.s.returnConfig('SampleDefaults', 'sampleSize', float)
		self.distance = self.s.returnConfig('SampleDefaults', 'distance', float)
		self.beds = self.s.returnConfig('SampleDefaults', 'numberOfBeds', float)
		logfile = f"{self.path}/{self.s.returnConfig('SampleDefaults', 'logfile', str)}"
		self.logFile = open(logfile, "w+")
		self.distanceLimit = self.s.returnConfig("SampleDefaults", "distance", float)
		self.generateData = generateFunc
		self.stateOfDay = self.generateData[1]
		self.MoversList = self.generateData[2]
		self.YesterdayPatients = list(self.generateData[0]['State'])
		self.startProcess = processFunc
		self.plotData = plotFunc

	def write_log(self, *args):
		line = ' '.join([str(a) for a in args])
		self.logFile.write(line + '\n')
		print(line)
		return
	
	def infect(self, i):
		if rn.random() > 0.25 and self.day > 3:
			return
		if self.generateData[0].loc[i, "State"] == 0:
			self.generateData[0].loc[i, "State"], self.generateData[0].loc[i, "Day"] = 1, self.day


	def nextDay(self):
		process = self.startProcess
		self.day += 1
		process.kill(self.day)
		process.hospitilize(self.day)
		process.cure(self.day)
		self.move()
		self.interact()
		return

	def plot(self):
		self.plotData.setup_plot(self.day)
		return

	def count(self):
		List = list(self.generateData[0]['State'])

		self.stateOfDay.loc[self.day, 'Healthy'] = List.count(0)
		self.stateOfDay.loc[self.day, 'Covid-19(+)'] = List.count(1)
		self.stateOfDay.loc[self.day, 'Hospitalized'] = List.count(2)
		self.stateOfDay.loc[self.day, 'Cured'] = List.count(4)
		self.stateOfDay.loc[self.day, 'Dead'] = List.count(3)
		self.stateOfDay.loc[self.day, 'Limbo'] = List.count(5)
		self.stateOfDay.loc[self.day, 'Self Cured'] = List.count(6)
		self.stateOfDay.loc[self.day, 'Total Cured'] = List.count(6) + List.count(4)

		return

	def run(self):
		self.infect(rn.randrange(self.groupsize))
		self.plot()
		self.count()
		self.log(2)
		self.nextDay()
		self.plot()
		self.count()
		self.log(2)
		return

	def interact(self):
		for i in range(len(self.generateData[0])):
			for j in range(i):
				if self.check(i, j):
					if (self.generateData[0].loc[i, 'State'] == 0):
						self.infect(i)
					else:
						self.infect(j)

	def check(self, i, j):
		Dist = math.sqrt((self.generateData[0].loc[i, 'X'] - self.generateData[0].loc[j, 'X'])
                         ** 2 + (self.generateData[0].loc[i, 'Y'] - self.generateData[0].loc[j, 'Y'])**2)
		flag = ((self.YesterdayPatients[i] == 1) ^
                (self.YesterdayPatients[j] == 1)) and Dist < self.distanceLimit
		return flag

	def move(self):
		for i in self.MoversList:
			if (self.generateData[0].loc[i, 'State'] == 2) or (self.generateData[0].loc[i, 'State'] == 3) or (self.generateData[0].loc[i, 'State'] == 5):
				self.MoversList.remove(i)
			self.generateData[0].loc[i, 'X'], self.generateData[0].loc[i, 'Y'] = (self.generateData[0].loc[i, 'X'] + rn.uniform(
		    1, self.x / 3)) % self.x , (self.generateData[0].loc[i, 'Y'] + rn.uniform(1, self.y / 3)) % self.y


	def log(self, phase):
		if phase == 1:
			self.write_log(31 * '-')
			self.write_log("Here's the Input Data:")
			self.write_log(8 * '- - ')
			self.write_log('Numper of Sample:', self.groupsize)
			self.write_log('X & Y limites: ', self.x, ', ', self.y)
			self.write_log('Distance required for Contamination:', self.distance)
			self.write_log("Moving Sample", self.sampleSize)
			self.write_log("Number Of Beds", self.beds)
			x = input("Do you wish to continue? y/n: ")
			if x == "y":
				pass
			elif x == 'n':
				sys.exit()	
		elif phase == 2:
			self.write_log(31 * '-')
			self.write_log('Day:', self.day)
			self.write_log(8 * '- - ')
			self.write_log(self.generateData[1].loc[self.day])
		return

	def end(self):
		self.Png_to_gif()

		self.stateOfDay.to_excel(f"{self.path}/Stat.xlsx")
		self.stateOfDay.plot(title='Statistical Data Vs. Days Passed')

		plt.savefig(f"{self.path}/Stat")
		self.logFile.close()

	def condition(self):
		healthy = len(self.generateData[0][self.generateData[0]['State'] == 0])
		covid19 = len(self.generateData[0][self.generateData[0]['State'] == 1])
		hospitilize = len(self.generateData[0][self.generateData[0]['State'] == 2])
		dead = len(self.generateData[0][self.generateData[0]['State'] == 3])
		cured = len(self.generateData[0][self.generateData[0]['State'] == 4])
		Limbo = len(self.generateData[0][self.generateData[0]['State'] == 5])
		selfcured = len(self.generateData[0][self.generateData[0]['State'] == 6])
		today = list(self.generateData[1].loc[self.day])
		yest = list(self.generateData[1].loc[self.day- 1])
		
		if covid19 == 0 and today == yest and hospitilize == 0:
			
			return 1
		else:
			return 0



	def main(self):
		
		whileBreak = 0
		while True:
			whileBreak += int(self.condition())
			
			if whileBreak > 2:
				self.end()
				break
				
			else:
				self.whileBreak = 0

			self.YesterdayPatients = list(self.generateData[0]['State'])
			self.nextDay()
			self.plot()
			self.count()
			self.log(2)
		

	def Png_to_gif(self):
		frames = []
		inImgs = f"{self.path}/days/*.png"
		output = f"{self.path}/png_to_gif.gif"

		img, *imgs = [Image.open(i) for i in sorted(glob.glob(inImgs))]
		img.save(fp=output, format='GIF', append_images=imgs,
         save_all=True, duration=500, loop=0)
			

if __name__ == '__main__':
	day = 0
	n = datetime.now()
	timeNdate = n.strftime("%d_%m_%Y_%H_%M")
	x = input("Model Name: ")
	path = f"{os.getcwd()}/Results/{x}/{timeNdate}"
	try:
		print(f"Creating Dirs...")
		os.makedirs(path)
		os.makedirs(f"{path}/days")
	except OSError:
		if os.path.isdir(path):
			print(f"Dir Already Exists")
		else:
			print(f" Could Note Create {path}")
	else:
		print(f"...OK")
	generateData = data.SampleGeneration()
	g = generateData.generate()
	YesterdayPatients = list(g[0]['State'])
	plotData = Draw(g, path)
	plotData.setup_plot(day)
	startProcess = process.Process(g, YesterdayPatients)
	sample = SampleModel(day, g, startProcess, plotData, path)
	sample.log(1)
	sample.run()
	sample.main()
