# Covid-19 Modeling

> This is a refactor of https://towardsdatascience.com/building-your-own-covid-19-epidemic-simple-model-using-python-e39788fbda55

> Please refer to the original post for more information.

> I am not the original author.

> The refactor did not alter or change the order of operation stated in the original script.


<img src="https://github.com/Logic-gate/Covid19-Modeling/blob/master/Results/1000M10P/14_05_2020_19_57/png_to_gif.gif" width="500" height="500" />


![Stat](https://github.com/Logic-gate/Covid19-Modeling/blob/master/Results/1000M10P/14_05_2020_19_57/Stat.png)



# Getting Started
Make sure to have a look at `config.ini`, it houses the parameters that will define the model. An important aspect to consider when starting is the `Group Size` and the `Sample Size`, they will dictate the resources and time needed for the simulation. I couldn't equate the exact time needed; there are many factors to consider. Processing power and memory are but a few. The default configuration took my i7-6700HQ CPU @ 2.60GHz 10 minutes to complete, however after testing with a `Group Size=3000 & Sample Size=0.1` it took 40 mins to reach day 17. 
 
 Not all parameters in `config.ini` are considered. This is a work in progress.

``` 
[SampleDefaults]
xLimit = 30
yLimit = 30
dayLimit = 100
groupSize = 3000
sampleSize = 0.1
distance = 1.5
numberOfBeds = 3 #Not Used
logfile = corona.log

[Rates]
#https://www.worldometers.info/coronavirus/coronavirus-death-rate/
deathRate = 0.034
deathsDueToLackOfBeds = 0.05 # Not Used
#https://www.cdc.gov/coronavirus/2019-ncov/covid-data/covidview/index.html
hospitalizationRate = 0.5
#https://www.worldometers.info/coronavirus/coronavirus-death-rate/
deathRateForICU = 0.15

[Days]
daysUntilLimboDieDuetoLackOfBeds = 3 # Not Used
dayUnitlCuredIfPositive = 14
dayUnitlCuredIfInHospital = 25
```

Limbo is also not taken into account. The state was supposed to represent those who are extremely sick yet cannot be hospitalized due to lack of beds...this is also a work in progress

I would suggest removing the ion func for Group Sizes > 1500

Since the model is dictated by ratios and counts, altering the parameters without considering it's soundness will result in unlikely outcomes. Be mindful when specifying your parameters.
