import random
import time
import pygame
import math
from copy import deepcopy
import numpy as np


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
    def __init__(self, position, depth=3):
        super().__init__(position)
        self.depth = 3

    def play(self, env, move):
        env_copy = deepcopy(env)
        possible = env.topPosition >= 0
        indices = []
        v = -np.inf
        alpha = -np.inf
        beta = np.inf

        for i, p in enumerate(possible):
            if p: indices.append(i)

        for i in indices:
            env_copy = deepcopy(env)
            self.simulateMove(env_copy, self.position, i)
            score = self.minimax(env_copy, i, self.depth - 1, False, alpha, beta)

            if score > v:
                v = score
                best_move = i

        move[:] = [best_move]

    def minimax(self, env, move, depth, maximizing_player, alpha, beta):
        if env.gameOver(move, self.position):
            return np.inf

        if env.gameOver(move, self.opponent.position):
            return -np.inf

        if depth == 0:
            return self.evaluate(env)

        possible = env.topPosition >= 0
        indices = []

        for i, p in enumerate(possible):
            if p: indices.append(i)

        if maximizing_player:
            best_score = -np.inf
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, self.position, i)
                score = self.minimax(env_copy, i, depth - 1, False, alpha, beta)
                best_score = max(best_score, score)
                alpha = max(alpha, best_score)
                if alpha >= beta:
                    break

            return best_score

        else:
            best_score = np.inf
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, self.opponent.position, i)
                score = self.minimax(env_copy, i, depth - 1, True, alpha, beta)
                best_score = min(best_score, score)
                beta = min(beta, best_score)
                if alpha >= beta:
                    break
            return best_score

    def evaluate(self, env):

        w = [[6, 8, 10, 18, 10, 8, 6],
             [8, 12, 16, 20, 16, 12, 8],
             [10, 16, 22, 26, 22, 16, 10],
             [10, 16, 22, 26, 22, 16, 10],
             [8, 12, 16, 20, 16, 12, 8],
             [6, 8, 10, 18, 10, 8, 6]]

        score = 0

        for i in range(6):
            for j in range(7):
                if env.board[i][j] == self.position:
                    score += w[i][j]
                elif env.board[i][j] == self.opponent.position:
                    score -= w[i][j]

        return score

    def simulateMove(self, env, player, move):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1


class minimaxAI(connect4Player):
    def __init__(self, position, depth=3):
        super().__init__(position)
        self.depth = 3

    def play(self, env, move):
        env_copy = deepcopy(env)
        possible = env.topPosition >= 0
        indices = []
        v = -np.inf

        for i, p in enumerate(possible):
            if p: indices.append(i)

        for i in indices:
            env_copy = deepcopy(env)
            self.simulateMove(env_copy, self.position, i)
            score = self.minimax(env_copy, i, self.depth - 1, False)

            if score > v:
                v = score
                best_move = i

        move[:] = [best_move]

    def minimax(self, env, move, depth, maximizing_player):
        if env.gameOver(move, self.position):
            return np.inf

        if env.gameOver(move, self.opponent.position):
            return -np.inf

        if depth == 0:
            return self.evaluate(env)

        possible = env.topPosition >= 0
        indices = []

        for i, p in enumerate(possible):
            if p: indices.append(i)

        if maximizing_player:
            best_score = -np.inf
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, self.position, i)
                score = self.minimax(env_copy, i, depth - 1, False)
                best_score = max(best_score, score)
            return best_score

        else:
            best_score = np.inf
            for i in indices:
                env_copy = deepcopy(env)
                self.simulateMove(env_copy, self.opponent.position, i)
                score = self.minimax(env_copy, i, depth - 1, True)
                best_score = min(best_score, score)
            return best_score

    def evaluate(self, env):

        w = [[6, 8, 10, 18, 10, 8, 6],
             [8, 12, 16, 20, 16, 12, 8],
             [10, 16, 22, 26, 22, 16, 10],
             [10, 16, 22, 26, 22, 16, 10],
             [8, 12, 16, 20, 16, 12, 8],
             [6, 8, 10, 18, 10, 8, 6]]

        score = 0

        for i in range(6):
            for j in range(7):
                if env.board[i][j] == self.position:
                    score += w[i][j]
                elif env.board[i][j] == self.opponent.position:
                    score -= w[i][j]

        return score

    def simulateMove(self, env, player, move):
        env.board[env.topPosition[move]][move] = player
        env.topPosition[move] -= 1


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
