"""
A simple script to test debugging functionality.
"""

from app.debug_test import test_function


def main():
    """Main function to test debugging."""
    print("Starting debug test...")

    # This is a simple function call that we can set a breakpoint on
    value = 10
    result = test_function(value)

    print(f"Final result: {result}")
    print("Debug test completed!")


if __name__ == "__main__":
    main()
