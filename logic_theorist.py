IMPLIES = '->'
AND = 'AND'
OR = 'OR'
NOT = 'NOT'

class LogicalExpression:  
    def __init__(self, operator, operands):
        self.operands = operands
        self.operator = operator
    
    def __eq__(self, other):
        if isinstance(other, LogicalExpression):
            return self.operator == other.operator and self.operands == other.operands
        return False

def modus_ponens(expression, A):
    if expression.operator == IMPLIES:
        operands = expression.operands
        if operands[0] == A:
            return operands[1]
    return expression

def modus_tollens(expression, not_B):
    if expression.operator == IMPLIES:
        operands = expression.operands
        if operands[1] == not_B.operands[0]:
            return LogicalExpression(NOT, [operands[0]])
    return expression

def conjunction_introduction(A, B):
    return LogicalExpression(AND, [A, B])

def conjunction_elimination(expression):
    if expression.operator == AND:
        return expression.operands
    return expression

def disjunction_introduction(A, B):
    return LogicalExpression(OR, [A, B])

def disjunction_elimination(expression):
    if expression.operator == OR:
        return expression.operands
    return expression