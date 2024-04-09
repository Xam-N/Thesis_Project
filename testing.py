class Node:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def build_parse_tree(expression):
    # Remove whitespace from the expression
    expression = expression.replace(" ", "")

    # Helper function to create nodes
    def create_node(value):
        return Node(value)

    # Helper function to parse the expression recursively
    def parse_expression(start, end):
        if start == end:
            return create_node(expression[start])

        parentheses_count = 0
        lowest_operator_index = None
        for i in range(end, start - 1, -1):
            if expression[i] == ')':
                parentheses_count += 1
            elif expression[i] == '(':
                parentheses_count -= 1
            elif expression[i] in {'and', 'or'} and parentheses_count == 0:
                lowest_operator_index = i
                break

        if lowest_operator_index is not None:
            root = create_node(expression[lowest_operator_index])
            root.left = parse_expression(start, lowest_operator_index - 1)
            root.right = parse_expression(lowest_operator_index + 1, end)
            return root
        elif expression[start] == '(' and expression[end] == ')':
            return parse_expression(start + 1, end - 1)
        else:
            return create_node(expression[start:end + 1])

    # Start parsing from the first character
    return parse_expression(0, len(expression) - 1)

def build_adjacency_matrix(root, matrix=None):
    if matrix is None:
        matrix = {}

    if root is not None:
        if root.value in {'and', 'or'}:
            matrix[root.value] = matrix.get(root.value, [])

            if root.left:
                matrix[root.value].append(root.left.value)
                build_adjacency_matrix(root.left, matrix)
            if root.right:
                matrix[root.value].append(root.right.value)
                build_adjacency_matrix(root.right, matrix)
        else:
            matrix[root.value] = []

    return matrix

# Example usage:
expression = "(COMP3100 or COMP3000) and (20cp from 3000 level units)"
parse_tree_root = build_parse_tree(expression)
adjacency_matrix = build_adjacency_matrix(parse_tree_root)
print(adjacency_matrix)
