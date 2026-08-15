"""
Random Password Generator (Beginner Tier)
-------------------------------------------
Generates a random password based on user-defined length and
character-type selection (uppercase, lowercase, numbers, symbols).
"""

import random
import string


def get_length() -> int:
    while True:
        raw_value = input("Enter desired password length (minimum 8): ").strip()
        if not raw_value.isdigit():
            print("  ⚠ Please enter a whole number.")
            continue
        length = int(raw_value)
        if length < 8:
            print("  ⚠ Length must be at least 8 characters.")
            continue
        return length


def get_character_types() -> dict:
    print("\nChoose which character types to include (y/n for each).")
    print("You must select at least 2 types.")

    while True:
        use_upper = input("  Include UPPERCASE letters? (y/n): ").strip().lower() == "y"
        use_lower = input("  Include lowercase letters? (y/n): ").strip().lower() == "y"
        use_digits = input("  Include numbers?          (y/n): ").strip().lower() == "y"
        use_symbols = input("  Include symbols?          (y/n): ").strip().lower() == "y"

        selected_count = sum([use_upper, use_lower, use_digits, use_symbols])
        if selected_count < 2:
            print("  ⚠ Please select at least 2 character types.\n")
            continue

        return {
            "upper": use_upper,
            "lower": use_lower,
            "digits": use_digits,
            "symbols": use_symbols,
        }


def build_character_pool(types: dict) -> str:
    pool = ""
    if types["upper"]:
        pool += string.ascii_uppercase
    if types["lower"]:
        pool += string.ascii_lowercase
    if types["digits"]:
        pool += string.digits
    if types["symbols"]:
        pool += string.punctuation
    return pool


def generate_password(length: int, types: dict) -> str:
    pool = build_character_pool(types)
    password = [random.choice(pool) for _ in range(length)]
    random.shuffle(password)
    return "".join(password)


def main():
    print("=" * 45)
    print("        RANDOM PASSWORD GENERATOR")
    print("=" * 45)

    while True:
        length = get_length()
        types = get_character_types()

        password = generate_password(length, types)

        print("\n" + "-" * 45)
        print(f"Generated password: {password}")
        print("-" * 45)

        again = input("\nGenerate another password? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye! Stay secure.")
            break
        print()


if __name__ == "__main__":
    main()
