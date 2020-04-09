Challenge 4: Epidemic modeling
==============================
For our final project of the term, we will build a program that can simulate _infectious and contagious diseases_, and 
how they spread through a population.

In particular, once the simulation is done, it will be up to your program to determine if it was indeed an epidemic or not.

How? The formal definition of an epidemic is when *on average, each infected person infected 1 or more other people*

This will be heavily reliant on OOP concepts, so spend time on practicing and revisit key concepts before diving too 
deeply into this assignment. The requirements are also quite diverse, so take it slow, step by step. Below we list the
requirements, as well as the various steps you can go through to build up the simulation.

Key requirements:
------------------
- Run a simulation which decides the following every cycle:
  - For each sick person: 
    - Did the person recover?
    - Did the person pass away?
  - For each healthy person:
    - How many people did they see today?
        - Were any of those people sick?
            - Does that mean the healthy person is now sick?
- You should have variables that keep track of the following over the course of the simulation:
    - The total population: This is the sum of the following 3 variables
    - The susceptible population: How many people could get sick?
    - The immune population: How many people can no longer get sick?
    - The infected population: How many people are sick?
    - The deceased population: This is separate from the total population, and tracks how many people have passed away.
- All the population variables above should be written to a CSV file called _simulation_report_. If the simulation ran 
for 100 days, you should have 100 lines in the csv file, plus 1 line at the beginning with the name of each column.
- When the program stops, it should report the following by printing it:
    - What percentage of the initial population survived?
    - Were we dealing with an epidemic or not?

Randomness:
------------
Bear in mind what we covered in class on Monday. For randomness, you can use a few different approaches.
In particular two methods from the random library are useful for us:
```randint(a, b)``` will return a random integer between a and b, inclusive.

```random()``` will return a random float between 0.0 and 1.0

If you want to check if something happened with a 50% chance, simply call random(), and check if the number generated was
above or below 0.5

Recall as well that you need to have ```from random import *``` in any file you plan to use these functions.

The disease class:
-------------------
The disease class is in fact quite simple, it will not have any methods, and simply track variables about the disease
you simulate, in particular you should have:
- infection_rate: What is the % chance that the disease transmits if two people are in contact.
- recovery_rate: What is the % chance that someone recovers each day.
- lethality_rate: What is the % chance that someone dies on a given day.

That's basically all you would need unless you tackle some of the extra credit.

The person class:
-----------------
**Step 1 - Categories:**

This is where a lot of the magic will occur, and where you will have a lot of freedom to determine your own approach.
Fundamentally, you need to know which category of population each person belongs to. The categories again are:
- Susceptible: The person is alive, not sick, but not immune to the disease.
- Immune: The person is alive, not sick , and can not catch the disease.
- Infected: The person is alive, and sick.
- Dead: The person is not alive.

Through a combination of methods and attributes, you should be able to create Person objects of each category.

**Step 2 - Interaction with the disease:**

Each person should know what they are sick of, and be able to interact with the sickness.
Create a method for each of the next scenarios:
- Determine if an infected person recovers.
- Determine if an infected person dies.
- Determine if a healthy person becomes sick given another person as a parameter.

The simulation
--------------

**Step 1 - Dealing with the population.**

Note that you are provided with some starter code for the simulation. You can, and will have to, add extra features to it
and define the classes above properly to be able to simulate the disease.

Note that your population is a **List of Person objects**.
You should implement the following functions:
- First a function that checks all sick people in the population, checks if they survive or recover, and update our global
counts accordingly.
- Secondly a function that checks all healthy people, then pick ```daily_encounter``` random other people from the population for them to meet.
If any of those randomly chosen individuals is sick, check if an infection happens.

*Step 2 - Reporting*
Before your simulation begin, create a new csv file in your code, and write this following line:
```buildoutcfg
Total population, Susceptible, Infected, Immune, Dead
```

Every step through the simulation, write a new line to the file with the required info. Don't forget to close at the end!

*Step 3 - Computing R0 and survival rate*
By default, your simulation should run for 100 cycles. This is already set up in the provided code, where cs1_quit() is 
called after 100 frames are drawn.

You should compute the R0 value on cycle number 20. This means that when the global _day_ variable reaches 20, and only then,
you should do the following:
- Add up all currently infected and deceased people, and substract the original number of infected.
- Divide the number you obtained by the original number of infected. 
- This should give you some positive number, which will tell us roughly how many people on average the initial infected 
population infected. You should have at least 5 infected people at the beginning to make this work.

Each cycle, write a new line with all the information suggested by the header. The idea is that you can easily upload such
a file to a spreadsheet and get a nice graph of the evolution of each category over time.

Grading
-------

Correctness:

-   Each strategy is implemented correctly
-   The program asks for user input and stores the information appropriately
-   The program creates and saves new files

Coding proficiency:

- You correctly use functions to organize the code's logic
- Drawing is done as per the standards of aluLib.
- Any logic in the code is handled clearly and elegantly. If statements are used appropriately.

Style:

-   Clear design and organization.
-   Good variable names, function names, and comments.
-   Functions where appropriate and not where inappropriate.
-   In this case in particular, be very clear about the assumptions you are making.

## Honor Code

Please make sure that you fully understand the Academic Honor System, and reach out if you need any clarifications. 


What to turn in
---------------

Make sure your git repository contains the following:
- At least 3 python files: One for the Disease class, one for the Person class, and one for the simulation
- Optionally: a second python file for the extra credit version of the simulation
- A text file describing the following:
    - An acknowledgement of upholding the honor code, or information if any breach occurred.
    - Any extra credits or additional features you attempted.
    - Any notes you want to bring to the attention of the grader. 


Extra Credit
------------

You can add all sorts of features to the submission for extra
credit. Make sure, however, before you charge off and do extra credit
that you have the basic game working correctly, that you've designed it
as cleanly as possible, and that you've documented it well. Remember, the extra credit points don't really count for anything.

There are plenty of ideas for extra credit, you can find some suggestions here:
- *Latency periods*: Each Disease object should know how much time it takes before it becomes contagious, and how much time it 
takes before it becomes lethal.
- *Better encounter rate*: Each Person object should know how many people they meet a day on average, and you should come
up with a strategy to assign an encounter rate to each person in your population.
- *Improved visualization*: Go crazy, and make a new visual representation of the spread of the disease.
- *Mutating disease*: This one would be hard, but fun: Each day there should be a chance for the disease to mutate, 
changing its parameters slightly. Over time this could create a brand new disease.