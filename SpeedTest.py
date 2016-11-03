#!/bin/sh
__author__ = 'Subhashis'

import Game
import CRAI
from time import time

amount = 1000
t0 = time()
state = Game.random_instance()
print 1
for i in range(amount):
    if (i + 1) % 100 == 0:
        print i+1
    if state.winner < 0:
        state = Game.random_instance()
    state.move(CRAI.random_move(state.grid, state.current_player))
t = time() - t0
print "Total Time:", str(t), "s for", str(amount), "moves."
print "Per Second:", str(amount / t)