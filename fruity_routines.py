import ratebeer
import csv
import os
import pickle
import sys
from termcolor import colored
from time import strftime

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


def cleanup(objekte):
    clean = []
    save = []
    for i in objekte:
        if i.url in save:
            pass
        else:
            clean.append(i)
            save.append(i.url)
    if len(clean) != len(save):
        addToLog('Error while cleanup.')
    return clean


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
        addToLog('Brewery skipped: ' + query + '; search returned an error.\n')
    return resultNew


def compare_lst_of_breweries():
    print('\n Compare the list of breweries with the breweries on ratebeer.com')
    with open("breweries.lst", "r") as fr:
        read_breweries = fr.readlines()

    breweries = []
    for i in read_breweries:
        breweries.append(i.replace("\n", ""))

    ratebeer_breweries = []
    itertotal = len(breweries)
    counter = 0
    for i in breweries:
        counter += 1
        progressBar(counter, itertotal)
        try:
            resultat = getBreweries(i)
        except:
            pass
        for j in resultat:
            ratebeer_breweries.append(j)
    print()

    ratebeer_breweries = cleanup(ratebeer_breweries)

    with open('brewery.save', 'wb') as fw: pickle.dump(ratebeer_breweries, fw)


def load_brewery_info():
    print('\n Downloading the infos of the breweries from ratebeer and filtering the breweries by the '
          'location "' + str(sys.argv[3]) + '".')
    with open('brewery.save', 'rb') as fr: ratebeer_breweries = pickle.load(fr)

    brewerie_info = []
    itertotal = len(ratebeer_breweries)
    counter = 0
    for i in ratebeer_breweries:
        counter += 1
        progressBar(counter, itertotal)
        try:
            brewerie_info.append(i._populate())
        except:
            addToLog("Brewery skipped: " + str(i.__dict__['url']) + "; _populate returned an error.\n")
    print()

    with open('brewery_info.save', 'wb') as fw: pickle.dump(brewerie_info, fw)


def load_all_beers():
    print('\n Downloading the beers for the breweries, including their information.')
    with open('brewery_info.save', 'rb') as fr: brewerie_info = pickle.load(fr)
    
    if sys.argv[3] == 'at':
        country = 'Austria'
    elif sys.argv[3] == 'ch':
        country = 'Switzerland'
    else:
        country = 'Germany'
    
    local_breweries = []
    for i in brewerie_info:
        try:
            if country in i.__dict__["location"]:
                local_breweries.append(i)
        except:
            addToLog('Brewery skipped: ' + str(i) + '; location cannot be read \n')

    beer = []
    itertotal = len(local_breweries)
    counter = 0
    for i in local_breweries:
        counter += 1
        progressBar(counter, itertotal)
        z = i.get_beers()
        try:
            for j in z:
                try:
                    beer.append(j._populate())
                    with open('beers.failsave', 'wb') as fw: pickle.dump(beer, fw)
                except:
                    addToLog('Beer skipped: ' + str(j) + '; error while redirecting from alias.\n')
        except:
            addToLog('Empty brewery object.\n')
    print()



    if sys.argv[3] == 'ch':
        beerfile = 'ch-Biere.save'
    elif sys.argv[3] == 'de':
        beerfile = 'de-Biere.save'
    elif sys.argv[3] == 'at':
        beerfile = 'at-Biere.save'
    else:
        beerfile = 'Biere.save'

    with open(beerfile, 'wb') as fw: pickle.dump(beer, fw)


def filter_beers():
    print('\n Filtering the already rated beers. Filtering the beers below minimal amount of ratings (' + str(sys.argv[2]) + ').')
    if sys.argv[3] == 'ch':
        beerfile = 'ch-Biere.save'
    elif sys.argv[3] == 'de':
        beerfile = 'de-Biere.save'
    elif sys.argv[3] == 'at':
        beerfile = 'at-Biere.save'
    else:
        beerfile = 'Biere.save'

    with open(beerfile, 'rb') as fr: beer = pickle.load(fr)

    popular_beers = []
    itertotal = len(beer)
    counter = 0
    for i in beer:
        counter += 1
        progressBar(counter, itertotal)
        if i.__dict__['num_ratings'] >= int(sys.argv[2]):
            popular_beers.append(i)

    ratings = ownRatings()

    unrated = []
    for i in popular_beers:
        counter = 0
        for j in ratings:
            if j[0] in i.__dict__['url']:
                counter += 1
        if counter == 0:
            unrated.append(i)

    unrated = cleanup(unrated)
    
    with open('Unrated.save', 'wb') as fw: pickle.dump(unrated, fw)


def sort_and_encoding():
    with open('Unrated.save', 'rb') as fr: unrated = pickle.load(fr)

    sortable = []
    for i in unrated:
        sortable.append(i.name)
    sortable.sort()

    storable = []
    for i in sortable:
        z = i.replace('Ã¤', 'ä').replace('Ã¼', 'ü').replace('Ã¶', 'ö').replace('Ã', 'ß').replace('â', '’') \
            .replace('Ã©', 'é').replace('Ã§', 'ç').replace('Ã¸', 'ø').replace('Ã¥', 'å').replace('Ã', 'Ü') \
            .replace('Ã', 'Ä').replace('Ã', 'Ö').replace('Ã¨', 'è').replace('Â½', '½').replace('Ã´', 'ô') \
            .replace('Ã²', 'ò').replace('Ãª', 'ê').replace('Â´', '´').replace('Ã«', 'ë').replace('Ã®', 'î') \
            .replace('Ã¹', 'ù').replace('Ã', 'Ø').replace('Ã ', 'à').replace('Ã¢', 'â').replace('Ã ', 'à') \
            .replace('Ã³', 'ó').replace('Ã¯', 'ï').replace('Ãº', 'ú').replace('Ã', 'É').replace('Ã', 'Ò')
        storable.append(z)

    with open('storable.save', 'wb') as fw: pickle.dump(storable, fw)


def save_beers():
    with open('storable.save', 'rb') as fr: storable = pickle.load(fr)
    with open((sys.argv[1] + "s_popular_unrated-" + sys.argv[3] + ".txt"), "w") as fw:
        for i in storable:
            fw.write((i + "\n"))
    print('\n\n Your low hanging fruits are saved as ' + sys.argv[1] + "s_popular_unrated-" + sys.argv[3] + ".txt")


def addToLog(Fehler):
    if isinstance(Fehler, str):
        time = strftime("%Y-%m-%d: %H:%M:%S - ")
        with open('Fehler.log', 'a') as fa: fa.write(time + Fehler)
    else:
        pass


def rm_savefiles_1():
    os.remove('brewery.save')
    os.remove('brewery_info.save')
    os.remove('beers.failsave')


def rm_savefiles_2():
    os.remove('Unrated.save')
    os.remove('storable.save')
