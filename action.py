
# ----------------------------
# Action Schema
# ----------------------------

class Action:

    """
    Action object that has precondition for action -> checks applicable and apply function that applies the action, cost
    """

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