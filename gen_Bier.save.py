# -*- coding: utf-8 -*-
from fruity_routines import *
from time import time


def checkBrauereien():

    brauereienAbgleichen()
    brauerienInfosLaden()


def ladeBiere():
    bierlisteLaden()


if __name__ == '__main__':
    start_time = time()

    checkBrauereien()
    bierlisteLaden()

    duration = ddhhmmss((time() - start_time))
    print("\n Program ran for: %sd %sh %sm %ss" % duration)
