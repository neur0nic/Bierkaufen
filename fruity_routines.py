import ratebeer
import csv
import os
import pickle
import sys
from termcolor import colored

rb = ratebeer.RateBeer()


def ddhhmmss(seconds):
    s_per_d = 86400
    s_per_h = 3600
    s_per_m = 60
    d = int(seconds / s_per_d)
    h = int((seconds % s_per_d) / s_per_h)
    m = int(((seconds % s_per_d) % s_per_h) / s_per_m)
    s = round((((seconds % s_per_d) % s_per_h) % s_per_m), 2)
    return d, h, m, s


def progressBar(current, total):
    i = round((current / total) * 100, 1)
    strdone = int(round(i, 0)) * '█'
    strundone = (100 - int(round(i, 0))) * '█'
    totstr = "|" + colored(strdone, 'green') + colored(strundone, 'red') + "| " + str(i) + "%"
    print(totstr, end='\r')


def ownRatings():
    dirContent = os.listdir("./")
    switch = False
    files = []
    while True:
        user = sys.argv[1]
        if isinstance(user, str):
            for i in dirContent:
                if user in i:
                    if "csv" in i:
                        files.append(i)
                        switch = True
            if switch: break
            else:
                exit(1)

    ratings = []
    for i in files:
        with open(i, "r") as f:
            read = csv.reader(f, delimiter='|')
            for i in read:
                ratings.append(i)

    ratingsNew = []
    for i in ratings: ratingsNew.append([i[0], i[1], i[11], i[12], i[14]])

    # for i in ratingsNew: print(i)
    return ratingsNew


def getBreweries(query):
    resultNew = []
    try:
        result = rb.search(query.lower())
        resultNew = result["breweries"]
    except:
        addToLog('Brauerei ausgelassen: ' + query + '; Fehler bei Suche\n')
    return resultNew


def brauereienAbgleichen():
    print('\n Abgleichen der Liste mit Brauereien auf ratebeer.com.')
    with open("Brauereien.lst", "r") as fr:
        readbrauereien = fr.readlines()

    brauereien = []
    for i in readbrauereien:
        brauereien.append(i.replace("\n", ""))

    ratebeerBrauereien = []
    itertotal = len(brauereien)
    counter = 0
    for i in brauereien:
        counter += 1
        progressBar(counter, itertotal)
        try:
            resultat = getBreweries(i)
        except:
            pass
        for j in resultat:
            ratebeerBrauereien.append(j)
    print()
    list(set(ratebeerBrauereien))

    with open('Brauerei.save', 'wb') as fw: pickle.dump(ratebeerBrauereien, fw)


def brauerienInfosLaden():
    print('\n Laden der Infos der gefundenen Brauereien und nicht deutsche Brauereien aussorieren.')
    with open('Brauerei.save', 'rb') as fr: ratebeerBrauereien = pickle.load(fr)

    brauereiInfo = []
    itertotal = len(ratebeerBrauereien)
    counter = 0
    for i in ratebeerBrauereien:
        counter += 1
        progressBar(counter, itertotal)
        try:
            brauereiInfo.append(i._populate())
        except:
            addToLog("Brauerei ausgelassen: " + str(i.__dict__['url']) + "; Fehler bei _populate.\n")
    print()

    with open('BrauereiInfo.save', 'wb') as fw: pickle.dump(brauereiInfo, fw)


def bierlisteLaden():
    print('\n Alle Biere und deren Infos von den Brauereien laden.')
    with open('BrauereiInfo.save', 'rb') as fr: brauereiInfo = pickle.load(fr)
    
    if sys.argv[3] == 'at':
        country = 'Austria'
    elif sys.argv[3] == 'ch':
        country = 'Switzerland'
    else:
        country = 'Germany'
    
    dtBrauereien = []
    for i in brauereiInfo:
        try:
            if country in i.__dict__["location"]:
                dtBrauereien.append(i)
        except:
            addToLog('Brauerei ausgelassen: ' + str(i) + '; Fehler bei location\n')

    Bier = []
    FailBrauereien = []
    itertotal = len(dtBrauereien)
    counter = 0
    for i in dtBrauereien:
        counter += 1
        progressBar(counter, itertotal)
        z = i.get_beers()
        try:
            for j in z:
                try:
                    Bier.append(j._populate())
                    with open('Biere.failsave', 'wb') as fw: pickle.dump(Bier, fw)
                except:
                    addToLog('Bier ausgelassen: ' + str(j) + '; Fehler wegen Alias.\n')
            print(z.name + ' fertig.')
            FailBrauereien.append(i)
            with open('Brauereien_fertig.failsave', 'wb') as fw: pickle.dump(FailBrauereien, fw)
        except:
            addToLog('Leere Brauerei.\n')
    print()

    if sys.argv[3] == 'ch':
        Bierfile = 'ch-Biere.save'
    elif sys.argv[3] == 'de':
        Bierfile = 'de-Biere.save'
    elif sys.argv[3] == 'at':
        Bierfile = 'at-Biere.save'
    else:
        Bierfile = 'Biere.save'

    with open(Bierfile, 'wb') as fw: pickle.dump(Bier, fw)


def biereAussortieren():
    print('\n Aussortieren der schon gerateten Biere und filtern nach Mindestanzahl der Ratings.')
    if sys.argv[3] == 'ch':
        Bierfile = 'ch-Biere.save'
    elif sys.argv[3] == 'de':
        Bierfile = 'de-Biere.save'
    elif sys.argv[3] == 'at':
        Bierfile = 'at-Biere.save'
    else:
        Bierfile = 'Biere.save'

    with open(Bierfile, 'rb') as fr: Bier = pickle.load(fr)

    popularBeers = []
    itertotal = len(Bier)
    counter = 0
    for i in Bier:
        counter += 1
        progressBar(counter, itertotal)
        if i.__dict__['num_ratings'] >= int(sys.argv[2]):
            popularBeers.append(i)

    ratings = ownRatings()

    unrated = []
    for i in popularBeers:
        counter = 0
        for j in ratings:
            if j[0] in i.__dict__['url']:
                counter += 1
        if counter == 0:
            unrated.append(i)

    with open('Unrated.save', 'wb') as fw: pickle.dump(unrated, fw)


def doppelAussortieren():
    with open('Unrated.save', 'rb') as fr: unrated = pickle.load(fr)

    sortable = []
    for i in unrated:
        sortable.append(i.name)
    sortable.sort()

    storable = []
    for i in sortable:
        if i in storable:
            pass
        else:
            storable.append(i)

    with open('storable.save', 'wb') as fw: pickle.dump(storable, fw)


def biereSpeichern():
    with open('storable.save', 'rb') as fr: storable = pickle.load(fr)
    with open((sys.argv[1] + "s_popular_unrated-" + sys.argv[3] + ".txt"), "w") as fw:
        for i in storable:
            fw.write((i + "\n"))
    print('\n\n Biere sind gespeichert als ' + sys.argv[1] + "s_popular_unrated-" + sys.argv[3] + ".txt")


def addToLog(Fehler):
    if isinstance(Fehler, str):
        with open('Fehler.log', 'a') as fa: fa.write(Fehler)
    else:
        pass
