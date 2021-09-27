from scipy.stats import norm
import random
import time
import pandas as pd
import numpy as np
PeopleDict = []
class Person():
    def __init__(self, Starting_Immunity):
        if random.randint(0,100) < Starting_Immunity:
            self.Immunity = True
        else:
            self.Immunity = False
        self.Infected = 0
        self.Life = 1
        self.Days_Contagious = 0
        self.Friends = int((norm.rvs(size = 1, loc=0.5, scale = 0.15)[0]*10).round(0))
        self.Age = int((norm.rvs(size = 1, loc = 0.5, scale = 0.15)[0]*100).round(0))
        #### A few more items need to be added under the person class
        self.Health = int((norm.rvs(size = 1, loc = 0.5, scale = 0.15)[0]*4).round(0))

def MCS():
    Population = int(input("Population of the Simulation: "))
    Starting_Immunity = int(input('Percentage of People with Natural Immunity: '))
    Ground_Zero = int(input('How many people will be infected day 0: '))
    Base_Lethality = int(input('How lethal is the infection: '))
    Base_Duration = int(input("How long will a person be infected: "))
    Length_Pandemic = int(input("How many days will be simulated: "))
    LockDownDay = int(input("What day does Lockdown start: "))
    for x in range(0,Population):
        PeopleDict.append(Person(Starting_Immunity))
    for x in range(0, Ground_Zero):
        PeopleDict[random.randint(0, len(PeopleDict)-1)].Infected = int((norm.rvs(size=1,loc=0.5,scale=0.15)[0]*10).round(0)*10)
    return Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Duration, LockDownDay

def DayPassage(Base_Duration, LockDown):
    for Person in [Person for Person in PeopleDict if Person.Infected =1 and Person.Friends > 0]:
        PeopleCouldMeet = int(Person.Friends)
        if PeopleCouldMeet > 0:
            PeopleMetToday = random.randint(0, PeopleCouldMeet)
        else:
            PeopleMetToday = 0
        if LockDown == True:
            PeopleMetToday = 0

        for x in range(0,PeopleMetToday):
            Peeps = PeopleDict[random.randint(0, len(PeopleDict)-1)]
            if random.randint(0,100) < Base_Infection and Peeps.Infected == 0 and Peeps.Immunity == False:
                Peeps.infected = 1



    for Person in [Person for Person in PeopleDict if Person.Infected = 1]:
        Person.Days_Contagious +=1
        if Person.Days_Contagious >= Base_Duration:
            Person.Immunity = True
            Person.Infected = 0
        Angel = random.randint(0,100)
        if Angel < Starting_Lethality * Person.Health:
            Person.Infected = 0
            Person.Life = 0

LockDown = False
Base_Duration, LockDownDay = initiateSim()
saveFile = open("pandemicsave3.txt", "a")
for x in range(0,Length_Pandemic):
    if x==LockDownDay:
        LockDown = True

    print("Day ", x)
    DayPassage(Base_Duration, LockDown)
    write = str(len([Person for Person in PeopleDict if Person.Infected>0])) + "\n"
    saveFile.write(write)
    print(len([Person for Person in PeopleDict if Person.Infected>0]), " people are contagious on this day.")
    print(len([Person for Person in PeopleDict if Person.Life=0]), " people have died since the beginning.")
    print(len([Person for Person in PeopleDict if Person.Immunity=1]), " people have gained immunity.")
    #### Create Dataframes, code that displays information within the dataframes
saveFile.close()
