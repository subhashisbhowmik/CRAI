#!/bin/python
__author__ = 'Subhashis'

import Game
import CRAI

total_players = 2 # CRAI only works for 2P mode now. For >2 player, comment out the marked line.
grid_size = (5, 5)
max_depth = 3

state = Game.new_instance(grid_size, total_players)

# state.register_controller(CRAI.CRAIController(max_depth), 0)  # Uncomment this line to play CPU v/s CPU.
state.register_controller(CRAI.CRAIController(max_depth), 1)  # For all human players, Comment out this line.

state.run()