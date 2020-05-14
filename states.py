from configparser import ConfigParser as SafeConfigParser

class States:

	def __init__(self):
		self.Config = SafeConfigParser()
		self.Config.read('config.ini')

	def status(self, i):
		state = {
				"Healthy":0,
				"Covid-19": 1,
				"Hospitalized": 2,
				"Dead": 3,
				"Cured" :4, 
				"Limbo": 5,
				"Self Cured": 6, 
				"Total Cured": 100
			}
		return state[i]

	def stateColors(self, j):
		colors = {
					0 : "blue",
					1 : "red",
					2 : "orange",
					3 : "black",
					4 : "green",
					5 : "yellow",
					6 : "cyan", 
					100: "lime"
		}
		return colors[j]

	def returnConfig(self, section, option, type):
		if type is float:
			return float(self.Config.get(section, option))
		elif type is int:
			return int(self.Config.get(section, option))
		elif type is str:
			return str(self.Config.get(section, option))