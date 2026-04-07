#!/usr/bin/env python3

# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: NUMBER PATTERN ANALYZER
# QUESTION NO: 7


def get_numbers():
    """Get list of numbers from user."""
    print(f"\n{'-' * 50}")
    print("  Enter numbers separated by spaces or commas")
    print(f"{'-' * 50}")

    user_input = input("\n  Enter numbers: ").strip()

    if not user_input:
        print("  Error: No input provided.")
        return None

    user_input = user_input.replace(",", " ")
    numbers = []

    for item in user_input.split():
        try:
            numbers.append(float(item))
        except ValueError:
            print(f"  Warning: '{item}' is not a valid number. Skipping.")

    if not numbers:
        print("  Error: No valid numbers entered.")
        return None

    return numbers


def find_largest(numbers):
    """Find largest number."""
    largest = numbers[0]
    for num in numbers:
        if num > largest:
            largest = num
    return largest


def find_smallest(numbers):
    """Find smallest number."""
    smallest = numbers[0]
    for num in numbers:
        if num < smallest:
            smallest = num
    return smallest


def calculate_mean(numbers):
    """Calculate average."""
    return sum(numbers) / len(numbers)


def calculate_median(numbers):
    """Calculate middle value."""
    sorted_nums = sorted(numbers)
    n = len(sorted_nums)
    mid = n // 2

    if n % 2 == 0:
        return (sorted_nums[mid - 1] + sorted_nums[mid]) / 2
    return sorted_nums[mid]


def calculate_mode(numbers):
    """Find most frequently occurring number(s)."""
    frequency = {}
    for num in numbers:
        if num in frequency:
            frequency[num] += 1
        else:
            frequency[num] = 1

    max_count = 0
    for count in frequency.values():
        if count > max_count:
            max_count = count

    if max_count == 1:
        return None, frequency

    modes = []
    for num, count in frequency.items():
        if count == max_count:
            modes.append(num)

    return modes, frequency


def remove_duplicates(numbers):
    """Remove duplicates while preserving order."""
    seen = []
    unique = []
    for num in numbers:
        if num not in seen:
            seen.append(num)
            unique.append(num)
    return unique


def format_number(num):
    """Display number as int if whole, otherwise as float."""
    if num == int(num):
        return str(int(num))
    return f"{num:.2f}"


def display_list(title, numbers):
    """Display a list of numbers in rows of 10."""
    print(f"\n  {title}:")
    print("  ", end="")
    for i, num in enumerate(numbers):
        print(f"{format_number(num):>8}", end="")
        if (i + 1) % 10 == 0:
            print("\n  ", end="")
    print()


def display_results(numbers):
    """Display all analysis results."""

    largest = find_largest(numbers)
    smallest = find_smallest(numbers)
    mean = calculate_mean(numbers)
    median = calculate_median(numbers)
    modes, frequency = calculate_mode(numbers)
    unique = remove_duplicates(numbers)
    ascending = sorted(numbers)
    descending = sorted(numbers, reverse=True)

    print(f"\n{'=' * 55}")
    print("       NUMBER PATTERN ANALYSIS")
    print(f"{'=' * 55}")

    display_list("ORIGINAL LIST", numbers)

    print(f"\n{'-' * 55}")
    print("  BASIC STATISTICS")
    print(f"{'-' * 55}")
    print(f"  Total numbers entered: {len(numbers)}")
    print(f"  Unique numbers:        {len(unique)}")
    print(f"  Duplicates found:      {len(numbers) - len(unique)}")
    print(f"  Largest number:        {format_number(largest)}")
    print(f"  Smallest number:       {format_number(smallest)}")
    print(f"  Range:                 {format_number(largest - smallest)}")

    print(f"\n{'-' * 55}")
    print("  CENTRAL TENDENCY")
    print(f"{'-' * 55}")
    print(f"  Mean (Average):  {mean:.2f}")
    print(f"  Median (Middle): {format_number(median)}")

    if modes:
        mode_str = ", ".join(format_number(m) for m in modes)
        print(f"  Mode (Frequent): {mode_str}")
    else:
        print("  Mode (Frequent): No mode (all appear once)")

    print(f"\n{'-' * 55}")
    print("  FREQUENCY TABLE")
    print(f"{'-' * 55}")
    print(f"  {'Number':<15} {'Frequency':<15}")
    print(f"  {'-'*14:<15} {'-'*14:<15}")

    for num in sorted(frequency.keys()):
        print(f"  {format_number(num):<15} {frequency[num]:<15}")

    print(f"\n{'-' * 55}")
    print("  DUPLICATES REMOVED")
    print(f"{'-' * 55}")
    display_list("Unique numbers", unique)

    print(f"\n{'-' * 55}")
    print("  SORTED LISTS")
    print(f"{'-' * 55}")
    display_list("Ascending order", ascending)
    display_list("Descending order", descending)

    print(f"\n{'=' * 55}")
    print("  END OF ANALYSIS")
    print(f"{'=' * 55}")


def main():
    """Main entry point."""

    print(f"\n{'=' * 55}")
    print("       NUMBER PATTERN ANALYZER")
    print(f"{'=' * 55}")

    while True:
        numbers = get_numbers()

        if numbers:
            display_results(numbers)

        again = input("\n  Analyze another list? (y/n): ").strip().lower()
        if again != "y":
            print("\n  Goodbye!\n")
            break


if __name__ == "__main__":
    main()