#!/usr/bin/env python3

# NAME:
# MATRIC NO:
# DEPARTMENT:
# TITLE: LIBRARY MANAGEMENT MINI SYSTEM
# QUESTION NO: 6

import json
import os

DATA_FILE = "library_data.json"

def load_books():
    """Load books from file."""
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_books(books):
    """Save books to file."""
    with open(DATA_FILE, "w") as f:
        json.dump(books, f, indent=4)


def add_book(books):
    """Add a new book to the library."""
    print(f"\n{'-' * 45}")
    print("  ADD NEW BOOK")
    print(f"{'-' * 45}")

    title = input("  Enter title: ").strip()
    author = input("  Enter author: ").strip()
    isbn = input("  Enter ISBN: ").strip()
    copies = input("  Enter number of copies: ").strip()

    if not title or not author or not isbn or not copies:
        print("\n  Error: All fields are required.")
        return

    if not copies.isdigit() or int(copies) < 1:
        print("\n  Error: Copies must be a positive number.")
        return

    if isbn in books:
        print(f"\n  Book with ISBN '{isbn}' already exists.")
        print(f"  Current copies: {books[isbn]['copies']}")
        add_more = input("  Add more copies? (y/n): ").strip().lower()
        if add_more == "y":
            books[isbn]["copies"] += int(copies)
            save_books(books)
            print(f"  Updated! Total copies: {books[isbn]['copies']}")
        return

    books[isbn] = {
        "title": title,
        "author": author,
        "isbn": isbn,
        "copies": int(copies),
        "borrowed": 0,
    }

    save_books(books)
    print(f"\n  Book '{title}' added successfully!")


def search_book(books):
    """Search for a book by title, author, or ISBN."""
    print(f"\n{'-' * 45}")
    print("  SEARCH BOOK")
    print(f"{'-' * 45}")

    if not books:
        print("\n  Library is empty.")
        return

    query = input("  Enter title, author, or ISBN: ").strip().lower()

    if not query:
        print("\n  Error: Search query cannot be empty.")
        return

    found = []
    for isbn, book in books.items():
        if (query in book["title"].lower() or
                query in book["author"].lower() or
                query in isbn.lower()):
            found.append(book)

    if not found:
        print(f"\n  No books found matching '{query}'.")
        return

    print(f"\n  Found {len(found)} book(s):\n")
    print(f"  {'Title':<25} {'Author':<20} {'ISBN':<15} {'Available':<10}")
    print(f"  {'-'*24:<25} {'-'*19:<20} {'-'*14:<15} {'-'*9:<10}")

    for book in found:
        available = book["copies"] - book["borrowed"]
        print(f"  {book['title']:<25} {book['author']:<20} {book['isbn']:<15} {available:<10}")


def borrow_book(books):
    """Borrow a book from the library."""
    print(f"\n{'-' * 45}")
    print("  BORROW BOOK")
    print(f"{'-' * 45}")

    if not books:
        print("\n  Library is empty.")
        return

    isbn = input("  Enter ISBN of book to borrow: ").strip()

    if isbn not in books:
        print(f"\n  No book found with ISBN '{isbn}'.")
        return

    book = books[isbn]
    available = book["copies"] - book["borrowed"]

    if available <= 0:
        print(f"\n  Sorry! '{book['title']}' has no copies available.")
        print(f"  Total copies: {book['copies']}")
        print(f"  Currently borrowed: {book['borrowed']}")
        return

    book["borrowed"] += 1
    save_books(books)
    available -= 1

    print(f"\n  Book borrowed successfully!")
    print(f"  Title: {book['title']}")
    print(f"  Author: {book['author']}")
    print(f"  Remaining copies: {available}")


def return_book(books):
    """Return a borrowed book."""
    print(f"\n{'-' * 45}")
    print("  RETURN BOOK")
    print(f"{'-' * 45}")

    if not books:
        print("\n  Library is empty.")
        return

    isbn = input("  Enter ISBN of book to return: ").strip()

    if isbn not in books:
        print(f"\n  No book found with ISBN '{isbn}'.")
        return

    book = books[isbn]

    if book["borrowed"] <= 0:
        print(f"\n  No copies of '{book['title']}' are currently borrowed.")
        return

    book["borrowed"] -= 1
    save_books(books)
    available = book["copies"] - book["borrowed"]

    print(f"\n  Book returned successfully!")
    print(f"  Title: {book['title']}")
    print(f"  Available copies: {available}")


def display_all(books):
    """Display all books in the library."""
    print(f"\n{'=' * 70}")
    print("  LIBRARY CATALOG")
    print(f"{'=' * 70}")

    if not books:
        print("\n  Library is empty.")
        return

    print(f"\n  {'Title':<25} {'Author':<20} {'ISBN':<15} {'Total':<7} {'Available':<10}")
    print(f"  {'-'*24:<25} {'-'*19:<20} {'-'*14:<15} {'-'*6:<7} {'-'*9:<10}")

    for isbn, book in books.items():
        available = book["copies"] - book["borrowed"]
        print(f"  {book['title']:<25} {book['author']:<20} {isbn:<15} {book['copies']:<7} {available:<10}")

    print(f"\n  Total books: {len(books)}")
    total_copies = sum(b["copies"] for b in books.values())
    total_borrowed = sum(b["borrowed"] for b in books.values())
    print(f"  Total copies: {total_copies}")
    print(f"  Total borrowed: {total_borrowed}")
    print(f"  Total available: {total_copies - total_borrowed}")

    print(f"{'=' * 70}")


def show_menu():
    """Display menu and return user choice."""
    print(f"\n{'=' * 45}")
    print("  LIBRARY MANAGEMENT SYSTEM")
    print(f"{'=' * 45}")
    print("  1. Add a new book")
    print("  2. Search for a book")
    print("  3. Borrow a book")
    print("  4. Return a book")
    print("  5. Display all books")
    print("  6. Exit")
    print(f"{'-' * 45}")

    return input("  Enter your choice (1-6): ").strip()


def main():
    """Main entry point."""

    # Load existing books
    books = load_books()

    # Preload sample data if library is empty
    if not books:
        books = {
            "978-0-13-468599-1": {
                "title": "The Pragmatic Programmer",
                "author": "David Thomas",
                "isbn": "978-0-13-468599-1",
                "copies": 5,
                "borrowed": 1,
            },
            "978-0-59-651798-7": {
                "title": "Head First Python",
                "author": "Paul Barry",
                "isbn": "978-0-59-651798-7",
                "copies": 3,
                "borrowed": 0,
            },
            "978-0-13-235088-4": {
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "isbn": "978-0-13-235088-4",
                "copies": 4,
                "borrowed": 2,
            },
            "978-0-20-161622-4": {
                "title": "The Pragmatic Programmer",
                "author": "Andrew Hunt",
                "isbn": "978-0-20-161622-4",
                "copies": 2,
                "borrowed": 2,
            },
            "978-1-49-195016-0": {
                "title": "Python Crash Course",
                "author": "Eric Matthes",
                "isbn": "978-1-49-195016-0",
                "copies": 6,
                "borrowed": 1,
            },
        }
        save_books(books)

    while True:
        choice = show_menu()

        if choice == "1":
            add_book(books)
        elif choice == "2":
            search_book(books)
        elif choice == "3":
            borrow_book(books)
        elif choice == "4":
            return_book(books)
        elif choice == "5":
            display_all(books)
        elif choice == "6":
            save_books(books)
            print("\n  Books saved. Goodbye!\n")
            break
        else:
            print("\n  Invalid choice. Please enter 1-6.")


if __name__ == "__main__":
    main()