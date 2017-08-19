# Low Hanging Fruits - Script

### Purpose
After shopping with the `compare.py` script, I realised I was missing some pretty common ratings. This little
program is looking for beers in Germany, Austria or Switzerland that have e.g. 100 and more ratings and hence is a
common beer and easy to get in that country.

### Usage
The program is split in two parts. Part one (`gen_Bier.save.py`) generates a list of "all" beers available in
a country. Part two (`local_fruits.py`) generates a text-file that list the names of the missing ratings.

#### gen_Bier.save.py
A list of all the breweies in the country is need and stored as `Brauereien.lst` in the programs directory. Only
one brewery per line and no special character (less is more).
```sh
python gen_Bier.save.py - - de
```
Currently the parameters `de`, `at` and `ch` are available.<br>
The files `de-Bier.save` for Germany, `ch-Bier.save` for Switzerland and thanks to
[SinH4](https://www.ratebeer.com/user/324362/) `at-Bier.save` for Austria are available in the repository
(as per Aug. 2017)

#### local_fruits.py
For comparison your ratings as `*.csv` files (more in the 
[Readme.md](https://github.com/neur0nic/Ratebeer-Shopping-Helper/blob/master/Readme.md)) are needed.
```sh
python local_fruits.py username minimum_ratings locale
``` 
for example
```sh
python local_fruits.py neur0 200 de
``` 
generates a text file with all the German beers with more then 200 ratings that neur0 hasn't rated.

### Disclaimer
I wrote this pretty quickly, half in German, half in English, so the code is close to unreadable (even for me). Also
[ratebeer.py](https://github.com/alilja/ratebeer) returned some errors and I just started to ignore them. So maybe this
will not be a complete list of <b>low hanging fruits</b>, but it's the next step to get some quick ratings.<br>
This program is only tested with Python 3.6 on a Linux machine.
