# -*- coding: utf-8 -*-
from fruity_routines import *
from time import time


def check_breweries():
    compare_lst_of_breweries()
    load_brewery_info()


if __name__ == '__main__':
    start_time = time()

    check_breweries()
    load_all_beers(sys.argv[3])
    rm_savefiles_1()

    duration = ddhhmmss((time() - start_time))
    print("\n Program ran for: %sd %sh %sm %ss" % duration)
