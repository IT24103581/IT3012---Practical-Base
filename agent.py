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
        # Internal memory
        self.visited_states = set()
        self.last_percept = None
        self.last_action = None

        # Used to try different actions when stuck
        self.action_cycle = ['Left', 'Right', 'Up', 'Down']
        self.cycle_index = 0

    def sense_and_act(self, percept: dict) -> str:

        # Create a state from the current percept
        current_state = (
            percept.get('wall_ahead', False),
            percept.get('food_here', False),
            percept.get('toxin_ahead', False)
        )

        # Remember the previous state + action
        if self.last_percept is not None and self.last_action is not None:

            previous_state = (
                self.last_percept.get('wall_ahead', False),
                self.last_percept.get('food_here', False),
                self.last_percept.get('toxin_ahead', False)
            )

            self.visited_states.add(
                (previous_state, self.last_action)
            )

        # Rule 1: If food is detected, move toward it
        if percept['food_here']:
            action = 'Right'

        # Rule 2: If there is a wall ahead,
        # try an action that has not been tried
        elif percept['wall_ahead']:

            action = None

            for candidate in self.action_cycle:

                if (current_state, candidate) not in self.visited_states:
                    action = candidate
                    break

            # If every action has already been tried,
            # change the starting point in the action cycle
            if action is None:
                self.cycle_index = (
                    self.cycle_index + 1
                ) % len(self.action_cycle)

                action = self.action_cycle[self.cycle_index]

        # Rule 3: If the path is clear,
        # continue using the current preferred direction
        else:
            action = self.action_cycle[self.cycle_index]

        # Store current state and action in memory
        self.last_percept = dict(percept)
        self.last_action = action

        return action      