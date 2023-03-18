import numpy as np
import random

class Game:
    def __init__(self, size, robot_pos, goal_pos, goal_reward, obstacles_pos, obstacle_reward, firecamps_pos, firecamp_reward):
        self.size = size
        self.robot_pos = robot_pos
        self.goal_pos = goal_pos
        self.obstacles_pos = obstacles_pos
        self.firecamps_pos = firecamps_pos
        self.map = np.zeros(size, dtype=int)
        self.map[goal_pos] = goal_reward
        self.game_won = False
        for obstacle in obstacles_pos:
            self.map[obstacle] = obstacle_reward
        for firecamp in firecamps_pos:
            self.map[firecamp] = firecamp_reward

    def move(self, action):
        # 0 = up, 1 = right, 2 = down, 3 = left
        # /!\ doesn't check if action is valid
        # choses move according to probabilities given
        has_moved = False
        if (self.robot_pos[0] == 0) or (self.robot_pos[0] == self.size[0] - 1) or (self.robot_pos[1] == 0) or (self.robot_pos[1] == self.size[1] - 1):
            if self.robot_pos[0] == 0:
                if action == 1:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0], self.robot_pos[1] + 1)
                    else:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] + 1)
                    has_moved = True
                elif action == 3:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0], self.robot_pos[1] - 1)
                    else:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] - 1)
                    has_moved = True
            if self.robot_pos[0] == self.size[0] - 1:
                if action == 1:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0], self.robot_pos[1] + 1)
                    else:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] + 1)
                    has_moved = True
                elif action == 3:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0], self.robot_pos[1] - 1)
                    else:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] - 1)
                    has_moved = True
            if self.robot_pos[1] == 0:
                if action == 0:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1])
                    else:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] + 1)
                    has_moved = True
                elif action == 2:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1])
                    else:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] + 1)
                    has_moved = True
            if self.robot_pos[1] == self.size[1] - 1:
                if action == 0:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1])
                    else:
                        self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] - 1)
                    has_moved = True
                elif action == 2:
                    if random.random() < 0.9:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1])
                    else:
                        self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] - 1)
                    has_moved = True
        if (has_moved == False):
            if action == 0:
                if random.random() < 0.1:
                    self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] - 1)
                elif random.random() < 0.2:
                    self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] + 1)
                else:
                    self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1])
            elif action == 1:
                if random.random() < 0.1:
                    self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] + 1)
                elif random.random() < 0.2:
                    self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] + 1)
                else:
                    self.robot_pos = (self.robot_pos[0], self.robot_pos[1] + 1)
            elif action == 2:
                if random.random() < 0.1:
                    self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] + 1)
                elif random.random() < 0.2:
                    self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] - 1)
                else:
                    self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1])
            elif action == 3:
                if random.random() < 0.1:
                    self.robot_pos = (self.robot_pos[0] + 1, self.robot_pos[1] - 1)
                elif random.random() < 0.2:
                    self.robot_pos = (self.robot_pos[0] - 1, self.robot_pos[1] - 1)
                else:
                    self.robot_pos = (self.robot_pos[0], self.robot_pos[1] - 1)
        if self.robot_pos == self.goal_pos:
            self.game_won = True
    
    def get_reward(self, pos):
        return self.map[pos]
    
    def debug_robot_pos(self):
        debug_map = np.zeros(self.size, dtype=str)
        debug_map[self.robot_pos] = "x"
        print(debug_map)
    

if __name__ == "__main__":  
    g = Game((5,5), (0,0), (4,4), 10, [(1,1), (2,2)], -5, [(3,3)], 5)
    print(g.map)
    g.debug_robot_pos()
    g.move(1)
    g.debug_robot_pos()
    g.move(2)
    g.debug_robot_pos()
    g.move(2)
    g.debug_robot_pos()
    g.move(3)
    g.debug_robot_pos()
