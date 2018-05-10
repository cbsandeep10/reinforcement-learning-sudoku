"""
Reinforcement learning Sudoku example.
value   action  check   reward
0   0   NA  -0.1
0   1   0   0
0   1   1   -1
1   0   NA  0
1   1   NA  -0.1

This script is the environment part of this example. The RL is in RL_brain.py.
"""

import numpy as np
import time
import sys
import checker

if sys.version_info.major == 2:
    import Tkinter as tk
else:
    import tkinter as tk

UNIT = 40  # pixels
MAZE_H = 9  # grid height
MAZE_W = 9  # grid width


class Maze(tk.Tk, object):
    def __init__(self, start):
        super(Maze, self).__init__()
        self.action_space = list(range(10))
        self.start = start
        self.state = [-1, -1, -1]
        self.n_actions = len(self.action_space)
        self.title('Sudoku')
        self.geometry('{0}x{1}'.format(MAZE_H * UNIT, MAZE_H * UNIT))
        self.values = np.copy(start)
        self._build_maze()

    def _build_maze(self):
        self.canvas = tk.Canvas(self, bg='white',
                                height=MAZE_H * UNIT,
                                width=MAZE_W * UNIT)

        # create grids
        for c in range(0, MAZE_W * UNIT, UNIT):
            x0, y0, x1, y1 = c, 0, c, MAZE_H * UNIT
            self.canvas.create_line(x0, y0, x1, y1)
        for r in range(0, MAZE_H * UNIT, UNIT):
            x0, y0, x1, y1 = 0, r, MAZE_H * UNIT, r
            self.canvas.create_line(x0, y0, x1, y1)

        # fill
        self.fill()

        # create origin
        origin = np.array([20, 20])
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15)

        # pack all
        self.canvas.pack()

    def fill(self):
        for i in range(len(self.start[0])):
            for j in range(len(self.start[0])):
                text = self.start[i][j]
                if text == 0:
                    text = "_"
                self.canvas.delete("num-" + str(i) + str(j))
                self.canvas.create_text(
                    UNIT / 2 + j * UNIT, UNIT / 2 + i * UNIT, font=("Purisa", 16),
                    text=text,
                    tag="num-" + str(i) + str(j))

    def reset(self):
        self.update()
        time.sleep(0.5)
        self.canvas.delete(self.rect)
        origin = np.array([20, 20])
        self.values = np.copy(self.start)
        self.fill()
        self.rect = self.canvas.create_rectangle(
            origin[0] - 15, origin[1] - 15,
            origin[0] + 15, origin[1] + 15)
        # time.sleep(10)
        self.state = [-1, -1, -1]
        return self.state

    def step(self, action):
        s = self.state
        base_action = np.array([0, 0])
        if s[1] == MAZE_W - 1:
            # move down
            base_action[0] -= MAZE_W * UNIT
            base_action[1] += UNIT
            next_state = [s[0] + 1, 0, action]
        elif s[0] == -1 and s[1] == -1:
            next_state = [0, 0, action]
        else:
            # move right
            base_action[0] += UNIT
            next_state = [s[0], s[1] + 1, action]

        self.canvas.move(self.rect, base_action[0], base_action[1])  # move agent
        self.state = next_state
        s_ = next_state
        print(s_)

        # reward function
        if next_state[0] < 9 and next_state[1] < 9:
            if self.values[next_state[0], next_state[1]] == 0:
                if action == 0:
                    reward = -0.1
                    done = False
                else:
                    self.values[next_state[0], next_state[1]] = action
                    self.canvas.delete("num-" + str(next_state[0]) + str(next_state[1]))
                    self.canvas.create_text(
                        UNIT / 2 + next_state[1] * UNIT, UNIT / 2 + next_state[0] * UNIT,
                        font=("Purisa", 16), text=action,
                        tag="num-" + str(next_state[0]) + str(next_state[1]))
                    if checker.check_sudoku(self.values):
                        reward = 0
                        done = False
                    else:
                        reward = -1
                        done = True
                        s_ = 'terminal'
            else:
                if action == 0:
                    reward = 0
                    done = False
                else:
                    reward = -0.1
                    done = False
        else:
            if not checker.check_sudoku(self.values):
                reward = -1
                done = True
                s_ = 'terminal'
            else:
                reward = 1
                done = True
                s_ = 'terminal'

        return s_, reward, done

    def render(self):
        time.sleep(0.1)
        self.update()


def update():
    for t in range(10):
        s = env.reset()
        while True:
            env.render()
            a = 1
            s, r, done = env.step(a)
            if done:
                break
