import heapq
from astar_util import goal_check
from make_action import  make_pick, make_insert
import itertools

def generate_actions(objects, holes,
                     gear_orientations,
                     rod_orientations):

    actions = []

    for obj, obj_type in objects.items():
        # -----------------
        # PICK ACTIONS
        # -----------------
        if obj_type == "gear":
            for orientation, cost in gear_orientations.items():
                actions.append(make_pick(obj, obj_type, orientation, cost))

        elif obj_type == "rod":
            for orientation, cost in rod_orientations.items():
                actions.append(make_pick(obj, obj_type, orientation, cost))

        # -----------------
        # INSERT ACTIONS
        # -----------------
    for obj_type in set(objects.values()):

        if obj_type == "rod":
            # rod → hole
            for hole in holes.keys():
                actions.append(make_insert(obj_type, hole, cost_value=3))

        elif obj_type == "gear":
            # gear → rod
            for hole in holes.keys():
                for orientation, cost in gear_orientations.items():
                    actions.append(make_insert(obj_type, hole, support = "rod", grasp_mode = orientation, cost_value=cost))
    return actions

# ----------------------------k
# A* Planner
# ----------------------------

def heuristic(state, goal):
    # Simple heuristic: number of missing goal predicates
    return len(state)


def astar(initial_state, goal_test, actions):
    counter = itertools.count()
    open_list = []

    heapq.heappush(open_list, (0, 0, next(counter), initial_state, []))

    visited = {}

    while open_list:
        f, g, _, state, plan = heapq.heappop(open_list)

        if goal_test(state):
            return plan

        if state in visited and visited[state] <= g:
            continue

        visited[state] = g

        for action in actions:
             if action.applicable(state):
                next_state = action.apply(state)
                new_g = g + action.cost(state)
                new_f = new_g + heuristic(next_state, goal_test)
                heapq.heappush(open_list,
                               (new_f, new_g, next(counter), next_state, plan + [action]))

    return None


def main():
    """ ----------------------------
List of predicates for gear assembly
1. is_graspable(object)
2. object_orientation(object, ) -> what orientation it is
    for cog: Top or Bottom
    for peg: right, opposite, side
3. is_graspable(object)
4. holding(object, orientation) empty list means gripper_empty
----------------------------------"""
    object_types = ["gear", "rod"]

    # These objects should be given by the environment 
    objects = {
        "gear_1": object_types[0],
        "gear_2": object_types[0],
        "gear_3": object_types[0],
        "rod_1": object_types[1],
        "rod_2": object_types[1],
        "rod_3": object_types[1]

    }

    holes = {"hole_1": "hole", "hole_2":"hole"}

    # This initial state should be given by the obervations from the environment
    # For pick() is_grapable(o), orientation(o) holding(o)
     
    initial_state = frozenset({
        ("is_graspable", "gear_1"),
        ("is_graspable", "gear_2"),
        ("is_graspable", "gear_3"),

        ("object_orientation", "gear_1", "bottom"),
        ("object_orientation", "gear_2", "top"),
        ("object_orientation", "gear_3", "bottom"),

        ("is_graspable", "rod_1"),
        ("is_graspable", "rod_2"),
        ("is_graspable", "rod_3"),

        ("object_orientation", "rod_1", "right"),
        ("object_orientation", "rod_2", "right"),
        ("object_orientation", "rod_3", "side"),

        ("holding", None, None),
    })

    gear_orientations = {
        "bottom": 4,
        "top": 2
    }

    rod_orientations = {
        "right": 1,
        "side": 2,
        "away": 4
    }

    available_actions = generate_actions(objects, holes, gear_orientations, rod_orientations)


    goal = [('inserted', "gear", "rod", "hole_1"), ('inserted', "gear", "rod", "hole_2")]


    plan = astar(
        initial_state,
        lambda s: goal_check(s, goal),
        available_actions
    )


    print("Plan:")


    for step in plan:
        print(step)


if __name__ == '__main__':
    main()