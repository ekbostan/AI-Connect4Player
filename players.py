import random
import sys
import time
import pygame
import math
import numpy as np
from copy import deepcopy

counter = 0
first_move = True

class connect4Player(object):
    def __init__(self, position, seed=0):
        self.position = position
        self.opponent = None
        self.seed = seed
        random.seed(seed)

    def play(self, env, move):
        move = [-1]


class human(connect4Player):

    def play(self, env, move):
        move[:] = [int(input('Select next move: '))]
        while True:
            if int(move[0]) >= 0 and int(move[0]) <= 6 and env.topPosition[int(move[0])] >= 0:
                break
            move[:] = [int(input('Index invalid. Select next move: '))]


class human2(connect4Player):

    def play(self, env, move):
        done = False
        while (not done):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.MOUSEMOTION:
                    pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARESIZE))
                    posx = event.pos[0]
                    if self.position == 1:
                        pygame.draw.circle(screen, RED, (posx, int(SQUARESIZE / 2)), RADIUS)
                    else:
                        pygame.draw.circle(screen, YELLOW, (posx, int(SQUARESIZE / 2)), RADIUS)
                pygame.display.update()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    posx = event.pos[0]
                    col = int(math.floor(posx / SQUARESIZE))
                    move[:] = [col]
                    done = True


class randomAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        move[:] = [random.choice(indices)]


class stupidAI(connect4Player):

    def play(self, env, move):
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        if 3 in indices:
            move[:] = [3]
        elif 2 in indices:
            move[:] = [2]
        elif 1 in indices:
            move[:] = [1]
        elif 5 in indices:
            move[:] = [5]
        elif 6 in indices:
            move[:] = [6]
        else:
            move[:] = [0]


class alphaBetaAI(connect4Player):

    def play(self, env, move):
        # Find legal moves
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        # Calculate the minimax value for each move
        vs = np.zeros(7)
        for i in indices:
            env_copy = deepcopy(env)
            self.simulateMove(env_copy, i, self.position)
            vs[i] = self.minimax(env_copy, self.depth - 1, -np.inf, np.inf, False)
        # Choose the move with the highest minimax value
        move[:] = [np.argmax(vs)]

    def minimax(self, env, depth, alpha, beta, maximizingPlayer):
        switch = {1: 2, 2: 1}
        if depth == 0 or env.gameOver(None, None):
            return self.evaluate(env)
        if maximizingPlayer:
            value = -np.inf
            possible = env.topPosition >= 0
            indices = []
            for i, p in enumerate(possible):
                if p: indices.append(i)
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, i, self.position)
                value = max(value, self.minimax(env_copy, depth - 1, alpha, beta, False))
                alpha = max(alpha, value)
                if beta <= alpha:
                    break
            return value
        else:
            value = np.inf
            possible = env.topPosition >= 0
            indices = []
            for i, p in enumerate(possible):
                if p: indices.append(i)
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, i, switch[self.position])
                value = min(value, self.minimax(env_copy, depth - 1, alpha, beta, True))
                beta = min(beta, value)
                if beta <= alpha:
                    break
            return value

    def evaluate(self, env):
        switch = {1: 2, 2: 1}
        if env.gameOver(None, None):
            if env.winner == self.position:
                return 100000000
            elif env.winner == switch[self.position]:
                return -100000000
            else:
                return 0
        else:
            score = 0
            for i in range(env.rows):
                for j in range(env.cols):
                    if env.board[i][j] == self.position:
                        # Check horizontally
                        if j <= env.cols - 4:
                            if env.board[i][j + 1] == self.position and env.board[i][j + 2] == self.position and \
                                    env.board[i][j + 3] == self.position:
                                score += 100
                            elif env.board[i][j + 1] == self.position and env.board[i][j + 2] == self.position:
                                score += 10
                            elif env.board[i][j + 1] == self.position:
                                score += 5
                        # Check vertically
                        if i <= env.rows - 4:
                            if env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position and \
                                    env.board[i + 3][j] == self.position:
                                score += 100
                            elif env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position:
                                score += 10
                            elif env.board[i + 1][j] == self.position:
                                score += 5
                        # Check diagonally (positive slope)
                        if i <= env.rows - 4 and j <= env.cols - 4:
                            if env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position and \
                                    env.board[i + 3][j + 3] == self.position:
                                score += 100
                            elif env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position:
                                score += 10
                            elif env.board[i + 1][j + 1] == self.position:
                                score += 5
                        # Check diagonally (negative slope)
                        if i >= 3 and j <= env.cols - 4:
                            if env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position and \
                                    env.board[i - 3][j + 3] == self.position:
                                score += 100
                            elif env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position:
                                score += 10
                            elif env.board[i - 1][j + 1] == self.position:
                                score += 5
                    elif env.board[i][j] == switch[self.position]:
                        # Check horizontally
                        if j <= env.cols - 4:
                            if env.board[i][j + 1] == switch[self.position] and env.board[i][j + 2] == switch[
                                self.position] and env.board[i][j + 3] == switch[self.position]:
                                score -= 5
                            elif env.board[i][j + 1] == switch[self.position] and env.board[i][j + 2] == switch[
                                self.position]:
                                score -= 4
                            elif env.board[i][j + 1] == switch[self.position]:
                                score -= 2
                        # Check vertically
                        if i <= env.rows - 4:
                            if env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position and \
                                    env.board[i + 3][j] == self.position:
                                score -= 5
                            elif env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position:
                                score -= 4
                            elif env.board[i + 1][j] == self.position:
                                score -= 2
                        # Check diagonally (positive slope)
                        if i <= env.rows - 4 and j <= env.cols - 4:
                            if env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position and \
                                    env.board[i + 3][j + 3] == self.position:
                                score -= 5
                            elif env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position:
                                score -= 4
                            elif env.board[i + 1][j + 1] == self.position:
                                score -= 2
                        # Check diagonally (negative slope)
                        if i >= 3 and j <= env.cols - 4:
                            if env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position and \
                                    env.board[i - 3][j + 3] == self.position:
                                score -= 5
                            elif env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position:
                                score -= 4
                            elif env.board[i - 1][j + 1] == self.position:
                                score -= 2
        return score

    def simulateMove(self, env, move, player):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1
        env.history[0].append(move)


class minimaxAI(connect4Player):

    def play(self, env, move):
        env_copy = deepcopy(env)
        possible = env.topPosition >= 0
        indices = []
        for i, p in enumerate(possible):
            if p: indices.append(i)
        # Calculate the minimax value for each move

        val = 0
        index = 0
        move[:] = [3]
        for i in indices:
            self.simulateMove(env_copy, self.position, i)
            new_val = self.evaluate(env_copy)
            #ove[:] = [3]
            if new_val > val:
                val = new_val
                index = i
                move[:] = [index]
    #         if new_val > val:
    #             move[:] =[i]
    #             val = new_val
    #     # Choose the move with the highest minimax value
    #
    # def minimax(self, env, depth, first_move, maximizingplayer):
    #     switch = {1: 2, 2: 1}
    #     move = first_move
    #     player = self.position
    #     opp = self.position.opponent
    #
    #     self.simulateMove(env, move, player)
    #     if depth == 0 or env.gameOver(move, player) or env.gameOver(move, opp):
    #         if env.gameOver(move, player) or env.gameOver(move, opp):
    #             if env.gameover(move, player):
    #                 return 10000000000000
    #             elif env.gameover(move, opp):
    #                 return -10000000000000
    #             else:
    #                 return 0
    #         else:
    #             return self.evaluate(env)
    #     if maximizingplayer:
    #         value = -np.inf
    #         possible = env.topPosition >= 0
    #         indices = []
    #         for i, p in enumerate(possible):
    #             if p: indices.append(i)
    #         for i in indices:
    #
    #             self.simulateMove(env, i, self.position)
    #             value = max(value, self.minimax(env, depth - 1,i, False))
    #         return value
    #
    #     else:
    #         value = np.inf
    #         possible = env.topPosition >= 0
    #         indices = []
    #         for i, p in enumerate(possible):
    #             if p: indices.append(i)
    #         for i in indices:
    #
    #             self.simulateMove(env, i, switch[self.position])
    #             value = min(value, self.minimax(env, depth - 1,i,True))
    #         return value

    # def evaluate(self, env):
    #     switch = {1: 2, 2: 1}
    #     score = 0
    #     for i in range(ROW_COUNT):
    #         if env.board[3][i] == self.position:
    #             score += 3
    #         elif env.board[3][i] == switch[self.position]:
    #             score -= 3
    #     for i in range(ROW_COUNT):
    #         for j in range(COLUMN_COUNT):
    #             if env.board[i][j] == self.position:
    #                 # Check horizontally
    #                 if j <= COLUMN_COUNT - 4:
    #                     if env.board[i][j + 1] == self.position and env.board[i][j + 2] == self.position and \
    #                             env.board[i][j + 3] == self.position:
    #                         score += 100
    #                     elif env.board[i][j + 1] == self.position and env.board[i][j + 2] == self.position:
    #                         score += 10
    #                     elif env.board[i][j + 1] == self.position:
    #                         score += 2
    #                     # Check vertically
    #                 if i <= ROW_COUNT - 3:
    #                     if env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position and \
    #                             env.board[i + 3][j] == self.position:
    #                         score += 100
    #                     elif env.board[i + 1][j] == self.position and env.board[i + 2][j] == self.position:
    #                         score += 10
    #                     elif env.board[i + 1][j] == self.position:
    #                         score += 2
    #                     # Check diagonally (positive slope)
    #                 if i <= ROW_COUNT - 3 and j <= COLUMN_COUNT - 4:
    #                     if env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position and \
    #                             env.board[i + 3][j + 3] == self.position:
    #                         score += 100
    #                     elif env.board[i + 1][j + 1] == self.position and env.board[i + 2][j + 2] == self.position:
    #                         score += 10
    #                     elif env.board[i + 1][j + 1] == self.position:
    #                         score += 2
    #                 # Check diagonally (negative slope)
    #                 if i >= 4 and j <= COLUMN_COUNT - 3:
    #                     if env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position and \
    #                             env.board[i - 3][j + 3] == self.position:
    #                         score += 100
    #                     elif env.board[i - 1][j + 1] == self.position and env.board[i - 2][j + 2] == self.position:
    #                         score += 10
    #                     elif env.board[i - 1][j + 1] == self.position:
    #                         score += 2
    #             elif env.board[i][j] == switch[self.position]:
    #                 # Check horizontally
    #                 if j <= COLUMN_COUNT - 4:
    #                     if env.board[i][j + 1] == switch[self.position] and env.board[i][j + 2] == switch[
    #                         self.position] and env.board[i][j + 3] == switch[self.position]:
    #                         score -= 100
    #                     elif env.board[i][j + 1] == switch[self.position] and env.board[i][j + 2] == switch[
    #                         self.position]:
    #                         score -= 10
    #                     elif env.board[i][j + 1] == switch[self.position]:
    #                         score -= 2
    #                 # Check vertically
    #                 if i <= ROW_COUNT - 3:
    #                     if env.board[i + 1][j] == switch[self.position] and env.board[i + 2][j] == switch[
    #                         self.position] and env.board[i + 3][j] == switch[self.position]:
    #                         score -= 100
    #                     elif env.board[i + 1][j] == switch[self.position] and env.board[i + 2][j] == switch[
    #                         self.position]:
    #                         score -= 10
    #                     elif env.board[i + 1][j] == switch[self.position]:
    #                         score -= 2
    #                 # Check diagonally (positive slope)
    #                 if i <= ROW_COUNT - 3 and j <= COLUMN_COUNT - 4:
    #                     if env.board[i + 1][j + 1] == switch[self.position] and env.board[i + 2][j + 2] == switch[
    #                         self.position] and env.board[i + 3][j + 3] == switch[self.position]:
    #                         score -= 100
    #                     elif env.board[i + 1][j + 1] == switch[self.position] and env.board[i + 2][j + 2] == switch[
    #                         self.position]:
    #                         score -= 10
    #                     elif env.board[i + 1][j + 1] == switch[self.position]:
    #                         score -= 2
    #                 # Check diagonally (negative slope)
    #                 if i >= 4 and j <= COLUMN_COUNT - 3:
    #                     if env.board[i - 1][j + 1] == switch[self.position] and env.board[i - 2][j + 2] == switch[
    #                         self.position] and env.board[i - 3][j + 3] == switch[self.position]:
    #                         score -= 100
    #                     elif env.board[i - 1][j + 1] == switch[self.position] and env.board[i - 2][j + 2] == switch[
    #                         self.position]:
    #                         score -= 10
    #                     elif env.board[i - 1][j + 1] == switch[self.position]:
    #                         score -= 2
    #
    #     return score

    def simulateMove(self, env, player, move):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1


    def evaluate(self,env):
        w = [[3, 4, 5, 7, 5, 4, 3],
             [4, 6, 8, 10, 8, 6, 4],
             [5, 8, 11, 13, 11, 8, 5],
             [5, 8, 11, 13, 11, 8, 5],
             [4, 6, 8, 10, 8, 6, 4],
             [3, 4, 5, 7, 5, 4, 3]]

        score = 0
        for i in range(6):
            for j in range(7):
                if env.board[i][j] == self.position:
                    score += w[i][j]
                elif env.board[i][j] == self.opponent.position:
                    score -= w[i][j]
        return score


SQUARESIZE = 100
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7

pygame.init()

SQUARESIZE = 100

width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 1) * SQUARESIZE

size = (width, height)

RADIUS = int(SQUARESIZE / 2 - 5)

screen = pygame.display.set_mode(size)

# /risk->7
# /hardworking->10
# /perfectionist->10
# /experienced->10
# /charismatic->8
# My dad  fits perfectly I would rate 10
# Im confident that we can start a company tomorrow so I would myself 10
