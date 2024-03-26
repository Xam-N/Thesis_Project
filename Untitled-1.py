def parse_boolean_statement(statement):
    """
    Parses a plain text boolean statement and converts it into a computer-readable version.

    Args:
    statement (str): The plain text boolean statement.

    Returns:
    str: The computer-readable version of the boolean statement.
    """

    # Dictionary to map plain text boolean operators to computer-readable ones
    operator_mapping = {
        'and': ' and ',
        'or': ' or ',
        'not': ' not ',
        '(': '(',
        ')': ')'
    }

    # Replace plain text boolean operators with computer-readable ones
    for word, operator in operator_mapping.items():
        statement = statement.replace(word, operator)

    return statement

# Example usage:
plain_text_statement = "A and (B or not C)"
computer_readable_statement = parse_boolean_statement(plain_text_statement)
print("Computer-readable statement:", computer_readable_statement)