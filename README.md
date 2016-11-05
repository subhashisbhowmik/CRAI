# CRAI - The Chain Reaction AI
## Introduction
__CRAI__ is the first Open Source AI for playing a 2 Player "Chain Reaction" Game, written in python.

__CRAI__ is based on "alpha-beta Pruning Algorithm", with a variable max_depth look-ahead.

## Requirements
- python 2.7
- git

## Files
* __Game.py__
    >Contains the Core Game Engine for the "Chain Reaction" game.
* __CRAI.py__
    >Contains the Core AI Engine for the 2 Player "Chain Reaction" game.
* __SpeedTest.py__
    >Contains code for checking out the time taken for each turn on a randomly generated game state.
* __main.py__
    >Contains code for running the Game Engine and the AI Engine together. You can play with upto 7 other human players without the AI Engine.

## Usage
For a blind check, just clone the repo and run the main.py file. 
The main.py file can be modified to:
- Change the max_depth of the alpha-beta pruning algorithm
- Define the total number of players (Min=2, Max=8). AI can be assigned only if it is 2.
- Assign the AI to any one player or both (Applicable for 2P mode only).
