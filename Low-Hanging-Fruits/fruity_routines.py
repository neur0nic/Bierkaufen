import ratebeer
import csv
import os
import pickle
import sys
from termcolor import colored
from time import strftime

rb = ratebeer.RateBeer()
wdir = os.getcwd()
if '/Low-Hanging-Fruits' in wdir: wdir = wdir[:wdir.find('/Low-Hanging-Fruits')]
tmpdir = wdir + '/Low-Hanging-Fruits/tmp/'
rtngdir =wdir + '/Ratings/'
lhfdir = wdir + '/Low-Hanging-Fruits/'


def ddhhmmss(seconds):
    """
    Converts seconds in a human readable format.

    :param seconds: seconds (float)
    :return : days, hours, minutes, seconds (tuple)
    """

    s_per_d = 86400
    s_per_h = 3600
    s_per_m = 60
    d = int(seconds / s_per_d)
    h = int((seconds % s_per_d) / s_per_h)
    m = int(((seconds % s_per_d) % s_per_h) / s_per_m)
    s = round((((seconds % s_per_d) % s_per_h) % s_per_m), 2)
    return d, h, m, s


def cleanup(objekte):
    """
    Removes duplicates in brewery- or beer-object lists
    :param objekte: list of brewery- or beer-objects from ratebeer.py
    :return: list of brewery- or beer-objects
    """

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


def progress_bar(current, total):
    """
    Creates an progress bar for iterative processes.
    :param current: number of iterations already done (int)
    :param total: total number of iterations (int)
    """

    i = round((current / total) * 100, 1)
    strdone = int(round(i, 0)) * '█'
    strundone = (100 - int(round(i, 0))) * '█'
    totstr = "|" + colored(strdone, 'green') + colored(strundone, 'red') + "| " + str(i) + "%"
    print(totstr, end='\r')


def ownRatings(username):
    """
    Reads the downloaded ratings form ratebeer.com and converts them into a list.
    :param username: ratebeer username (str)
    :return: list of list. The inner lists are the ratings with the attributes
        ['BeerID', 'Beer', 'Country', 'State', 'Style']
    """

    global rtngdir
    dirContent = os.listdir(rtngdir)
    switch = False
    files = []
    while True:
        user = username
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
        with open((rtngdir + i), "r") as f:
            read = csv.reader(f, delimiter='|')
            for i in read:
                ratings.append(i)

    ratingsNew = []
    for i in ratings: ratingsNew.append([i[0], i[1], i[11], i[12], i[14]])

    # for i in ratingsNew: print(i)
    return ratingsNew


def getBreweries(query):
    """
    Search for breweries on ratebeer.com
    :param query: search term (str)
    :return: a list of brewery-generator-objects
    """

    resultNew = []
    try:
        result = rb.search(query.lower())
        resultNew = result["breweries"]
    except:
        addToLog('Brewery skipped: ' + query + '; search returned an error.\n')
    return resultNew


def compare_lst_of_breweries():
    """
    Iterates through the breweries.lst file and tries to find the breweries on ratebeer.com
    :return: stores a list of brewery-generator-objects in brewery.save
    """
    global rtngdir
    global tmpdir
    print('\n Compare the list of breweries with the breweries on ratebeer.com')
    with open((lhfdir + "breweries.lst"), "r") as fr:
        read_breweries = fr.readlines()

    breweries = []
    for i in read_breweries:
        breweries.append(i.replace("\n", ""))

    ratebeer_breweries = []
    itertotal = len(breweries)
    counter = 0
    for i in breweries:
        counter += 1
        progress_bar(counter, itertotal)
        try:
            result = getBreweries(i)
        except:
            result = []
            pass
        for j in result:
            ratebeer_breweries.append(j)
    print()

    ratebeer_breweries = cleanup(ratebeer_breweries)

    with open((tmpdir + 'brewery.save'), 'wb') as fw: pickle.dump(ratebeer_breweries, fw)


def load_brewery_info():
    """
    Populates the list of brewery-generator-objects.
    :return: stores a list of brewery-objects in brewery_info.save
    """

    global tmpdir
    print('\n Downloading the infos of the breweries from ratebeer and filtering the breweries by the '
          'location "' + str(sys.argv[3]) + '".')
    with open((tmpdir + 'brewery.save'), 'rb') as fr: ratebeer_breweries = pickle.load(fr)

    brewerie_info = []
    itertotal = len(ratebeer_breweries)
    counter = 0
    for i in ratebeer_breweries:
        counter += 1
        progress_bar(counter, itertotal)
        try:
            brewerie_info.append(i._populate())
        except:
            addToLog("Brewery skipped: " + str(i.__dict__['url']) + "; _populate returned an error.\n")
    print()

    with open((tmpdir + 'brewery_info.save'), 'wb') as fw: pickle.dump(brewerie_info, fw)


def load_all_beers(locale):
    """
    Loads the beer-generator-objects of the breweries and populates then.
    :param locale: ISO 3166-1 country code (str)
    :return: stores list of beer-objects to *-Biere.save
    """

    global tmpdir
    print('\n Downloading the beers for the breweries, including their information.')
    with open((tmpdir + 'brewery_info.save'), 'rb') as fr: brewerie_info = pickle.load(fr)

    ccodes = {'at': 'Austria', 'ch': 'Switzerland', 'de': 'Germany'}
    try:
        country = ccodes[locale]
    except:
        country = ccodes['de']
    
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
        progress_bar(counter, itertotal)
        z = i.get_beers()
        try:
            for j in z:
                try:
                    beer.append(j._populate())
                    with open((tmpdir + 'beers.failsave'), 'wb') as fw: pickle.dump(beer, fw)
                except:
                    addToLog('Beer skipped: ' + str(j) + '; error while redirecting from alias.\n')
        except:
            addToLog('Empty brewery object.\n')
    print()

    try:
        beerfile = locale + '-Biere.save'
    except:
        beerfile = 'de-Biere.save'
    with open((lhfdir + beerfile), 'wb') as fw: pickle.dump(beer, fw)


def filter_beers(locale, minrate, username):
    """
    Filters beers by minimal amount of ratings and filters the already rated beers.
    :param locale: ISO 3166-1 country code (str)
    :param minrate: minimal amount of ratings (int)
    :param username: ratebeer username (str)
    :return: stores a list of beer-objects in Unrated.save
    """

    global lhfdir
    global tmpdir
    print('\n Filtering the already rated beers. Filtering the beers below minimal amount of ratings (' + str(sys.argv[2]) + ').')
    try:
        beerfile = locale + '-Biere.save'
    except:
        beerfile = 'de-Biere.save'

    with open((lhfdir + beerfile), 'rb') as fr: beer = pickle.load(fr)

    popular_beers = []
    itertotal = len(beer)
    counter = 0
    for i in beer:
        counter += 1
        progress_bar(counter, itertotal)
        if i.__dict__['num_ratings'] >= int(minrate):
            popular_beers.append(i)

    ratings = ownRatings(username)

    unrated = []
    for i in popular_beers:
        counter = 0
        for j in ratings:
            if j[0] in i.__dict__['url']:
                counter += 1
        if counter == 0:
            unrated.append(i)

    unrated = cleanup(unrated)
    
    with open((tmpdir + 'Unrated.save'), 'wb') as fw: pickle.dump(unrated, fw)


def sort_and_encoding():
    """
    Sorts the beers by name and removes artifacts from encoding
    :return: stores a list of beers (str) in storable.save
    """

    global tmpdir
    with open((tmpdir + 'Unrated.save'), 'rb') as fr: unrated = pickle.load(fr)

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

    with open((tmpdir + 'storable.save'), 'wb') as fw: pickle.dump(storable, fw)


def save_beers(username, locale):
    """
    Stores the list of beernames into a human readable file
    :param locale: ISO 3166-1 country code (str)
    :param username: ratebeer username (str)
    :return: plain text file with beernames
    """

    global tmpdir
    global rtngdir
    with open((tmpdir + 'storable.save'), 'rb') as fr: storable = pickle.load(fr)
    with open((rtngdir + username + "s_popular_unrated-" + locale + ".txt"), "w") as fw:
        for i in storable:
            fw.write((i + "\n"))
    print('\n\n Your low hanging fruits are saved as ' + rtngdir + username + "s_popular_unrated-" + locale + ".txt")


def addToLog(Fehler):
    """
    Stores errors to local file
    :param Fehler: error message (str)
    :return: stores error messages with timecode to Fehler.log
    """

    global lhfdir
    if isinstance(Fehler, str):
        time = strftime("%Y-%m-%d: %H:%M:%S - ")
        with open((lhfdir + 'Fehler.log'), 'a') as fa: fa.write(time + Fehler)
    else:
        pass


def rm_savefiles_1():
    """
    Removes the files creates during gen_Bier.save.py
    """

    global tmpdir
    os.remove(tmpdir + 'brewery.save')
    os.remove(tmpdir + 'brewery_info.save')
    os.remove(tmpdir + 'beers.failsave')


def rm_savefiles_2():
    """
    Removes the files creates during local_fruits.py
    """

    global tmpdir
    os.remove(tmpdir + 'Unrated.save')
    os.remove(tmpdir + 'storable.save')
