# -*- coding: utf-8 -*-
from fruity_routines import *
from time import time


def main():
    start_time = time()

    brauereienAbgleichen()
    brauerienInfosLaden()
    bierlisteLaden()  # Bis hier bitte auskommentieren
    biereAussortieren(sys.argv[2])
    doppelAussortieren()
    biereSpeichern()

    duration = ddhhmmss((time() - start_time))
    print("\n Program ran for: %sd %sh %sm %ss" % duration)


if __name__ == '__main__':
    main()
