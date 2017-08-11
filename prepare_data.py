###
# This file will take the csv files from ratebeer.com and convert the beernames and into a list.
import csv
import os
import pickle


dirContent = os.listdir("./")
switch = False
while True:
    user = input("Username: ")
    if isinstance(user, str):
        for i in dirContent:
            if user in i:
                if "csv" in i:
                    file = i
                    switch = True
                    break
        if switch: break
        else: pass
    else:
        pass

with open(file, "r") as f:
    read = csv.reader(f)
    ratings = []
    for i in read:
        ratings.append(i)

ratingsNew = []
for i in ratings: ratingsNew.append(i[1])

container = (user + ".ratings")
with open(container, "wb") as f: pickle.dump(ratingsNew, f)


