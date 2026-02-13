# ----------------------------
# Predicate helpers
# ----------------------------

def has(state, pred):
    """
    check if the predicate is in the state
    Input: state and predicate
    state: what state the robot is in
    predicate: type of predicates
    Output: Outputs True or False based on if predicate exists

    """
    return pred in state


def add(state, pred):
    """
    add a predicate to the state based on the state observation: for example) initial predicates added in the begining
    Input: state and predicate
    state: what state the robot is in
    predicate: type of predicates
    Output: Returns the forzen set of new state withe the added predicate

    """

    new_state = set(state)
    new_state.add(pred)
    return frozenset(new_state)


def remove(state, pred):
    """
    removes a predicate from the state based on the state observation : like for example) gripper_empty removed from predicate after grasping
    Input: state and predicate
    state: what state the robot is in
    predicate: type of predicates
    Output: Returns the forzen set of new state withe the removed predicate

    """

    new_state = set(state)
    if pred in new_state:
        new_state.remove(pred)
    return frozenset(new_state)

def goal_check(state, goals):
    """
    state: current frozenset state
    goals: iterable of goal predicates
    """
    return all(goal in state for goal in goals)