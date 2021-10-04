import pandas as pd
import numpy as np
from scipy.stats import norm
import random
import time
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt

People_Dict = [] # Holds all randomly generated people
# This Generates the People in the simulation
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
    def as_dict(self): # Used to create dataframe of initial values
        return{'Immunity':self.Immunity, 'Infected':self.Infected, 'Life':self.Life,
        'Days_Contagious':self.Days_Contagious ,
        'Friends':self.Friends, 'Age':self.Age, 'Health':self.Health
        }

def Starting_Menu():
    Population = int(input("Population of the Simulation: "))
    Starting_Immunity = int(input('Percentage of People with Natural Immunity: '))
    Ground_Zero = int(input('How many people will be infected day 0: '))
    Base_Lethality = int(input('How lethal is the infection: '))
    Base_Infection = int(input("Base Infection Rate: "))
    Base_Duration = int(input("How long will a person be infected: "))
    Length_Pandemic = int(input("How many days will be simulated: "))
    LockDownDay = int(input("What day does Lockdown start: "))
    Vaccination_Rate = int(input("What Percentage of the Population will take the vaccine: ")) # I can't fucking spell
    Vaccination_Day = int(input("What Day will Vaccines be Avaiable: "))
    Number_Sims = int(input("How many simulations will be conducted: "))
    Run_Notation = int(input("ID of simulation run: "))
    # for x in range(0,Population):
    #     People_Dict.append(Person(Starting_Immunity))
    # for x in range(0, Ground_Zero):
    #     People_Dict[random.randint(0, len(People_Dict)-1)].Infected = int((norm.rvs(size=1,loc=0.5,scale=0.15)[0]*10).round(0)*10)
    return Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic, LockDownDay, Vaccination_Rate, Vaccination_Day ,Number_Sims, Run_Notation

def TimeLine(Base_Lethality, Base_Duration, Base_Infection):
    for Person in [Person for Person in People_Dict if Person.Immunity == True]:
        pass
    for Person in [Person for Person in People_Dict if Person.Infected == 0 and Person.Immunity == False]:
        Chance_to_Infect = random.randint(0,100)
        if Chance_to_Infect < Base_Infection:
            Person.Infected = 1
        pass
    for Person in [Person for Person in People_Dict if Person.Infected == 1]:
        Angel = random.randint(0,100)
        Die_Roll = random.randint(0,100)
        if Angel <= Base_Lethality:
            Person.Infected = 0
            Person.Life = 0
        if Person.Days_Contagious >= Base_Duration:
            if Die_Roll < 75:
                Person.Infected = 0
                Person.Immunity = True
            else:
                Person.Days_Contagious +=1
        else:
            Person.Days_Contagious += 1
        pass
    for Person in [Person for Person in People_Dict if Person.Life == 0]:
        pass

# for x in range(0, Length_Pandemic):
#     Time_Passage()

Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic, LockDownDay, Vaccination_Rate, Vaccination_Day ,Number_Sims, Run_Notation = Starting_Menu()
for x in range(0,Population):
    People_Dict.append(Person(Starting_Immunity))

Killed_List = []
Immune_List = []
Day_List = []
for x in range(0,Length_Pandemic):
    TimeLine(Base_Lethality, Base_Duration, Base_Infection)
    print("Amount of People Killed", len([Person for Person in People_Dict if Person.Life == 0]))
    print("Amount of People Immune: ", len([Person for Person in People_Dict if Person.Infected == 1]))
    Killed_List.append(len([Person for Person in People_Dict if Person.Life == 0]))
    Immune_List.append(len([Person for Person in People_Dict if Person.Infected == 1]))
    Day_List.append(x)


starting_pop = pd.DataFrame([x.as_dict() for x in People_Dict])
starting_paramters = pd.DataFrame([[Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic,
                                    LockDownDay, Vaccination_Rate, Vaccination_Day, Number_Sims, Run_Notation]],
                                    columns = ['Population', 'Starting Immunity', 'Ground Zero', 'Base Lethality', 'Base Infection' ,'Base Duration',
                                               'Length Pandemic', 'Lock Down Day', 'Vaccination Rate', 'Vaccination Day', 'Number of Simulations',
                                               'Run ID'])
with pd.ExcelWriter("C:/Users/schne/Desktop/TestTestTest.xlsx") as writer:
    starting_paramters.to_excel(writer, sheet_name = 'Starting Paramater')
    starting_pop.to_excel(writer, sheet_name = 'Starting Population')

# Graphing = pd.DataFrame([[Killed_List, Immune_List, Day_List]], columns = ['Killed', 'Immune', 'Day_'])
Graphing=pd.DataFrame.from_dict({'Killed' : Killed_List, 'Immune' : Immune_List, 'Day' : Day_List}, orient='index').T
print(Graphing)
sns.lineplot(x = "Day", y = "Killed", data = Graphing)
sns.lineplot(x = "Day", y = "Immune", data = Graphing)
plt.show()
# writer = pd.ExcelWriter(f'Simulation_Outputs_for_{Number_Sims}_simulations_{Run_Notation}')
