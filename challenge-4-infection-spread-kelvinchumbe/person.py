import random
from disease import *

#create a person class to represent a person's behaviour through the different stages of the model
class Person:
    def __init__(self, susceptible_count, infected_count, immune_count, deceased_count, CONTACT_NUMBER):

        self.susceptible = susceptible_count
        self.infected = infected_count
        self.immune = immune_count
        self.dead = deceased_count
        self.contact_no = CONTACT_NUMBER
        self.disease = Disease()                        #create an object of the disease class
        self.state = 0                      #state variable that identifies which category a person belongs to. 1 if susceptible, 2 if infected, 3 if immune and 4 if deceased
        self.people_met = []            #list with people a susceptible person meets in a day

#function to check whether a person is susceptible. Returns True if a person is susceptible otherwise False
    def is_susceptible(self):
        if self.infected > 0:           #if a few infected people are introduced in the population, then that makes one susceptible to contracting the disease
            self.state = 1              #change state to 1 to indicate susceptibility
            return True
        else:
            return False

#fucntion to check who a susceptible person met on a specific day and whether the person(s) was infected.
    def contact_with_infected(self):
        contact_list = []                 #a list of all the alive people in the population that a person could possibly meet. The person has an equal probability of meeting any of them
        met_infected_count = 0             #count of the infected people a person meets in a day

        #if a person is susceptible i.e state 1, then we create a list of all the alive people in the population i.e susceptibles, infected and immune
        if self.state == 1:
            for u in range(self.infected):
                contact_list.append('In' + str(u+1))

            for a in range(self.susceptible):
                contact_list.append('Susc' + str(a+1))

            for o in range(self.immune):
                contact_list.append('Imm' + str(o+1))

            #shuffle the contact list to rearrange the order
            random.shuffle(contact_list)
            self.people_met = random.sample(contact_list, self.contact_no)      #pick a random sample of the population thats the size of the contact number a person meets in a day. This becomes the list of people a person meets in a day

            #go through the list and find those who were infected and count them
            for i in range(len(self.people_met)):
                if self.people_met[i].startswith('In'):
                    met_infected_count += 1

        return met_infected_count          #return the number of infected people the person meets

#fucntion to check whether the person got infected after meeting the infected people.  Returns True if the got infected otherwise False
    def is_infected(self):
        #check whether a person got infected by the infected people they met. The probability of infection is proportional to the number of infected met
        #We check if after contact with an infected person whether the disease was transmitted or not. If not, we check again with the other infected people.
        #The moment a person gets infected, then we stop checking and change their state to 2 indicating infection

        for i in range(self.contact_with_infected()):
            # Generate a random float number and compare it to the disease's infection rate. The probability is biased since there isn't a 50-50 chance
            #If the random number generated is less than the infection rate, then the person contracted the disease
            if random.random() < self.disease.infection_rate:
                self.state = 2
                break

        if self.state == 2:
            return True
        else:
            return False

#function to check whether an infected person recovers from a disease and acquires immunity. Returns True if one recovers otherwise False
    def is_immune(self):
        if self.state == 2:
            # Generate a random float number and compare it to the disease's recovery rate. The probability is biased since there isn't a 50-50 chance
            # If the random number generated is less than the recovery rate, then the person recovered from the disease
            if random.random() < self.disease.recovery_rate:
                self.state = 3
                return True
            else:
                return False

#function to check whether an infected  person dies from the infection. Returns True is one dies otherwise false
    def is_dead(self):
        if self.state == 2:
            # Generate a random float number and compare it to the disease's lethality rate. The probability is biased since there isn't a 50-50 chance
            # If the random number generated is less than the lethality rate, then the person died from the disease
            if random.random() < self.disease.lethality_rate:
                self.state = 4
                return True
            else:
                return False
