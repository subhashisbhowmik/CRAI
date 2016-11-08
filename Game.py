__author__ = 'Subhashis'

from copy import copy, deepcopy
import random


def _grid_play(grid, move, player_counts, player_points, moving_player, state):
    q = [move]
    while len(q) > 0 and state.winner == -1:
        move = q[0]
        q = q[1:]
        if (0 <= move[1] < len(grid[0])) and (0 <= move[0] < len(grid)):
            can_win = True
            if grid[move[0]][move[1]].is_full():
                player_counts[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value
                player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value
                if grid[move[0]][move[1]].on_edge:
                    player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value * ChainReactionState.edge_points
                if grid[move[0]][move[1]].on_corner:
                    player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value * ChainReactionState.corner_points

                grid[move[0]][move[1]].value = 0
                can_win = False
                q += [(move[0] - 1, move[1]), (move[0], move[1] - 1), (move[0] + 1, move[1]),
                      (move[0], move[1] + 1)]
            else:
                player_counts[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value
                player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value
                if grid[move[0]][move[1]].on_edge:
                    player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value * ChainReactionState.edge_points
                if grid[move[0]][move[1]].on_corner:
                    player_points[grid[move[0]][move[1]].player] -= grid[move[0]][move[1]].value * ChainReactionState.corner_points
                grid[move[0]][move[1]].value += 1
                grid[move[0]][move[1]].player = moving_player
                player_counts[grid[move[0]][move[1]].player] += grid[move[0]][move[1]].value
                player_points[grid[move[0]][move[1]].player] += grid[move[0]][move[1]].value
                if grid[move[0]][move[1]].on_edge:
                    player_points[grid[move[0]][move[1]].player] += grid[move[0]][move[1]].value * ChainReactionState.edge_points
                if grid[move[0]][move[1]].on_corner:
                    player_points[grid[move[0]][move[1]].player] += grid[move[0]][move[1]].value * ChainReactionState.corner_points
            if player_counts.count(0) == len(player_counts) - 1 and state.turn >= state.total_players and can_win:
                for i in range(len(player_counts)):
                    if player_counts[i] > 0:
                        state._won(i)
                        break


def new_instance(grid_size=(8, 8), player_count=2):
    grid = [[Square(grid_size, (i, j), 0, 0) for i in range(grid_size[0])] for j in range(grid_size[1])]
    player_counts = [0 for i in range(player_count)]
    player_points = [0 for i in range(player_count)]
    return ChainReactionState(grid, player_counts, player_points)


def random_instance(grid_size=(8, 8), player_count=2):
    grid = []
    player_counts = [0 for i in range(player_count)]
    player_points = [0 for i in range(player_count)]
    for i in range(grid_size[0]):
        row = []
        for j in range(grid_size[1]):
            s = Square(grid_size, (i, j), random.randrange(player_count), random.randrange(4))
            if s.overflown():
                s = Square(grid_size, (i, j), random.randrange(player_count), random.randrange(3))
            if s.overflown():
                s = Square(grid_size, (i, j), random.randrange(player_count), random.randrange(2))
            player_counts[s.player] += s.value
            player_points[s.player] += s.value
            if s.on_edge:
                player_points[s.player] += s.value * ChainReactionState.edge_points
            if s.on_corner:
                player_points[s.player] += s.value * ChainReactionState.corner_points

            row.append(s)
        grid += [row]
    return ChainReactionState(grid, player_counts, player_points, random.randrange(player_count))


class GameState:
    def __init__(self):
        pass

    def evaluate(self):
        raise NotImplementedError("Evaluate method must be implemented.")

    def move(self, move, test=False):
        raise NotImplementedError("Move method must be implemented.")

    def all_moves(self):
        raise NotImplementedError("All_moves method must be implemented.")

    def is_valid_move(self):
        raise NotImplementedError("Is_valid_move method must be implemented.")

    def run(self):
        raise NotImplementedError("run method must be implemented.")


class ChainReactionState(GameState):
    corner_points = 2
    edge_points = 1

    def __init__(self, grid, player_counts, player_points, current_player=0, turn=0, player_controllers=0, test=False):
        self.gridSize = (len(grid[0]), len(grid))
        self.grid = grid
        self.total_players = len(player_counts)
        self.player_counts = player_counts
        self.player_points = player_points
        self.turn = turn
        self.test = test
        self.winner = -1
        self.current_player = current_player
        if player_controllers is 0:
            self.player_controllers = [0 for i in range(self.total_players)]
        else:
            self.player_controllers = player_controllers
        self.undo = 0

    def play(self, move, moving_player, test):
        if self.winner != -1:
            if not test:
                print "Game has ended!"
            return self
        if not self.is_valid_move(move, moving_player):
            raise InvalidMoveException(
                "Invalid Move as player " + str(moving_player) + " at position (" + str(move[0]) + "," + str(
                    move[1]) + ").")
        grid = deepcopy(self.grid)
        player_counts = copy(self.player_counts)
        player_points = copy(self.player_points)

        _grid_play(grid, move, player_counts, player_points, moving_player, self)
        if self.winner < 0:
            return ChainReactionState(grid, player_counts, player_points, test=test)
        else:
            return self

    def move(self, move, test=False):
        if self.winner != -1:
            # print "Match has already ended!"
            return self
        turn = self.turn + 1
        current_player = (self.current_player + 1) % self.total_players
        while turn >= self.total_players and self.player_counts[current_player] == 0:
            current_player = (current_player + 1) % self.total_players
        new_state = self.play(move, self.current_player, test)
        new_state.turn = turn
        new_state.current_player = current_player
        new_state.player_controllers = self.player_controllers
        return new_state

    def _won(self, winner):
        self.winner = winner
        if not self.test:
            print "\nPlayer " + str(winner) + " won!\n"

    def is_valid_move(self, move, moving_player):
        if move[0] < 0 or move[1] < 0 or move[1] >= self.gridSize[0] or move[0] >= self.gridSize[1]:
            return False
        if self.grid[move[0]][move[1]].value == 0 or self.grid[move[0]][move[1]].player == moving_player:
            return True
        return False

    def register_controller(self, controller, player):
        if player >= self.total_players:
            raise UnknownPlayerException("Player " + str(player) + " tried to register while there are only " + str(
                self.total_players) + " players.")
        self.player_controllers[player] = controller

    def run(self):
        while self.winner < 0:
            if self.player_controllers[self.current_player] == 0:
                print ""
                print self
                move = tuple(map(int, raw_input(
                    "\nTurn for player " + str(
                        self.current_player) + ": Enter coordinates from the top left corner:\n").split()))
                self = self.move(move)
            else:
                print ""
                print self
                move = self.player_controllers[self.current_player].make_move(self)
                undo = self
                self = self.move(move)
                self.undo = undo

    def evaluate(self):
        # TODO: Update this evaluation with proper scoring for corner and edge values
        # return 2 * self.player_points[self.current_player] - sum(self.player_points)
        return 2 * self.player_counts[self.current_player] - sum(self.player_counts)

    def random_move(self):
        return random.choice(self.all_moves())

    def all_moves(self):
        l = []
        for j in range(len(self.grid)):
            for i in range(len(self.grid[0])):
                if self.grid[j][i].player == self.current_player or self.grid[j][i].value == 0:
                    l += [(j, i)]
        return l

    def __str__(self):
        string = ""
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j].value == 0:
                    pass
                elif self.grid[i][j].player == 0:
                    string += b_colors.FAIL
                elif self.grid[i][j].player == 1:
                    string += b_colors.OK_GREEN
                elif self.grid[i][j].player == 2:
                    string += b_colors.OK_BLUE
                elif self.grid[i][j].player == 3:
                    string += b_colors.WARNING
                elif self.grid[i][j].player == 4:
                    string += b_colors.UNDERLINE
                elif self.grid[i][j].player == 5:
                    string += b_colors.BOLD
                elif self.grid[i][j].player == 6:
                    string += b_colors.HEADER

                string += str(self.grid[i][j].value) + " " + b_colors.ENDC
            string += "\n"
        return string

    def deep_print(self):
        string = "\nGrid Size: " + str(self.gridSize) + "\nTotal Players: " + str(
            self.total_players) + "\nPlayer Scores: " + str(self.player_counts) + "\nPlayer Points:" + str(
            self.player_points) + "\nTurn No.: " + str(
            self.turn) + "\nCurrent Player: " + str(self.current_player) + "\n\nGrid:\n\n"
        string += self.__str__()
        print string


class Square:
    def __init__(self, grid_size, position, player, value):
        self.player = player
        self.value = value
        self.grid_size = grid_size
        self.position = position
        self.on_corner = self.is_on_corner()
        self.on_edge = self.is_on_edge()
        self.on_middle = self.is_on_middle()

    def is_empty(self):
        if self.value == 0:
            return True
        else:
            return False

    def is_on_corner(self):
        if self.position == (0, 0) or self.position == (self.grid_size[0] - 1, 0) or self.position == (
                0, self.grid_size[1] - 1) or self.position == (self.grid_size[0] - 1, self.grid_size[0] - 1):
            return True
        else:
            return False

    def is_on_edge(self):
        if (self.position[0] == 0 or self.position[1] == 0 or self.position[0] == self.grid_size[0] - 1 or
                    self.position[1] == self.grid_size[1] - 1) and not self.is_on_corner():
            return True
        else:
            return False

    def is_on_middle(self):
        if not self.is_on_corner() and not self.is_on_edge():
            return True
        else:
            return False

    def is_full(self):
        if self.on_corner and self.value >= 1:
            return True
        if self.on_edge and self.value >= 2:
            return True
        if self.value >= 3:
            return True
        return False

    def overflown(self):
        if self.on_corner and self.value >= 2:
            return True
        if self.on_edge and self.value >= 3:
            return True
        if self.value >= 4:
            return True
        return False

    def __str__(self):
        string = ""
        if self.value == 0:
            pass
        elif self.player == 0:
            string += b_colors.FAIL
        elif self.player == 1:
            string += b_colors.OK_GREEN
        elif self.player == 2:
            string += b_colors.OK_BLUE
        elif self.player == 3:
            string += b_colors.WARNING
        elif self.player == 4:
            string += b_colors.UNDERLINE
        elif self.player == 5:
            string += b_colors.BOLD
        elif self.player == 6:
            string += b_colors.HEADER

        string += str(self.value) + b_colors.ENDC

        return string


class Controller:
    def make_move(self, state):
        '''
        :param state: The Game State object to play the move on
        :return: Crate a move tuple indicating the (row,column) for the move
        '''
        raise NotImplementedError("The make_move() method must be implemented.")


class b_colors:
    HEADER = '\033[95m'
    OK_BLUE = '\033[94m'
    OK_GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class InvalidMoveException(Exception):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return repr(self.expression)


class UnknownPlayerException(Exception):
    def __init__(self, expression):
        self.expression = expression

    def __str__(self):
        return repr(self.expression)

