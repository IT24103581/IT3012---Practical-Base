# agent.py
import random

class GreedyGridAgent:
    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    def sense_and_act(self, percept: dict) -> str:
        if percept['food_here']:
            return 'Right'

        if percept['wall_ahead']:
            return 'Left'

        return 'Right'

class ModelBasedAgent:
    def __init__(self):
        self.last_percept = None
        self.last_action = None
        self.visited_cells = set()
        self.relative_pos = (0, 0)
        self.action_cycle = ['Left', 'Right', 'Up', 'Down']
        self.cycle_index = 0

    def sense_and_act(self, percept: dict) -> str:
        if self.last_action is not None and not percept['wall_ahead']:
            self._update_relative_pos(self.last_action)

        self.visited_cells.add(self.relative_pos)

        repeated_situation = (self.last_percept == percept)

        if percept['food_here']:
            action = 'Right'
        elif percept['wall_ahead']:
            if repeated_situation:
                self.cycle_index = (self.cycle_index + 1) % len(self.action_cycle)
            action = self.action_cycle[self.cycle_index]
        else:
            candidate = self._forward_cell(self.action_cycle[self.cycle_index])
            if candidate in self.visited_cells:
                self.cycle_index = (self.cycle_index + 1) % len(self.action_cycle)
            action = self.action_cycle[self.cycle_index]

        self.last_percept = dict(percept)
        self.last_action = action
        return action

    def _update_relative_pos(self, action):
        x, y = self.relative_pos
        if action == 'Up':
            self.relative_pos = (x, y + 1)
        elif action == 'Down':
            self.relative_pos = (x, y - 1)
        elif action == 'Left':
            self.relative_pos = (x - 1, y)
        elif action == 'Right':
            self.relative_pos = (x + 1, y)

    def _forward_cell(self, action):
        x, y = self.relative_pos
        if action == 'Up':
            return (x, y + 1)
        elif action == 'Down':
            return (x, y - 1)
        elif action == 'Left':
            return (x - 1, y)
        elif action == 'Right':
            return (x + 1, y)
        return self.relative_pos        