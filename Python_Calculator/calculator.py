
import math
from datetime import datetime


class ScientificCalculator:

    def __init__(self):
        self.history = []

    def calculate(self, operation, a, b=None):
        operations = {
            "1": ("Addition", lambda: a + b),
            "2": ("Subtraction", lambda: a - b),
            "3": ("Multiplication", lambda: a * b),
            "4": ("Division", lambda: a / b),
            "5": ("Power", lambda: a ** b),
            "6": ("Modulus", lambda: a % b),
            "7": ("Floor Division", lambda: a // b),
            "8": ("Square Root", lambda: math.sqrt(a)),
            "9": ("Factorial", lambda: math.factorial(a)),
            "10": ("Percentage", lambda: (a * b) / 100),
            "11": ("Sine", lambda: math.sin(math.radians(a))),
            "12": ("Cosine", lambda: math.cos(math.radians(a))),
            "13": ("Tangent", lambda: math.tan(math.radians(a))),
            "14": ("Logarithm (Base 10)", lambda: math.log10(a)),
            "15": ("Natural Logarithm", lambda: math.log(a)),
        }

        if operation not in operations:
            raise ValueError("Invalid operation selected.")

        name, function = operations[operation]

        # Validate special operations
        if operation in ["4", "6", "7"] and b == 0:
            raise ZeroDivisionError("Cannot divide by zero.")

        if operation in ["8"] and a < 0:
            raise ValueError("Square root requires a non-negative number.")

        if operation == "9":
            if a < 0 or not a.is_integer():
                raise ValueError("Factorial requires a non-negative integer.")

        if operation in ["14", "15"] and a <= 0:
            raise ValueError("Logarithm requires a positive number.")

        if operation == "5" and a == 0 and b < 0:
            raise ValueError("Zero cannot have a negative exponent.")

        result = function()

        if isinstance(result, float) and not math.isfinite(result):
            raise ValueError("Result is outside the supported numeric range.")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.history.append({
            "operation": name,
            "number1": a,
            "number2": b,
            "result": result,
            "time": timestamp
        })

        return result

    def show_history(self):
        if not self.history:
            print("\nNo calculation history available.")
            return

        print("\n========== CALCULATION HISTORY ==========")

        for index, item in enumerate(self.history, start=1):
            print(
                f"{index}. {item['operation']}: "
                f"{item['number1']} | {item['number2']} "
                f"= {item['result']}"
            )
            print(f"   Time: {item['time']}")

        print("=========================================")

    def clear_history(self):
        self.history.clear()
        print("\nHistory cleared successfully!")


def display_menu():
    print("\n" + "=" * 45)
    print("          PYTHON SCIENTIFIC CALCULATOR")
    print("=" * 45)

    print("""
    BASIC OPERATIONS
    1.  Addition
    2.  Subtraction
    3.  Multiplication
    4.  Division
    5.  Power
    6.  Modulus
    7.  Floor Division

    SCIENTIFIC OPERATIONS
    8.  Square Root
    9.  Factorial
    10. Percentage
    11. Sine
    12. Cosine
    13. Tangent
    14. Logarithm (Base 10)
    15. Natural Logarithm

    OTHER OPTIONS
    16. View History
    17. Clear History
    0.  Exit
    """)


def main():

    calculator = ScientificCalculator()

    print("\nWelcome to Python Scientific Calculator!")

    while True:

        display_menu()

        choice = input("Select an operation: ").strip()

        if choice == "0":
            print("\nThank you for using the calculator!")
            break

        if choice == "16":
            calculator.show_history()
            continue

        if choice == "17":
            calculator.clear_history()
            continue

        if choice not in [str(i) for i in range(1, 16)]:
            print("\nInvalid choice! Please select a valid option.")
            continue

        try:
            a = float(input("Enter first number: "))

            # Operations requiring only one number
            single_number_operations = ["8", "9", "11", "12", "13", "14", "15"]

            if choice in single_number_operations:
                b = None
            else:
                b = float(input("Enter second number: "))

            result = calculator.calculate(choice, a, b)

            print("\n" + "-" * 45)
            print(f"Result: {result:,.10g}")
            print("-" * 45)

        except ValueError as error:
            print(f"\nInput/Calculation Error: {error}")

        except ZeroDivisionError as error:
            print(f"\nMath Error: {error}")

        except OverflowError:
            print("\nMath Error: Result is too large.")

        except Exception as error:
            print(f"\nUnexpected Error: {error}")


if __name__ == "__main__":
    main()
