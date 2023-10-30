IMPLIES = '->'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'


class LogicalExpression:
    def __init__(self, operator, operands = []):
        self.operands = operands
        self.operator = operator

    def __eq__(self, other):
        if isinstance(other, LogicalExpression):
            return self.operator == other.operator and self.operands == other.operands
        return False

    def __hash__(self):
        return hash((self.operator, tuple(self.operands)))


def modus_ponens(expression, A):
    if expression.operator == IMPLIES:
        operands = expression.operands
        if operands[0] == A:
            return operands[1]
    return None


def modus_tollens(expression, not_B):
    if expression.operator == IMPLIES:
        operands = expression.operands
        if len(not_B.operands) <= 0:
            return None
        if operands[1] == not_B.operands[0]:
            return LogicalExpression(NOT, [operands[0]])
    return None


def conjunction_introduction(A, B):
    return LogicalExpression(AND, [A, B])


def conjunction_elimination(expression, _):
    if expression.operator == AND:
        return expression.operands
    return None


def disjunction_introduction(A, B):
    return LogicalExpression(OR, [A, B])


def disjunction_elimination(expression, _):
    if expression.operator == OR:
        return expression.operands
    return None


class LogicTheorist():
    def __init__(self, root, axioms):
        self.root = root
        self.axioms = axioms
        self.derived = set([])
        self.inference_rules = [disjunction_elimination, disjunction_introduction,
                                conjunction_elimination, conjunction_introduction,
                                modus_tollens, modus_ponens]

    def prove(self):
        stack = []
        stack.append(self.root)
        while (len(stack) > 0):
            expression = stack.pop()
            for axiom in self.axioms:
                for inference_rule in self.inference_rules:
                    child = inference_rule(expression, axiom)
                    if isinstance(child, list):
                        for sub_child in child:
                            if sub_child == self.root:
                                return True
                            if sub_child not in self.derived:
                                self.derived.add(sub_child)
                                stack.append(sub_child)
                    else:
                        if child:
                            if child == self.root:
                                return True
                            if child not in self.derived:
                                self.derived.add(child)
                                stack.append(child)
        return False

A = LogicalExpression('A')
B = LogicalExpression('B')

axioms = [A, LogicalExpression(IMPLIES, [A, B])]
theorem = B

print(LogicTheorist(theorem, axioms).prove())
