"""
Sudoku solver - Reinforcement Learning
"""
import numpy as np
import pandas as pd
import time

from Sudoku import Maze
from Rl_brain import QLearningTable
import checker

np.random.seed(2)  # reproducible


def update():
    for episode in range(360):
        # initial observation
        observation = env.reset()
        # print(observation)

        while True:
            # fresh env
            env.render()

            # RL choose action based on observation
            action = RL.choose_action(str(observation))
            # print(action)

            # RL take action and get next observation and reward
            observation_, reward, done = env.step(action)

            # RL learn from this transition
            RL.learn(str(observation), action, reward, str(observation_))

            # swap observation
            observation = observation_

            # break while loop when end of this episode
            if done:
                print("break")
                break

    # end of game
    print('game over')
    env.destroy()


if __name__ == "__main__":
    start = np.array([[2, 9, 0, 0, 0, 0, 0, 7, 0],
                      [3, 0, 6, 0, 0, 8, 4, 0, 0],
                      [8, 0, 0, 0, 4, 0, 0, 0, 2],
                      [0, 2, 0, 0, 3, 1, 0, 0, 7],
                      [0, 0, 0, 0, 8, 0, 0, 0, 0],
                      [1, 0, 0, 9, 5, 0, 0, 6, 0],
                      [7, 0, 0, 0, 9, 0, 0, 0, 1],
                      [0, 0, 1, 2, 0, 0, 3, 0, 6],
                      [0, 3, 0, 0, 0, 0, 0, 5, 9]])
    # print(checker.check_sudoku(start))
    env = Maze(start)
    RL = QLearningTable(actions=list(range(env.n_actions)))

    env.after(100, update)
    env.mainloop()
