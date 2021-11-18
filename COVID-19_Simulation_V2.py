import pandas as pd
import numpy as np
from scipy.stats import norm
import random
import time
import openpyxl
import seaborn as sns
import matplotlib.pyplot as plt
import PySimpleGUI as sg

People_Dict = []  # Holds all randomly generated people
# This Generates the People in the simulation


class Person():
    def __init__(self, Starting_Immunity):
        if random.randint(0,100) < Starting_Immunity:
            self.Immunity = True
        else:
            self.Immunity = False
        self.Infected = 0
        self.Vaccinated = 0
        self.Life = 1
        self.Days_Contagious = 0
        self.Friends = int((norm.rvs(size = 1, loc=0.5, scale = 0.15)[0]*10).round(0))
        self.Age = int((norm.rvs(size = 1, loc = 0.5, scale = 0.15)[0]*100).round(0))
        #### A few more items need to be added under the person class
        self.Health = int((norm.rvs(size = 1, loc = 0.5, scale = 0.15)[0]*4).round(0))
        self.Job = int((norm.rvs(size = 1, loc = 0.5, scale = 0.15)[0]*5).round(0))
        self.Days = 0
    def as_dict(self): # Used to create dataframe of initial values
        return{'Immunity':self.Immunity, 'Infected':self.Infected, 'Vaccinated' :self.Vaccinated, 'Life':self.Life,
        'Days_Contagious':self.Days_Contagious ,
        'Friends':self.Friends, 'Age':self.Age, 'Health':self.Health, 'Days': self.Days
        }
def Starting_Menu():
    layout = [[sg.Text("Bjornen Project: ")],
    [sg.Text("Population of the Simulation: "),sg.Input(10000)],
    [sg.Text("Percentage of People with Natural Immunity: "), sg.Input(1)],
    [sg.Text("How many people will be infected day 1: "), sg.Input(100)],
    [sg.Text("How lethal is the infection: "), sg.Input(2)],
    [sg.Text("How Infectious is the disease: "), sg.Input(25)],
    [sg.Text("How many days will a Person be Infected: "), sg.Input(10)],
    [sg.Text("How many days will be simulated: "), sg.Input(25)],
    [sg.Text("What day does LockDown start: "), sg.Input(150)],
    [sg.Text("What Percentage of the Population will take the vaccine: "), sg.Input(52)],
    [sg.Text("What day will vaccines be available: "), sg.Input(150)],
    [sg.Text("How many simulations will be conducted: "), sg.Input(1)],
    [sg.Text("ID number of simulation run: "), sg.Input(1)],
    [sg.Submit(), sg.Cancel()]]
    window = sg.Window("Bjornen 1.0V", layout)
    button, Initial_Values = window.read()
    Population = int(Initial_Values[0])
    Starting_Immunity = int(Initial_Values[1])
    Ground_Zero = int(Initial_Values[2])
    Base_Lethality = int(Initial_Values[3])
    Base_Infection = int(Initial_Values[4])
    Base_Duration = int(Initial_Values[5])
    Length_Pandemic = int(Initial_Values[6])
    LockDownDay = int(Initial_Values[7])
    Vaccination_Rate = int(Initial_Values[8])
    Vaccination_Day = int(Initial_Values[9])
    Number_Sims = int(Initial_Values[10])
    Run_Notation = int(Initial_Values[11])
    window.close()
    return Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic, LockDownDay, Vaccination_Rate, Vaccination_Day ,Number_Sims, Run_Notation


def TimeLine(Base_Lethality, Base_Duration, Base_Infection):
    for Person in [Person for Person in People_Dict if Person.Infected == 0 and Person.Immunity == False]:
        Chance_to_Infect = random.randint(0,100)
        Person.Days += 1

        if Vaccination_Day <= x:
            if Chance_to_Infect < Base_Infection:
                Person.Infected = 1
        Get_Vaccine = random.randint(0,100)
        if Get_Vaccine <= Vaccination_Rate:
            Person.Immunity = True
        else:
            if Chance_to_Infect < Base_Infection:
                Person.Infected = 1
                pass
    for Person in [Person for Person in People_Dict if Person.Infected == 1 and Person.Days==x ]:
        Person.Days += 1
        Angel = random.randint(0,100)
        Die_Roll = random.randint(0,100)
        RR_Increase = random.randint(0,5)
        if Person.Days_Contagious  >= Base_Duration:
            if Angel <= Base_Lethality * Person.Health:
                Person.Infected = 0
                Person.Life = 0
        if Die_Roll < 75 - (Person.Health * 10):
            Person.Infected = 0
            Person.Immunity = True
        else:
            Person.Days_Contagious += 1
        if Person.Days_Contagious  < Base_Duration:
            Person.Days_Contagious += 1

    for Person in [Person for Person in People_Dict if Person.Life == 0 and Person.Days == x]:
        Person.Days += 1
        pass
    for Person in [Person for Person in People_Dict if Person.Immunity == True and Person.Days == x]:
        Person.Days += 1
        pass


# for x in range(0, Length_Pandemic):
#     Time_Passage()
# LockDownDay == False
Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic, LockDownDay, Vaccination_Rate, Vaccination_Day ,Number_Sims, Run_Notation = Starting_Menu()
for x in range(0, Number_Sims):
    for x in range(0,Population):
        People_Dict.append(Person(Starting_Immunity))
    for Person in (random.sample([Person for Person in People_Dict if Person.Immunity == False], Ground_Zero)):
        Person.Infected = 1
    ### These lists are used to print numbers throughtout the process
    Killed_List = []
    Infected_List = []
    Immune_List = []
    Day_List = []

    ###### Dataframe for more analysis

    Memory_Tunnel = pd.DataFrame(

    )
    for x in range(0,Length_Pandemic):
        TimeLine(Base_Lethality, Base_Duration, Base_Infection)
        print("Day: ", x)
        print("Amount of People Killed: ", len([Person for Person in People_Dict if Person.Life == 0]))
        print("Amount of People Infected: ", len([Person for Person in People_Dict if Person.Infected == 1]))
        print("Amount of People Immune: ", len([Person for Person in People_Dict if Person.Immunity == True]))
        Killed_List.append(len([Person for Person in People_Dict if Person.Life == 0]))
        Infected_List.append(len([Person for Person in People_Dict if Person.Infected == 1]))
        Immune_List.append(len([Person for Person in People_Dict if Person.Immunity == True]))
        Day_List.append(x)
    # Memory_Tunnel.append(pd.DataFrame([x.as_dict() for x in People_Dict]))
    # for Person in [Person for Person in People_Dict if Person.Life == 1]:
    #     temp = pd.DataFrame([Person], columns = ['Health'])
    #     Memory_Tunnel = Memory_Tunnel.append(temp, ignore_index=True)
        temp = pd.DataFrame([x.as_dict() for x in People_Dict])
        Memory_Tunnel = Memory_Tunnel.append(temp, ignore_index = True)

starting_pop = pd.DataFrame([x.as_dict() for x in People_Dict])
starting_paramters = pd.DataFrame([[Population, Starting_Immunity, Ground_Zero, Base_Lethality, Base_Infection ,Base_Duration, Length_Pandemic,
    LockDownDay, Vaccination_Rate, Vaccination_Day, Number_Sims, Run_Notation]],
    columns=['Population', 'Starting Immunity', 'Ground Zero', 'Base Lethality', 'Base Infection', 'Base Duration',
    'Length Pandemic', 'Lock Down Day', 'Vaccination Rate', 'Vaccination Day', 'Number of Simulations', 'Run ID'])

# Analysis_df=Memory_Tunnel.groupby(['Day', 'Life']).count()
# print(Analysis_df.head())
with pd.ExcelWriter("C:/Users/schne/Desktop/TestTestTest.xlsx") as writer:
    starting_paramters.to_excel(writer, sheet_name='Starting Paramater')
    starting_pop.to_excel(writer, sheet_name='Starting Population')
    Memory_Tunnel.to_excel(writer, sheet_name='All Data')

Graphing = pd.DataFrame.from_dict({'Killed': Killed_List, 'Infected': Infected_List, 'Immune': Immune_List, 'Day': Day_List}, orient='index').T
print(Graphing)
sns.lineplot(x="Day", y="Killed", data=Graphing)
plt.show()
sns.lineplot(x="Day", y='Immune', data=Graphing)
plt.show()
sns.lineplot(x="Day", y="Infected", data=Graphing)
plt.show()
