from action import Action
from astar_util import add, remove, has


""" ----------------------------
List of actions for gear assembly
1. pick gear from the side
2. pick gear from the top
3. pick peg right
4. pick peg from opposite
5. pick peg from the side orientation
6. insert_peg
7. insert_gear
----------------------------------"""

""" ----------------------------
List of predicates for gear assembly
1. is_detectable(object)
2. object_orientation(object, ) -> what orientation it is
    for cog: Top or Bottom
    for peg: right, opposite, side
3. is_graspable(object)
4. holding(object, orientation) empty list means gripper_empty
----------------------------------"""

def make_pick(o, o_type, orientation, cost_value):
    def precond(state):
        return (
            has(state, ("is_detectable", o,)) and
            has(state, ("object_orientation", o, orientation)) and
            has(state, ("is_graspable", o)) and
            has(state, ("holding", None, None))
        )

    def effect(state):
        # We can have this effect only if we have succeeded
        if o_type == "gear":
            state_step1 = add(state, ("holding", o_type, orientation))
        else:
            state_step1 = add(state, ("holding", o_type, None))
        new_state = remove(state_step1, ("holding", None, None))
        new_state = remove(new_state, ("is_graspable", o))
        new_state = remove(new_state, ("object_orientation", o, orientation))
        return new_state
    
    def cost(state):
        return cost_value 
    
    return Action(f"pick_{o_type}_{orientation}", (o,), precond, effect, cost)


def make_insert(o, target, support=None, grasp_mode=None, cost_value=1):

    if grasp_mode is not None:
        action_name = f"insert_{o}_into_{target}_{grasp_mode}"
    else:
        action_name = f"insert_{o}_into_{target}"

    def precond(state):
        holding_ok = has(state, ("holding", o, grasp_mode))

        support_ok = True
        if support is not None:
            support_ok = has(state, ("inserted", support, target))

        return holding_ok and support_ok

    def effect(state):
        # remove holding
        state1 = remove(state, ("holding", o, grasp_mode))

        # gripper becomes empty
        state2 = add(state1, ("holding", None, None))

        # add insertion fact
        if support is None:
            state3 = add(state2, ("inserted", o, target))
        else:
            state3 = add(state2, ("inserted", o, support, target))

        return state3

    def cost_fn(state):
        return cost_value

    return Action(action_name,(o, target), precond, effect, cost_fn)

def make_singulate(o, cost_value=1):

    def precond(state):
        return (
            not has(state, ("is_graspable", o)) and
            has(state, ("holding", None, None))
        )

    def effect(state):
         
        state2 = add(state, ("is_graspable", o))
        return state2

    def cost_fn(state):
        return cost_value

    return Action(f"singulate_{o}",(o, ), precond, effect, cost_fn)
