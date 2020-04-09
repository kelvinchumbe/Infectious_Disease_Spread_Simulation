from aluLib import *

#get input from the user on the attributes of the disease i.e its name, infection rate, recovery rate and lethality rate
disease = input("Whats the name of the disease? ")
infection_rate = float(input("What is its infection rate? "))
recovery_rate = float(input("What is its recovery rate? "))
lethality_rate = float(input('What is its lethality rate? '))

#create a disease class to represent the key attributes of the disease
class Disease:
    def __init__(self):
        self.disease = disease
        self.infection_rate = infection_rate
        self.recovery_rate = recovery_rate
        self.lethality_rate = lethality_rate