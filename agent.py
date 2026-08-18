# agent.py
import random
from collections import deque
import heapq

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

class SearchAgent:

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

    def get_neighbors(self, position, walls, grid_size):
        x, y = position
        width, height = grid_size

        moves = [
            ((x, y + 1), 'Up'),
            ((x, y - 1), 'Down'),
            ((x - 1, y), 'Left'),
            ((x + 1, y), 'Right')
        ]

        neighbors = []

        for new_pos, action in moves:
            nx, ny = new_pos

            if (
                0 <= nx < width
                and 0 <= ny < height
                and new_pos not in walls
            ):
                neighbors.append((new_pos, action))

        return neighbors

    def reconstruct_path(self, parent, start, goal):
        path = []
        current = goal

        while current != start:
            previous, action = parent[current]
            path.append(action)
            current = previous

        path.reverse()
        return path

    def bfs_search(self, start, goal, walls, grid_size):
        if start == goal:
            return []

        frontier = deque([start])
        reached = {start}
        parent = {}

        while frontier:
            current = frontier.popleft()

            for next_pos, action in self.get_neighbors(
                current, walls, grid_size
            ):
                if next_pos not in reached:
                    reached.add(next_pos)
                    parent[next_pos] = (current, action)

                    if next_pos == goal:
                        return self.reconstruct_path(
                            parent, start, goal
                        )

                    frontier.append(next_pos)

        return None

    def dfs_search(self, start, goal, walls, grid_size):
        if start == goal:
            return []

        frontier = [start]
        reached = {start}
        parent = {}

        while frontier:
            current = frontier.pop()

            for next_pos, action in self.get_neighbors(
                current, walls, grid_size
            ):
                if next_pos not in reached:
                    reached.add(next_pos)
                    parent[next_pos] = (current, action)

                    if next_pos == goal:
                        return self.reconstruct_path(
                            parent, start, goal
                        )

                    frontier.append(next_pos)

        return None

    def ucs_search(self, start, goal, walls, grid_size):
        if start == goal:
            return []

        frontier = []
        heapq.heappush(frontier, (0, start))

        reached = {start: 0}
        parent = {}

        while frontier:
            cost, current = heapq.heappop(frontier)

            if current == goal:
                return self.reconstruct_path(
                    parent, start, goal
                )

            for next_pos, action in self.get_neighbors(
                current, walls, grid_size
            ):
                new_cost = cost + 1

                if (
                    next_pos not in reached
                    or new_cost < reached[next_pos]
                ):
                    reached[next_pos] = new_cost
                    parent[next_pos] = (current, action)

                    heapq.heappush(
                        frontier,
                        (new_cost, next_pos)
                    )

        return None

    def find_closest_food(self, start, food_positions):
        if not food_positions:
            return None

        return min(
            food_positions,
            key=lambda food:
                abs(food[0] - start[0]) +
                abs(food[1] - start[1])
        )


    def sense_and_act(self, percept):

        if not self.plan:

            start = tuple(percept['agent_pos'])

            food_positions = [
                tuple(food)
                for food in percept['all_food']
            ]

            if not food_positions:
                return 'Stay'

            goal = self.find_closest_food(
                start,
                food_positions
            )

            walls = {
                tuple(wall)
                for wall in percept['walls']
            }

            grid_size = percept['grid_size']

            if self.active_algo == 'BFS':
                self.plan = self.bfs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'DFS':
                self.plan = self.dfs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

            elif self.active_algo == 'UCS':
                self.plan = self.ucs_search(
                    start,
                    goal,
                    walls,
                    grid_size
                )

        if self.plan:
            return self.plan.pop(0)

        return 'Stay'    