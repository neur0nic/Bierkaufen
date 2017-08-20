# -*- coding: utf-8 -*-
from fruity_routines import *


def create_list():
    filter_beers(sys.argv[3], sys.argv[2], sys.argv[1])
    sort_and_encoding()
    save_beers(sys.argv[1], sys.argv[3])
    rm_savefiles_2()


if __name__ == '__main__':
    create_list()
