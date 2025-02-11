# coding: utf-8
#
# Copyright 2021 The Technical University of Denmark
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#    http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from __future__ import annotations
import sys
import time
import memory
from typing import Union

import domains.hospital.actions as actions
import domains.hospital.state as state
import domains.hospital.goal_description as goal_description
import strategies.bfs as bfs

from domains.hospital.actions import MoveAction

# Note: This syntax below (<variable name>: <variable type>) is type hinting and is meant
# to make it easier for you to understand (now you know that `action_set` is a list of lists of
# actions!) but if it is confusing, you can just ignore it as it is only for documentation
def graph_search(
        initial_state:      state.HospitalState,
        action_set:         list[list[actions.AnyAction]],
        goal_description:   goal_description.HospitalGoalDescription,
        frontier:           bfs.FrontierBFS
    ) -> tuple[bool, list[list[actions.AnyAction]]]:

    global start_time

    # Set start time
    start_time = time.time()
    iterations = 0
    frontier.prepare(goal_description)

    # Clear the parent pointer and cost in order make sure that the initial state is a root node
    initial_state.parent = None
    initial_state.path_cost = 0
    
    # Here, you should implement the Graph-Search algorithm from R&N figure 3.7
    # The algorithm should here return a (boolean, list) pair where the boolean denotes
    # whether the algorithm successfully found a plan and the list is the found plan.
    # In the case of "failure to find a solution" you should therefore return False, [].
    # Some useful methods on the State class which you will need to use are:
    # node.extract_plan() - Returns the list of actions used to reach this state. <=== Q: how does it know without knowing the start/end nodes?
    # node.get_applicable_actions(action_set) - Returns a list containing the actions applicable in the state.
    # node.result(action) - Returns the new state reached by applying the action to the current state.
    # For the GoalDescription class, you will need to use
    # goal_description.is_goal(node) - Returns true if the state is a goal state.
    # For debugging, remember that you can use print(node, file=sys.stderr) to get a representation of the state.
    # You should also take a look at the frontiers in the strategies folder to see which methods they expose

    return_fixed_solution = False
    
    if return_fixed_solution:
        return True, []
    
    # added: our implementation of graph search

    frontier.add(initial_state)           # start node
    visited = set()                       # a set to keep track of visited nodes
    visited.add(initial_state)

    states_generated = 0

    while (True):

        if (frontier.is_empty()): break
        currNode = frontier.pop()
        states_generated += 1
            
        # check if each state is the goal.
        # if we reached goal state -> end the search so there's a possibility 
        # all the nodes aren't hit
        # print("agents", currNode.agent_positions)
        # print("boxes", currNode.box_positions)
        if (goal_description.is_goal(currNode)):
            # print("goal", goal_description)
            # print("curr", currNode)
            print("Goal Reached! States generated: ", states_generated)
            # print(currNode.extract_plan())
            return True, currNode.extract_plan()

        # returns list of next actions
        next_actions = currNode.get_applicable_actions(action_set)
        for action in next_actions:
            nextNode = currNode.result(action)
            
            if (not frontier.contains(nextNode) and nextNode not in visited):
                # follow each action to the next node and add to our queue
                frontier.add(nextNode) 
                visited.add(nextNode)

    print("Search Finished without finding a solution")

    return False, []


# A global variable used to keep track of the start time of the current search
start_time = 0


def print_search_status(expanded, frontier):
    global start_time
    if len(expanded) == 0:
        start_time = time.time()
    memory_usage_bytes = memory.get_usage()
    # Replacing the generated comma thousands separators with dots is neither pretty nor locale aware but none of
    # Pythons four different formatting facilities seems to handle this correctly!
    num_expanded = f"{len(expanded):8,d}".replace(',', '.')
    num_frontier = f"{frontier.size():8,d}".replace(',', '.')
    num_generated = f"{len(expanded) + frontier.size():8,d}".replace(',', '.')
    elapsed_time = f"{time.time() - start_time:3.3f}".replace('.', ',')
    memory_usage_mb = f"{memory_usage_bytes / (1024*1024):3.2f}".replace('.', ',')
    status_text = f"#Expanded: {num_expanded}, #Frontier: {num_frontier}, #Generated: {num_generated}," \
                  f" Time: {elapsed_time} s, Memory: {memory_usage_mb} MB"
    print(status_text, file=sys.stderr)