# import the CSV Library
import csv

# open and read the file
with open("csample.csv")as csvfile:
    csample = csv.reader(csvfile, delimiter=',')

# get the rows of the CSV file and show them
    for row in csample:
        print("{device} is in {location} and has IP {ip}.".format(
            device=row[0],
            ip=row[1],
            location=row[1])
        )



