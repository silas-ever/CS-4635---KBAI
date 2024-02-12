from __future__ import print_function
from __future__ import unicode_literals
from __future__ import absolute_import
from __future__ import division
from random import choice

from py_search.base import Problem
from py_search.base import Node
from py_search.base import GoalNode
from py_search.uninformed import depth_first_search
from py_search.uninformed import breadth_first_search
from py_search.uninformed import iterative_deepening_search
from py_search.uninformed import iterative_sampling
from py_search.informed import best_first_search
from py_search.informed import iterative_deepening_best_first_search
from py_search.informed import widening_beam_search
from py_search.utils import compare_searches


class GuardsPrisoners:
    """
    A prisoners and guards problem, which can be used to try different search
    algorithms.
    """

    def __init__(self):
        # 0=guards left, 1=prisoners left, 3=boat location (0=left, 1=right), 4=guards right, 5=prisoners right
        self.state = (3, 3, 0, 0, 0)

    def __hash__(self):
        return hash(self.state)

    def __eq__(self, other):
        if isinstance(other, GuardsPrisoners):
            return self.state == other.state
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return "left: {} guards, {} prisoners -- boat on {} -- right: {} guards, {} prisoners".format(self.state[0],
                                                                                                      self.state[1],
                                                                                                      "left" if self.state[2] == 0 else "right",
                                                                                                      self.state[3],
                                                                                                      self.state[4])

    def copy(self):
        """
        Makes a deep copy of an GuardsPrisoners object.
        """
        new = GuardsPrisoners()
        new.state = tuple([i for i in self.state])
        return new

    def executeAction(self, action):
        """
        Executes an action to the GuardsPrisoners object.

        :param action: the action to execute
        :type action: "2g", "2p", "1g1p", "1g", "1p"
        """
        successor = list(self.state)

        # if boat on left
        if self.state[2] == 0:
            successor[2] = 1
            if action == "2g":
                successor[0] -= 2
                successor[3] += 2
            elif action == "2p":
                successor[1] -= 2
                successor[4] += 2
            elif action == "1g1p":
                successor[0] -= 1
                successor[3] += 1
                successor[1] -= 1
                successor[4] += 1
            elif action == "1g":
                successor[0] -= 1
                successor[3] += 1
            elif action == "1p":
                successor[1] -= 1
                successor[4] += 1

        # boat on right
        else:
            successor[2] = 0
            if action == "2g":
                successor[0] += 2
                successor[3] -= 2
            elif action == "2p":
                successor[1] += 2
                successor[4] -= 2
            elif action == "1g1p":
                successor[0] += 1
                successor[3] -= 1
                successor[1] += 1
                successor[4] -= 1
            elif action == "1g":
                successor[0] += 1
                successor[3] -= 1
            elif action == "1p":
                successor[1] += 1
                successor[4] -= 1

        self.state = tuple(successor)

    def legalActions(self):
        """
        Returns an iterator to the legal actions that can be executed in the
        current state.
        """
        if self.state[2] == 0:
            if (self.state[0] >= 2 and (self.state[0] == 2 or (self.state[0] - 2 - self.state[1]) >= 0) and (self.state[3] + 2 - self.state[4]) >= 0):
                yield "2g"
            if (self.state[0] >= 1 and (self.state[0] == 1 or (self.state[0] - 1 - self.state[1]) >= 0) and (self.state[3] + 1 - self.state[4]) >= 0):
                yield "1g"
            if (self.state[0] >= 1 and self.state[1] >= 1 and (self.state[3] - self.state[4]) >= 0):
                yield "1g1p"
            if (self.state[1] >= 2 and (self.state[3] == 0 or (self.state[3] > 0 and (self.state[3] - self.state[4] - 2) >= 0))):
                yield "2p"
            if (self.state[1] >= 1 and (self.state[3] == 0 or (self.state[3] > 0 and (self.state[3] - self.state[4] - 1) >= 0))):
                yield "1p"
        else:
            if (self.state[3] >= 2 and (self.state[3] == 2 or (self.state[3] - 2 - self.state[4]) >= 0) and (self.state[0] + 2 - self.state[1]) >= 0):
                yield "2g"
            if (self.state[3] >= 1 and (self.state[3] == 1 or (self.state[3] - 1 - self.state[4]) >= 0) and (self.state[0] + 1 - self.state[1]) >= 0):
                yield "1g"
            if (self.state[3] >= 1 and self.state[4] >= 1 and (self.state[0] - self.state[1]) >= 0):
                yield "1g1p"
            if (self.state[4] >= 2 and (self.state[0] == 0 or (self.state[0] > 0 and (self.state[0] - self.state[1] - 2) >= 0))):
                yield "2p"
            if (self.state[4] >= 1 and (self.state[0] == 0 or (self.state[0] > 0 and (self.state[0] - self.state[1] - 1) >= 0))):
                yield "1p"

    def invert_action(self, action):
        """ each action undoes itself """
        return action


class GuardsPrisonersProblem(Problem):
    """
    This class wraps around an Guards and Prisoners object and instantiates the
    successor and goal test functions necessary for conducting search.

    This class also implements an heuristic function which is used to compute
    the value for each successor as cost to node + heuristic estimate of
    distance to goal. This yield A* search when used with best first search or
    a more greedy variant when used with Beam Search.
    """

    def misplaced_person_heuristic(self, state, goal):
        """
        The misplaced tiles heuristic.
        """
        h = 0
        
        for idx in range(len(state.state)):
            h += abs(state.state[idx] - goal.state[idx])

        return h

    def node_value(self, node):
        """
        The function used to compute the value of a node.
        """
        if isinstance(node, GoalNode):
            return (node.cost() +
                    self.misplaced_person_heuristic(self.initial.state,
                                                   node.state))
        else:
            return (node.cost() +
                    self.misplaced_person_heuristic(node.state, self.goal.state))

    def successors(self, node):
        """
        Computes successors and computes the value of the node as cost +
        heuristic, which yields A* search when using best first search.
        """
        for action in node.state.legalActions():
            new_state = node.state.copy()
            new_state.executeAction(action)
            path_cost = node.cost() + 1
            yield Node(new_state, node, action, path_cost)

    def predecessors(self, goal_node):
        """
        Computes successors and computes the value of the node as cost +
        heuristic, which yields A* search when using best first search.
        """
        for action in goal_node.state.legalActions():
            new_goal = goal_node.state.copy()
            new_goal.executeAction(action)
            path_cost = goal_node.cost() + 1
            yield GoalNode(new_goal, goal_node,
                           goal_node.state.invert_action(action), path_cost)


class NoHeuristic(GuardsPrisonersProblem):
    """
    A variation on the Eight Puzzle Problem that has a heuristic for 0. This
    yields something equivelent to dijkstra's algorithm when used with best
    first search and a more greedy variant when used with Beam Search.
    """

    def node_value(self, node):
        return node.cost()


if __name__ == "__main__":

    goal = GuardsPrisoners()
    goal.state = (0, 0, 1, 3, 3)

    initial = GuardsPrisoners()
    print("Initial State:")
    print(initial)
    print()

    def iterative_sampling_100_10(problem):
        return iterative_sampling(problem, max_samples=100, depth_limit=10)

    def backward_bf_search(problem):
        return best_first_search(problem, forward=False, backward=True)

    def bidirectional_breadth_first_search(problem):
        return breadth_first_search(problem, forward=True, backward=True)

    compare_searches(problems=[GuardsPrisonersProblem(initial, goal), NoHeuristic(initial, goal)],
                     searches=[iterative_sampling_100_10,
                               depth_first_search,
                               breadth_first_search,
                               bidirectional_breadth_first_search,
                               iterative_deepening_search,
                               best_first_search,
                               backward_bf_search,
                               iterative_deepening_best_first_search,
                               widening_beam_search
                               ])

    solution = next(best_first_search(GuardsPrisonersProblem(initial, goal)))
    print(solution.path())
