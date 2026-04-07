#!/usr/bin/env python3

# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: SORTING ALGORITHM EFFICIENCY ANALYZER
# QUESTION NO: 4
import random
import time


def generate_random_integers(count=100, low=1, high=1000):
    """Generate a list of random integers."""
    return [random.randint(low, high) for _ in range(count)]


def bubble_sort(arr):
    """Bubble Sort: Repeatedly swaps adjacent elements if in wrong order."""
    data = arr.copy()
    n = len(data)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if data[j] > data[j + 1]:
                data[j], data[j + 1] = data[j + 1], data[j]
                swapped = True
        # If no swaps occurred, list is already sorted
        if not swapped:
            break

    return data


def selection_sort(arr):
    """Selection Sort: Finds minimum element and places it at beginning."""
    data = arr.copy()
    n = len(data)

    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if data[j] < data[min_index]:
                min_index = j
        data[i], data[min_index] = data[min_index], data[i]

    return data


def merge_sort(arr):
    """Merge Sort: Divides array in half, sorts each half, then merges."""
    data = arr.copy()

    if len(data) <= 1:
        return data

    mid = len(data) // 2
    left = merge_sort(data[:mid])
    right = merge_sort(data[mid:])

    return merge(left, right)


def merge(left, right):
    """Merge two sorted lists into one sorted list."""
    result = []
    i = 0
    j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])

    return result


def measure_time(sort_function, data):
    """Measure execution time of a sorting function."""
    start_time = time.perf_counter()
    sorted_data = sort_function(data)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time

    return sorted_data, elapsed_time


def display_list(title, data, per_row=10):
    """Display a list of numbers in formatted rows."""
    print(f"\n  {title}:")
    print("  ", end="")
    for i, num in enumerate(data):
        print(f"{num:5}", end="")
        if (i + 1) % per_row == 0:
            print("\n  ", end="")
    print()


def display_results(original, results):
    """Display all sorting results."""

    print("=" * 70)
    print("       SORTING ALGORITHM EFFICIENCY ANALYSIS")
    print("=" * 70)

    # Display original unsorted list
    display_list("ORIGINAL UNSORTED LIST", original)

    print("\n" + "-" * 70)
    print("  SORTING RESULTS")
    print("-" * 70)

    # Display each algorithm's result
    for name, sorted_data, elapsed_time in results:
        print(f"\n  Algorithm: {name}")
        print(f"  Time Taken: {elapsed_time:.6f} seconds")
        display_list(f"Sorted List ({name})", sorted_data)
        print("-" * 70)

    # Time comparison
    print("\n" + "=" * 70)
    print("  TIME COMPARISON")
    print("=" * 70)
    print(f"\n  {'Algorithm':<20} {'Time (seconds)':<20} {'Relative Speed':<15}")
    print(f"  {'-'*19:<20} {'-'*19:<20} {'-'*14:<15}")

    # Find fastest time for relative comparison
    fastest_time = min(results, key=lambda x: x[2])[2]

    for name, _, elapsed_time in results:
        if fastest_time > 0:
            relative = elapsed_time / fastest_time
            relative_str = f"{relative:.2f}x"
        else:
            relative_str = "N/A"
        print(f"  {name:<20} {elapsed_time:<20.6f} {relative_str:<15}")

    # Determine fastest algorithm
    fastest = min(results, key=lambda x: x[2])
    slowest = max(results, key=lambda x: x[2])

    print("\n" + "=" * 70)
    print("  CONCLUSION")
    print("=" * 70)
    print(f"\n  Fastest Algorithm: {fastest[0]} ({fastest[2]:.6f} seconds)")
    print(f"  Slowest Algorithm: {slowest[0]} ({slowest[2]:.6f} seconds)")

    if fastest[2] > 0:
        speedup = slowest[2] / fastest[2]
        print(f"\n  {fastest[0]} is {speedup:.2f}x faster than {slowest[0]}")

    # Time complexity reference
    print("\n" + "-" * 70)
    print("  ALGORITHM TIME COMPLEXITY REFERENCE")
    print("-" * 70)
    print(f"  {'Algorithm':<20} {'Best':<15} {'Average':<15} {'Worst':<15}")
    print(f"  {'-'*19:<20} {'-'*14:<15} {'-'*14:<15} {'-'*14:<15}")
    print(f"  {'Bubble Sort':<20} {'O(n)':<15} {'O(n²)':<15} {'O(n²)':<15}")
    print(f"  {'Selection Sort':<20} {'O(n²)':<15} {'O(n²)':<15} {'O(n²)':<15}")
    print(f"  {'Merge Sort':<20} {'O(n log n)':<15} {'O(n log n)':<15} {'O(n log n)':<15}")

    print("\n" + "=" * 70)
    print("  END OF ANALYSIS")
    print("=" * 70)


def verify_sorting(original, results):
    """Verify all algorithms produced correct results."""
    expected = sorted(original)

    print("\n  VERIFICATION:")
    for name, sorted_data, _ in results:
        is_correct = sorted_data == expected
        status = "PASS" if is_correct else "FAIL"
        print(f"  {name}: {status}")


def main():
    # Generate random integers
    print("\nGenerating 100 random integers...")
    original = generate_random_integers(100, 1, 1000)

    # Define sorting algorithms
    algorithms = [
        ("Bubble Sort", bubble_sort),
        ("Selection Sort", selection_sort),
        ("Merge Sort", merge_sort),
    ]

    # Measure each algorithm
    results = []
    for name, sort_func in algorithms:
        print(f"Running {name}...")
        sorted_data, elapsed_time = measure_time(sort_func, original)
        results.append((name, sorted_data, elapsed_time))

    # Display results
    display_results(original, results)

    # Verify correctness
    verify_sorting(original, results)


if __name__ == "__main__":
    main()