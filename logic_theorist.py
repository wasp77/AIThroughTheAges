IMPLIES = '->'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'


class LogicalExpression:
    def __init__(self, operator, operands=[]):
        self.operands = operands
        self.operator = operator

    def __eq__(self, other):
        if isinstance(other, LogicalExpression):
            return self.operator == other.operator and self.operands == other.operands
        return False

    def __hash__(self):
        return hash((self.operator, tuple(self.operands)))


def modus_ponens(expression, A, _):
    if expression.operator == IMPLIES:
        operands = expression.operands
        if operands[0] == A:
            return operands[1]
    return None


def modus_tollens(expression, not_B, _):
    if expression.operator == IMPLIES and not_B.operator == NOT:
        operands = expression.operands
        if operands[1] == not_B.operands[0]:
            return LogicalExpression(NOT, [operands[0]])
    return None


def conjunction_introduction(A, B, known_truths):
    if A in known_truths and B in known_truths:
        return LogicalExpression(AND, [A, B])
    return None


def conjunction_elimination(expression, _, __):
    if expression.operator == AND:
        return expression.operands
    return None


def disjunction_introduction(A, B, known_truths):
    if A in known_truths or B in known_truths:
        return LogicalExpression(OR, [A, B])
    return None


def disjunction_elimination(expression, _, known_truths):
    if expression.operator == OR:
        A, B = expression.operands
        if A in known_truths or B in known_truths:
            return expression.operands
    return None


def disjunctive_syllogism(expression, not_A, _):
    if expression.operator == OR:
        operands = expression.operands
        if not_A.operator == NOT and not_A.operands[0] == operands[0]:
            return operands[1]
        elif not_A.operator == NOT and not_A.operands[0] == operands[1]:
            return operands[0]
    return None

def chain_forward(expression, axiom, known_truths):
    if expression == axiom:
        return None

    known_axioms = known_truths | {axiom}
    # Check if expression is of the form A -> B
    if expression.operator == IMPLIES:
        A = expression.operands[0]
        B = expression.operands[1]

        # Look for a known axiom of the form B -> C
        for axiom in known_axioms:
            if axiom.operator == IMPLIES and axiom.operands[0] == B:
                C = axiom.operands[1]
                return LogicalExpression(IMPLIES, [A, C])

    return None

def chain_backward(expression, axiom, known_truths):
    if expression == axiom:
        return None


    known_axioms = known_truths | {axiom}

    # Check if expression is of the form A -> C
    if expression.operator == IMPLIES:
        A = expression.operands[0]
        C = expression.operands[1]

        # Look for a known axiom of the form B -> C
        for axiom in known_axioms:
            if axiom.operator == IMPLIES and axiom.operands[1] == C:
                B = axiom.operands[0]
                return LogicalExpression(IMPLIES, [A, B])

    return None

'''
This wants to be rewritten so that the axioms are part of derived so that
the chaining works. 
'''
class LogicTheorist():
    def __init__(self, root, axioms):
        self.root = root
        self.axioms = axioms
        self.derived = set([])
        self.inference_rules = [disjunctive_syllogism, disjunction_elimination, disjunction_introduction,
                                conjunction_elimination, conjunction_introduction,
                                modus_tollens, modus_ponens, chain_backward, chain_forward]

    def prove(self):
        stack = []
        stack.append(self.root)
        stack.extend(self.axioms)
        while (len(stack) > 0):
            expression = stack.pop()
            for axiom in self.axioms:
                for inference_rule in self.inference_rules:
                    child = inference_rule(expression, axiom, self.derived)
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
C = LogicalExpression('C')

axioms = [A, LogicalExpression(IMPLIES, [A, B])]
theorem = B
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(NOT, [B]), LogicalExpression(IMPLIES, [A, B])]
theorem = LogicalExpression(NOT, [A])
print(LogicTheorist(theorem, axioms).prove())

axioms = [A, B]
theorem = LogicalExpression(AND, [A, B])
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(OR, [A, B]), LogicalExpression(NOT, [A])]
theorem = B
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(NOT, [A])]
theorem = A
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(AND, [A, B])]
theorem = A
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(OR, [A, B])]
theorem = LogicalExpression(NOT, [A])
print(LogicTheorist(theorem, axioms).prove())

axioms = [LogicalExpression(IMPLIES, [A, B]), LogicalExpression(IMPLIES, [B, C])]
theorem = LogicalExpression(IMPLIES, [A, C])
print(LogicTheorist(theorem, axioms).prove())