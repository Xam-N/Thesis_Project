from pyparsing import infixNotation, opAssoc, Keyword, Word, alphas

# Define boolean operations
TRUE = Keyword("True")
FALSE = Keyword("False")
AND = Keyword("and")
OR = Keyword("or")
NOT = Keyword("not")

# Define grammar
variable = Word(alphas)
expression = infixNotation(variable,
                           [
                               (NOT, 1, opAssoc.RIGHT, ),
                               (AND, 2, opAssoc.LEFT, ),
                               (OR, 2, opAssoc.LEFT, ),
                           ])

# Parse boolean expression
def parse_boolean_expr(expr):
    return expression.parseString(expr)[0]

# Test the parser
boolean_expr = "not A and (B or C)"
parsed_expr = parse_boolean_expr(boolean_expr)
print(parsed_expr)