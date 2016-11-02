__author__ = 'Subhashis'

import random
import Game
from copy import copy


# Currently for 2P mode only
class CRAIController(Game.Controller):
    def __init__(self, max_depth=3):
        self.max_depth = max_depth

    def make_move(self, state):
        print "Waiting for player " + str(state.current_player) + "..."
        node = Node(state, self.max_depth)
        node.evaluate()
        if state.winner < 0:
            print "\nMove from Player", str(state.current_player) + ":"
        return node.next_move


class Node:
    def __init__(self, state, max_depth=3, player=1, mini=False, depth=0, parents=[]):
        self.state = state
        self.mini = mini
        self.val = 0
        self.depth = depth
        self.parents = parents
        self.max_depth = max_depth
        self.set = False
        self.next_move = 0
        self.next_node = 0
        self.player = player

    def child(self, move):
        state = self.state.move(move, True)
        parents = copy(self.parents) + [self]
        return Node(state, self.max_depth, self.player, not self.mini, self.depth + 1, parents)

    def value(self):
        return self.state.evaluate()

    def evaluate(self):
        if self.depth >= self.max_depth:
            self.val = self.value()
            return self.val
        if self.state.winner is not -1:
            if self.state.winner is self.player:
                return 10000
            else:
                return -10000
        l = self.state.all_moves()
        return_none = False
        for i in range(len(l)):
            child = self.child(l[i])
            cv = child.evaluate()
            if cv is not None:
                if not self.set:
                    self.val = cv
                    self.next_move = l[i]
                    self.next_node = child
                    self.set = True
                elif self.mini:
                    if cv < self.val:
                        self.val = cv
                        self.next_move = l[i]
                        self.next_node = child
                else:
                    if cv > self.val:
                        self.val = cv
                        self.next_move = l[i]
                        self.next_node = child

            # The following loop implements the alpha-beta pruning. Removing it will cause the algorithm to become
            # a simpler MiniMax search. The loop does nothing but remove redundant options, improving the efficiency.
            for j in range(len(self.parents)):
                if self.parents[j].mini is True and self.mini is False and self.parents[j].set:
                    if self.val > self.parents[j].val:
                        return_none = True
                        break
                elif self.parents[j].mini is False and self.mini is True and self.parents[j].set:
                    if self.val < self.parents[j].val:
                        return_none = True
                        break
        if return_none:
            return None
        return self.val
