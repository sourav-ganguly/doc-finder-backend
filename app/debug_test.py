"""
A simple module to test debugging functionality.
"""


def test_function(value):
    """A simple function to test debugging."""
    result = value * 2
    print(f"Value: {value}, Result: {result}")
    return result


# This will be executed when the module is imported
print("Debug test module loaded!")
