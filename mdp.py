import numpy as np
from game import Game

class Mdp():
    def __init__(self, game, gamma=0.9, epsilon=0.01):
        self.game = game
        self.gamma = gamma
        self.epsilon = epsilon
        self.nb_states = game.size[0] * game.size[1]
        self.rewards = (game.map).flatten()
        self.values = np.zeros(self.nb_states)

    def allowed_actions(self, state):
        state_pos = (state // self.game.size[1], state % self.game.size[1])
        actions = []
        if state_pos[0] > 0:
            actions.append(0)
        if state_pos[1] < self.game.size[1] - 1:
            actions.append(1)
        if state_pos[0] < self.game.size[0] - 1:
            actions.append(2)
        if state_pos[1] > 0:
            actions.append(3)
        return actions

    def transition_probability(self, state, action, next_state):
        state_pos = (state // self.game.size[1], state % self.game.size[1])
        next_state_pos = (next_state // self.game.size[1], next_state % self.game.size[1])
        allowed = self.allowed_actions(state)
        if state_pos[0] == 0:
            if action == 0:
                return 0
            if action == 1 and action in allowed:
                if next_state_pos == (state_pos[0], state_pos[1] + 1):
                    return 0.9
                if next_state_pos == (state_pos[0] + 1, state_pos[1] + 1):
                    return 0.1
                else:
                    return 0
            if action == 3 and action in allowed:
                if next_state_pos == (state_pos[0], state_pos[1] - 1):
                    return 0.9
                if next_state_pos == (state_pos[0] + 1, state_pos[1] - 1):
                    return 0.1
                else:
                    return 0
        if state_pos[0] == self.game.size[0] - 1:
            if action == 2:
                return 0
            if action == 1 and action in allowed:
                if next_state_pos == (state_pos[0], state_pos[1] + 1):
                    return 0.9
                if next_state_pos == (state_pos[0] - 1, state_pos[1] + 1):
                    return 0.1
                else:
                    return 0
            if action == 3 and action in allowed:
                if next_state_pos == (state_pos[0], state_pos[1] - 1):
                    return 0.9
                if next_state_pos == (state_pos[0] - 1, state_pos[1] - 1):
                    return 0.1
                else:
                    return 0
        if state_pos[1] == 0:
            if action == 3:
                return 0
            if action == 0 and action in allowed:
                if next_state_pos == (state_pos[0] - 1, state_pos[1]):
                    return 0.9
                if next_state_pos == (state_pos[0] - 1, state_pos[1] + 1):
                    return 0.1
                else:
                    return 0
            if action == 2 and action in allowed:
                if next_state_pos == (state_pos[0] + 1, state_pos[1]):
                    return 0.9
                if next_state_pos == (state_pos[0] + 1, state_pos[1] + 1):
                    return 0.1
                else:
                    return 0
        if state_pos[1] == self.game.size[1] - 1:
            if action == 1:
                return 0
            if action == 0 and action in allowed:
                if next_state_pos == (state_pos[0] - 1, state_pos[1]):
                    return 0.9
                if next_state_pos == (state_pos[0] - 1, state_pos[1] - 1):
                    return 0.1
                else:
                    return 0
            if action == 2 and action in allowed:
                if next_state_pos == (state_pos[0] + 1, state_pos[1]):
                    return 0.9
                if next_state_pos == (state_pos[0] + 1, state_pos[1] - 1):
                    return 0.1
                else:
                    return 0

        if action == 0:
            if next_state_pos == (state_pos[0] - 1, state_pos[1]):
                return 0.8
            if next_state_pos == (state_pos[0] - 1, state_pos[1] + 1):
                return 0.1
            if next_state_pos == (state_pos[0] - 1, state_pos[1] - 1):
                return 0.1
        elif action == 1:
            if next_state_pos == (state_pos[0], state_pos[1] + 1):
                return 0.8
            if next_state_pos == (state_pos[0] - 1, state_pos[1] + 1):
                return 0.1
            if next_state_pos == (state_pos[0] + 1, state_pos[1] + 1):
                return 0.1
        elif action == 2:
            if next_state_pos == (state_pos[0] + 1, state_pos[1]):
                return 0.8
            if next_state_pos == (state_pos[0] + 1, state_pos[1] + 1):
                return 0.1
            if next_state_pos == (state_pos[0] + 1, state_pos[1] - 1):
                return 0.1
        elif action == 3:
            if next_state_pos == (state_pos[0], state_pos[1] - 1):
                return 0.8
            if next_state_pos == (state_pos[0] - 1, state_pos[1] - 1):
                return 0.1
            if next_state_pos == (state_pos[0] + 1, state_pos[1] - 1):
                return 0.1
        return 0

    def one_iteration(self):
        delta = 0
        for state in range(self.nb_states):
            old_value = self.values[state]
            allowed = self.allowed_actions(state)
            values_dict = {action: 0 for action in allowed}
            for action in allowed:
                for next_state in range(self.nb_states):
                    values_dict[action] += self.transition_probability(state, action, next_state) * self.values[next_state]
            new_value = self.rewards[state] + self.gamma * max(values_dict.values())
            self.values[state] = new_value
            delta = max(delta, abs(old_value - new_value))
        return delta

    def get_policy(self):
        policy = np.zeros(self.nb_states, dtype=int)
        for state in range(self.nb_states):
            allowed = self.allowed_actions(state)
            values_dict = {action: 0 for action in allowed}
            for action in allowed:
                for next_state in range(self.nb_states):
                    values_dict[action] += self.transition_probability(state, action, next_state) * self.values[next_state]
            policy[state] = max(values_dict, key=values_dict.get)
        return policy

    def value_iteration(self):
        epoch = 0
        delta = self.one_iteration()
        delta_history = [delta]
        while delta > self.epsilon:
            epoch += 1
            delta = self.one_iteration()
            delta_history.append(delta)
        self.policy = self.get_policy()
    
    def get_robot_path(self):
        pos = self.game.robot_pos
        path = [pos]
        while pos != self.game.goal_pos:
            action = self.policy[pos[0] * self.game.size[1] + pos[1]]
            pos = self.game.likely_next_state(pos, action)
            path.append(pos)
        return path

if __name__ == '__main__':
    g = Game((5,5), (4,0), (4,4), 10, [(4,1), (4,2), (4,3), (3,1), (3,2), (3,3)], -5, [(0,4)], 5)
    m = Mdp(g, gamma=0.9, epsilon=0.01)
    m.value_iteration()
    print(g.map)
    print(m.policy.reshape(g.size))