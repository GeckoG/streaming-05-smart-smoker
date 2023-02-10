# streaming-05-smart-smoker
Work from module 5 of Streaming Data at NWMSU

> This program sends temperature readings from a smoker (csv file) to a set of queues

# Running the program
This program is designed to run on its own, as long as a properly named csv file (smokertemps.csv) is in the directory
When the program starts, it will declare queues for the smoker, food 1, and food 2.
Once it declares the queues, it reads the temperatures from the csv, and sends each of the 3 temps to its own queue to await reception by a receiver.

# Screenshot of Program Running
![img](screenshot.PNG)