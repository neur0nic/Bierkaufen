###
# This file will take the csv files from ratebeer.com and convert the beernames and into a list.
import csv
import os
import pickle

while True:
    user = input("Username: ")
    if isinstance(user, str):
        if " " not in user: break
        else: pass
    else:
        pass

dirContent = os.listdir("./")
files = []
for i in dirContent:
    if user and "csv" in i: files.append(i)

ratings = []
for i in files:
    with open(i, "r") as f: ratings += csv.reader(f)

ratingsNew = []
for i in ratings:
    ratingsNew.append(i[1:3])

container = (user + ".ratings")
with open(container, "wb") as f: pickle.dump(ratingsNew, f)


