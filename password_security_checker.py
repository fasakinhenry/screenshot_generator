# TITLE: PASSWORD SECURITY CHECKER
# QUESTION NO: 5

def check_password(password):
    """Analyze password and return checks, strength, score, suggestions."""

    special_chars = "!@#$%^&*()_+-=[]{}|;:',.<>?/~`"
    common = ["password", "12345678", "qwerty123", "admin123",
              "letmein1", "welcome1", "password1", "iloveyou"]
    # Run all checks
    checks = {
        "Minimum 8 characters": len(password) >= 8,
        "Contains uppercase": any(c.isupper() for c in password),
        "Contains lowercase": any(c.islower() for c in password),
        "Contains digit": any(c.isdigit() for c in password),
        "Contains special char": any(c in special_chars for c in password),
        "Not common password": password.lower() not in common,}
    passed = sum(checks.values())
    # Classification
    if passed >= 5 and len(password) >= 12:
        strength, score = "STRONG", 100
    elif passed >= 3:
        strength, score = "MODERATE", 60
    else:
        strength, score = "WEAK", 25
    # Suggestions
    suggestions = [name for name, result in checks.items() if not result]
    if len(password) < 12:
        suggestions.append("Consider 12+ characters for better security")
    return checks, strength, score, suggestions


def display_results(password, checks, strength, score, suggestions):
    """Display password analysis results."""

    print(f"\n{'=' * 55}")
    print("       PASSWORD STRENGTH ANALYSIS")
    print(f"{'=' * 55}")
    print(f"\n  Password:  {password}")
    print(f"  Length:    {len(password)} characters")
    print(f"  Strength: {strength}")
    print(f"  Score:     {score}/100")

def main():
    while True:
        password = input("\n  Enter password (or 'quit'): ")
        if password.lower() == "quit":
            print("\n  Goodbye!")
            break
        if not password:
            print("  Error: Password cannot be empty.")
            continue
        checks, strength, score, suggestions = check_password(password)
        display_results(password, checks, strength, score, suggestions)
        break

if __name__ == "__main__":
    main()