import random as rn
import math
from states import States


class Process:

    def __init__(self, generateFunc, Yesterday):
        self.df = generateFunc[0]
        self.stateOfDay = generateFunc[1]
        self.MoversList = generateFunc[2]
        self.YesterdayPatients = Yesterday
        s = States()
        self.deathRate = s.returnConfig("Rates", "deathRate", float)
        self.daysFromLimbo = s.returnConfig(
            "Days", "daysUntilLimboDieDuetoLackOfBeds", int)
        self.numberOfBeds = s.returnConfig(
            "SampleDefaults", "numberOfBeds", int)
        self.deathsLackBed = s.returnConfig(
            "Rates", "deathsDueToLackOfBeds", float)
        self.hospitalRate = s.returnConfig(
            "Rates", "hospitalizationRate", float)
        self.hospitalRateICU = s.returnConfig(
            "Rates", "deathRateForICU", float)
        self.dayUntilCuredCovid = s.returnConfig(
            "Days", "dayUnitlCuredIfPositive", int)
        self.daysUnitlCuredHos = s.returnConfig(
            "Days", "dayUnitlCuredIfInHospital", int)

        self.xlimit = s.returnConfig("SampleDefaults", "xlimit", int)
        self.ylimit = s.returnConfig("SampleDefaults", "ylimit", int)
        self.distanceLimit = s.returnConfig("SampleDefaults", "distance", float)


    def kill(self, day):
        samplesize = math.floor(len(
            self.df[self.df['State'] == 1]) * self.deathRate + len(self.df[self.df['State'] == 2]) * self.hospitalRateICU)
        if samplesize > len(self.df[self.df['State'] == 1]):
            return
        self.df.loc[self.df[self.df['State'] ==
                            1].sample(n=int(samplesize)).index.values.tolist(), 'State'] = 3
        self.df.loc[(self.df['Day'] < day - self.daysFromLimbo)
                    & (self.df['State'] == 5), 'State'] = 3
        return



    def hospitilize(self, day):
        samplesize = math.floor(
            len(self.df[self.df['State'] == 1]) * self.hospitalRate)
        if samplesize > len(self.df[self.df['State'] == 1]):
            return
        self.df.loc[self.df[self.df['State'] ==
                            1].sample(n=int(samplesize)).index.values.tolist(), 'State'] = 2
      
        return


    def cure(self, day):
        self.df.loc[(self.df['Day'] < day - self.dayUntilCuredCovid) & (self.df['State'] == 1), 'State'] = 6
        self.df.loc[(self.df['Day'] < day - self.daysUnitlCuredHos) & (self.df['State'] == 2), 'State'] = 4
        return



