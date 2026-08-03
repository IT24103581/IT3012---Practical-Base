# agent.py
import random

class SimpleReflexAgent:

    def sense_and_act(self, percept):

        # Rule 1
        if percept["food_here"]:
            return "Stay"

        # Rule 2
        elif not percept["wall_right"]:
            return "Right"

        # Rule 3
        elif not percept["wall_up"]:
            return "Up"

        # Rule 4
        elif not percept["wall_left"]:
            return "Left"

        # Rule 5
        else:
            return "Down"