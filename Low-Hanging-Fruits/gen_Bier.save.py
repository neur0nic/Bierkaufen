# -*- coding: utf-8 -*-
from time import time

from fruity_routines import *


def check_breweries():
    compare_lst_of_breweries()
    load_brewery_info()


if __name__ == '__main__':
    start_time = time()

    create_folders()
    check_breweries()
    load_all_beers(sys.argv[3])
    rm_savefiles_1()

    duration = ddhhmmss((time() - start_time))
    print("\n Program ran for: %sd %sh %sm %ss" % duration)
