from person import *
import csv
import matplotlib.pyplot as plt

# Constants for drawing
WINDOW_WIDTH = 1300
WINDOW_HEIGHT = 500
BAR_HEIGHT = 80
BAR_Y_COORD = 300
LEGEND_SIZE = 30
LEGEND_OFFSET = 270
LEGEND_TEXT_OFFSET = 230

#Setting up the population
#get user input on the different sizes of the initial populations i.e the population size, the immune people and the infected people
original_population_size = int(input("What is the size of the original population? "))
immune_count = int(input("What is the size of the immune population? "))  # This should start coming from user input.
infected_count = int(input("What is the size of the infected population? "))  # This should start coming from user input.
deceased_count = 0  # At the start of the simulation, there is no deceased person

#compute the initial susceptible population from the data provided
susceptible_count = original_population_size - immune_count - infected_count - deceased_count

#create a temporary variable to hold the count initial infected population
org_infected = infected_count

CONTACT_NUMBER = int(input("What is the number of people a person can meet in a day "))  # Constant for how many people each Person meets a day.

# Keep track of how many days it's been
day_count = 0
target_duration = int(input("How long would like to run this simulation.(Enter time in days) "))  # This is how long we want to run the simulation

# create a person object of the person class and initialize it with values from the user's input
person = Person(susceptible_count, infected_count, immune_count, deceased_count, CONTACT_NUMBER)

#create a list of the person objects
population = [person.is_susceptible, person.contact_with_infected, person.is_infected, person.is_immune, person.is_dead]

#function to draw the different populations on the graphics window
def draw_status():
    clear()
    set_font_size(24)
    draw_text("Total population is: " + str(immune_count + infected_count + susceptible_count), 10, 30)

    draw_text("Simulation has been running for " + str(day_count) + " days", 10, 75)

    # Figure out how large we should make each population
    susceptible_width = (susceptible_count / original_population_size) * WINDOW_WIDTH
    infected_width = (infected_count / original_population_size) * WINDOW_WIDTH
    immune_width = (immune_count / original_population_size) * WINDOW_WIDTH
    dead_width = (deceased_count / original_population_size) * WINDOW_WIDTH

    # Start with susceptible
    set_fill_color(0, 1, 0)
    # Draw the bar
    if susceptible_count != 0:
        draw_rectangle(0, BAR_Y_COORD, susceptible_width, BAR_HEIGHT)
    # Draw the legend:
    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 30, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Susceptible '  + str(susceptible_count), WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 60)

    # Draw infected
    set_fill_color(1, 0, 0)
    if infected_count != 0:
        draw_rectangle(susceptible_width, BAR_Y_COORD, infected_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 75, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Infected ' + str(infected_count), WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 105)

    # Draw immune
    set_fill_color(0, 0, 1)
    if immune_count != 0:
        draw_rectangle(susceptible_width + infected_width, BAR_Y_COORD, immune_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 120, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Immune ' + str(immune_count), WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 150)

    # Draw diseased
    set_fill_color(0.2, 0.7, 0.7)
    if deceased_count != 0:
        draw_rectangle(susceptible_width + infected_width + immune_width, BAR_Y_COORD, dead_width, BAR_HEIGHT)

    draw_rectangle(WINDOW_WIDTH - LEGEND_OFFSET, 165, LEGEND_SIZE, LEGEND_SIZE)
    draw_text('Dead '  + str(deceased_count), WINDOW_WIDTH - LEGEND_TEXT_OFFSET, 195)

#function to check each infected person in the population whether they recovered or died on a particular day
def check_the_infected():
    global immune_count, deceased_count, infected_count

    for i in range(infected_count):
        person.state = 2

        if person.is_immune() is True:
            immune_count += 1           #increase the count of the immune population by one if the person recovered
            infected_count -= 1         #decrease the count of the infected population by one
        else:
            if person.is_dead() is True:
                deceased_count += 1     #increase the count of the immune population by one if the person died
                infected_count -= 1     #decrease the count of the infected population by one

#function to check each susceptible person in the population and check who they met and whether they contracted the disease
def check_the_susceptible():
    global infected_count, susceptible_count

    for i in range(susceptible_count):
        person.state = 1

        #check who they met and return how many of them were infected
        person.contact_with_infected()

        if person.is_infected() is True:
            infected_count += 1         #increase the count of the infected population by one if the person contracted the disease
            susceptible_count -= 1      #decrease the count of the susceptible population by one

#fuction to write each count of the different populations in a day to a csv file
def write_csv():
    #create a list with the different populations and the day they were recorded
    row = [day_count + 1, original_population_size, susceptible_count, infected_count, immune_count, deceased_count]

    #open the file in append mode
    with open('simulation_data.csv', 'a', newline = '') as csv_file:
        write_file = csv.writer(csv_file, delimiter = ',', quotechar = '|', quoting = csv.QUOTE_MINIMAL)
        write_file.writerow(row)

    csv_file.close()        #close the file after writing

#function to report the outcome of the simulation
def generate_final_report():

    R0 = (infected_count + deceased_count - org_infected) / org_infected
    survival_rate = ((susceptible_count + immune_count + infected_count) / original_population_size) * 100      #compute the survival rate
    print(str(survival_rate)+ "% of the original population survived the outbreak")
    print("On average, the initial infected population infected "+ str(R0) +" people")

    if R0 > 1:
        print("WE HAVE AN EPIDEMIC")
    else:
        print("We do NOT have an epidemic..just an outbreak. ")

#function to draw a graph to a file to give a better visualization of the populations as time progressed. Values used are those written to the csv file
def draw_report():
    x_time = []         #stores the x-axis values i.e Time
    y_susc = []         #stores the y-axis values of the susceptible count
    y_inf = []          #stores the y-axis values of the infected count
    y_rem = []          #stores the y-axis values of the removed count. Based on the SIR model, the Removed group is the summation of the immune and the dead population

    #open the file in read mode
    with open('simulation_data.csv', 'r') as csv_file:
        plots = csv.reader(csv_file, delimiter=',')

        #append to the list the values from each of the rows in the csv file
        for row in plots:
            x_time.append(int(row[0]))
            y_susc.append(int(row[2]))
            y_inf.append(int(row[3]))
            y_rem.append(int(row[4]) + int(row[5]))

    plt.title('SIR graph model for ' + disease)          #give the graph a title
    plt.plot(x_time, y_susc,'r' ,label = 'Susceptible')        #plot a line graph of the susceptible population over time
    plt.plot(x_time, y_inf,'b', label = 'Infected')         #plot a line graph of the infected population over time
    plt.plot(x_time, y_rem,'g', label = 'Removed')         #plot a line graph of the removed population over time
    plt.xlabel('Time')
    plt.ylabel('Count of Population')
    plt.legend()
    plt.savefig('report_graph1')

def main():
    global day_count
    # Draws the visual representation
    draw_status()

    # Loop over the infected population to determine if they could recover or pass away
    check_the_infected()

    # Loop over the healthy population to determine if they can catch the disease
    check_the_susceptible()

    # Update our output CSV
    write_csv()

    #increase the day by one
    day_count += 1

    #End the simulation once we reach the set target.
    if day_count == target_duration:
        generate_final_report()
        draw_report()
        cs1_quit()      #quit the graphics window

start_graphics(main, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, framerate=1)
