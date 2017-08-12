#-*-coding:utf8;-*-
#qpy:console
#qpy:2

import pickle
import os
from termcolor import colored
import platform


def loaddata():
    ## Load and sort data
    # while True:
    #     available = []
    #     inDir = os.listdir(wdir)
    #     for i in inDir:
    #         if i[-8:] == ".ratings":
    #             available.append(i[0:-8])
    #
    #     amount = 2 #input("Shopping for how many Ratebeerians? ")
        # try: amount = int(amount)
        # except: print("Please insert an integer ")
        # users = []
        # k = 0
        # for i in range(0, amount):
        #     k += 1
        #     while True:
        #         user = input("Username #" + str(k) + ": ")
        #         if isinstance(user, str):
        #             if user in available:
        #                 if user not in users:
        #                     users.append(user)
        #                     break
        #                 else:
        #                     print("User already in list.")
        #                     while True:
        #                         answer = input("Do you want to reduce the number of ratebeerians by 1? (Y/N)")
        #                         if answer.lower() == "y":
        #                             amount -= 1
        #                             k -= 1
        #                             break
        #                         elif answer.lower() == "n":
        #                             k -= 1
        #                             break
        #                     break
        #             else: print("Error: Typo in username or ratings are not available. Please try again. ")
        # break
    users = ["neur0", "jfb"]
    ratings = []
    machine = platform.machine()
    wdir = ("./")
    if (machine == 'armv7l'):
        wdir = ('/storage/emulated/0/qpython/scripts3')
    for i in users: ratings.append(i.split())
    for i in range(0, len(users)):
        # with open((users[i] + ".ratings"), "rb") as f: ratings[i].append(pickle.load(f))
        with open((wdir + users[i] + ".ratings"), "rb") as f: ratings[i].append(pickle.load(f))
    return ratings


def searchbeer(userratings, srch):
    fnd = []
    for i in userratings:
        if srch.lower() in i.lower():
            fnd.append(i)
    return fnd


def mapresults(found):
    matrix = []
    for userliste in range(0, len(found)):
        for beer in found[userliste]:
            if beer not in matrix:
                matrix.append(beer)

    for i in range(0, len(matrix)):
        obj = []
        obj.append(matrix[i])
        matrix[i] = obj

    newmatrix = matrix
    for beer in matrix:
        for userlisten in found:
            count = 0
            for rating in userlisten:
                i = newmatrix.index(beer)
                if rating in beer:
                    count += 1
            if count > 0:
                newmatrix[i].append(1)
            else:
                newmatrix[i].append(0)
    return newmatrix


def colorize(matrix, user):
    newmatrix = matrix
    for line in range(0, len(matrix)):
        for users in range(0, len(user)):
            if matrix[line][users + 1] == 0:
                newmatrix[line][users + 1] = (colored(user[users], "red"))
            elif matrix[line][users + 1] == 1:
                newmatrix[line][users + 1] = (colored(user[users], "green"))
    for i in newmatrix:
        for j in i:
            print(j + " ", end="")
        print("\n")


def main():
    ratings = loaddata()

    print("---------------------------------------------------------\n"
          "| Start shopping - Enter Beer Name - Enter exit to quit |\n"
          "|       " + colored("red", "red") + " means: not rated; " + colored("green", "green") + " means: rated        |\n"
          "---------------------------------------------------------")
    while True:
        search = input("> ")
        if search == "exit":
            break

        found = []
        for i in range(0, len(ratings)):
            found.append(sorted(searchbeer(ratings[i][1], search)))

        outputmatrix = mapresults(found)
        # for i in outputmatrix:
        #     print(str(i))

        users = [ratings[0][0], ratings[1][0]]
        colorize(outputmatrix, users)

if __name__ == '__main__':
    main()
