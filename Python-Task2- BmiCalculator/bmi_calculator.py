"""
BMI Calculator (Beginner Tier)
--------------------------------
Prompts the user for weight (kg) and height (m), calculates BMI,
classifies it into a standard health category, and validates input.

Formula: BMI = weight (kg) / height (m)^2
"""


def get_positive_float(prompt: str) -> float:
    """Repeatedly ask the user for input until a valid positive number is given."""
    while True:
        raw_value = input(prompt).strip()
        try:
            value = float(raw_value)
        except ValueError:
            print("  ⚠ Please enter a valid number (e.g. 68.5). Try again.")
            continue

        if value <= 0:
            print("  ⚠ Value must be greater than zero. Try again.")
            continue

        return value


def classify_bmi(bmi: float) -> str:
    """Return the standard BMI category for a given BMI value."""
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    return weight_kg / (height_m ** 2)


def main():
    print("=" * 45)
    print("           BMI CALCULATOR")
    print("=" * 45)

    while True:
        weight = get_positive_float("Enter your weight in kg: ")
        height = get_positive_float("Enter your height in m (e.g. 1.75): ")

        bmi = calculate_bmi(weight, height)
        category = classify_bmi(bmi)

        print("\n" + "-" * 45)
        print(f"Your BMI is: {bmi:.2f}")
        print(f"Category   : {category}")
        print("-" * 45)

        again = input("\nCalculate another BMI? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for using the BMI Calculator. Stay healthy!")
            break
        print()


if __name__ == "__main__":
    main()
