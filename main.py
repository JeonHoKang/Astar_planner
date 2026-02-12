import heapq
from copy import deepcopy


# ----------------------------
# Predicate helpers
# ----------------------------

def has(state, pred):
    return pred in state


def add(state, pred):
    new_state = set(state)
    new_state.add(pred)
    return frozenset(new_state)


def remove(state, pred):
    new_state = set(state)
    if pred in new_state:
        new_state.remove(pred)
    return frozenset(new_state)

def goal_test(state, goal_object):
    return any(
        ("inserted", o, goal_object) in state
        for o in objects
    )


# ----------------------------
# Action Schema
# ----------------------------

class Action:
    def __init__(self, name, parameters, precondition_fn, effect_fn, cost_fn):
        self.name = name
        self.parameters = parameters
        self.precondition_fn = precondition_fn
        self.effect_fn = effect_fn
        self.cost_fn = cost_fn

    def applicable(self, state):
        return self.precondition_fn(state)

    def apply(self, state):
        return self.effect_fn(state)

    def cost(self, state):
        return self.cost_fn(state)

    def __repr__(self):
        return f"{self.name}{self.parameters}"


# ----------------------------
# Example Actions
# ----------------------------

def make_pick_side(o):

    def precond(state):
        return (
            has(state, ("is_graspable", o)) and
            has(state, ("side_clearance", o)) and
            has(state, ("gripper_empty",))
        )

    def effect(state):
        state2 = add(state, ("held", o))
        state2 = remove(state2, ("gripper_empty",))
        return state2

    def cost(state):
        return 4  # more expensive

    return Action("pick_side", (o,), precond, effect, cost)

def make_pick_upwards(o):

    def precond(state):
        return (
            has(state, ("is_graspable", o)) and
            has(state, ("top_clearance", o)) and
            has(state, ("gripper_empty",))
        )

    def effect(state):
        state2 = add(state, ("held", o))
        state2 = remove(state2, ("gripper_empty",))
        return state2

    def cost(state):
        return 2  # cheap

    return Action("pick_upwards", (o,), precond, effect, cost)

def make_insert(o, h):
    def precond(state):
        return (
            has(state, ("held", o)) and
            not has(state, ("inserted", o, h))
        )

    def effect(state):
        state2 = add(state, ("inserted", o, h))
        state2 = remove(state2, ("held", o))
        return state2

    def cost(state):
        return 3

    return Action("insert", (o, h), precond, effect, cost)


# ----------------------------
# A* Planner
# ----------------------------

def heuristic(state, goal):
    # Simple heuristic: number of missing goal predicates
    return len(goal - state)


def astar(initial_state, goal_test, actions):

    open_list = []
    heapq.heappush(open_list, (0, 0, initial_state, []))

    visited = {}

    while open_list:
        f, g, state, plan = heapq.heappop(open_list)

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
                               (new_f, new_g, next_state, plan + [action]))

    return None


def main():
    object_types = {
        "gear_1": "gear",
        "gear_2": "gear",
        "peg_1": "peg",
    }
    hole = ["hole_1", "hole_2"]

    initial_state = frozenset({
        ("is_graspable", "gear_1"),
        ("is_orientation_right", "gear_1"),
        ("is_graspable", "gear_2"),
        ("gripper_empty",),
    })

    actions = [
        make_pick("gear_1"),
        make_insert("gear_1", "shaft_1"),
        make_pick("gear_2"),
        make_insert("gear_2", "shaft_1"),
    ]

    plan = astar(initial_state, goal_test, actions)
    actions = []
    for o in objects: 
        actions.append(make_pick_upwards(o))
        actions.append(make_insert(o, hole))

    plan = astar(initial_state, goal_test, actions)

    print("Plan:")
    for step in plan:
        print(step)
if __name__ == '__main__':
    main()