#!/usr/bin/env python3
# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: TEXT ANALYSIS SYSTEM
# QUESTION NO: 3

import os
import sys
import re


def read_file(filepath):
    """Read file and return contents."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: File '{filepath}' not found.")
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied to read '{filepath}'.")
        sys.exit(1)
    except UnicodeDecodeError:
        print(f"Error: Unable to decode '{filepath}'. Make sure it's a text file.")
        sys.exit(1)


def count_lines(content):
    """Count total number of lines."""
    if not content:
        return 0
    return content.count('\n') + (1 if not content.endswith('\n') else 0)


def count_words(content):
    """Count total number of words."""
    return len(content.split())


def count_characters(content):
    """Count characters with and without spaces."""
    total = len(content)
    no_spaces = len(content.replace(' ', '').replace('\n', '').replace('\t', ''))
    return total, no_spaces


def get_word_frequencies(content):
    """Count word frequencies using a dictionary."""
    words = re.findall(r'[a-zA-Z0-9]+', content.lower())

    if not words:
        return {}, None, 0

    # Count frequencies manually
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    # Find most frequent word
    most_common_word = max(word_counts, key=word_counts.get)
    most_common_count = word_counts[most_common_word]

    return word_counts, most_common_word, most_common_count


def get_top_words(word_counts, n=10):
    """Get top N most frequent words."""
    sorted_words = sorted(word_counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_words[:n]


def generate_report(filepath, total_lines, total_words, total_chars,
                    total_chars_no_spaces, most_common_word,
                    most_common_count, word_counts):
    """Generate formatted analysis report."""

    report = []
    report.append("=" * 60)
    report.append("           TEXT FILE ANALYSIS REPORT")
    report.append("=" * 60)
    report.append("")
    report.append(f"  File Analyzed: {filepath}")
    report.append(f"  File Size:     {os.path.getsize(filepath)} bytes")
    report.append("")
    report.append("-" * 60)
    report.append("  BASIC STATISTICS")
    report.append("-" * 60)
    report.append(f"  Total Lines:                    {total_lines}")
    report.append(f"  Total Words:                    {total_words}")
    report.append(f"  Total Characters (with spaces): {total_chars}")
    report.append(f"  Total Characters (no spaces):   {total_chars_no_spaces}")
    report.append("")
    report.append("-" * 60)
    report.append("  MOST FREQUENT WORD")
    report.append("-" * 60)

    if most_common_word:
        report.append(f'  Word:       "{most_common_word}"')
        report.append(f"  Frequency:  {most_common_count} times")
        report.append("")
        report.append("-" * 60)
        report.append("  TOP 10 MOST FREQUENT WORDS")
        report.append("-" * 60)
        report.append(f"  {'Rank':<6} {'Word':<20} {'Count':<10} {'Percentage':<10}")
        report.append(f"  {'-'*5:<6} {'-'*19:<20} {'-'*9:<10} {'-'*9:<10}")

        for rank, (word, count) in enumerate(get_top_words(word_counts), 1):
            percentage = (count / total_words) * 100 if total_words > 0 else 0
            report.append(f"  {rank:<6} {word:<20} {count:<10} {percentage:.2f}%")
    else:
        report.append("  No words found in the file.")

    report.append("")
    report.append("=" * 60)
    report.append("           END OF REPORT")
    report.append("=" * 60)

    return "\n".join(report)


def save_report(report, output_file="analysis_report.txt"):
    """Save report to file."""
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(report)
        return True
    except (PermissionError, IOError) as e:
        print(f"Error writing report: {e}")
        return False


def main():
    """Main entry point."""

    # Get file path
    if len(sys.argv) > 1:
        filepath = sys.argv[1]
    else:
        filepath = input("Enter the path to the text file: ").strip()

    if not filepath:
        print("Error: No file path provided.")
        sys.exit(1)

    filepath = filepath.strip('"').strip("'")

    if not os.path.isfile(filepath):
        print(f"Error: '{filepath}' is not a valid file.")
        sys.exit(1)

    # Read and analyze
    print(f"\nReading file: {filepath}")
    content = read_file(filepath)

    print("Analyzing...")
    total_lines = count_lines(content)
    total_words = count_words(content)
    total_chars, total_chars_no_spaces = count_characters(content)
    word_counts, most_common_word, most_common_count = get_word_frequencies(content)

    # Generate and display report
    report = generate_report(
        filepath, total_lines, total_words, total_chars,
        total_chars_no_spaces, most_common_word,
        most_common_count, word_counts
    )
    print("\n" + report)

    # Save report
    output_file = "analysis_report.txt"
    if save_report(report, output_file):
        print(f"\nReport saved to: {output_file}")
    else:
        print("\nFailed to save report.")


if __name__ == "__main__":
    main()