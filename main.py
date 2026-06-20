"""
main.py

Entry point for the Library Management System.
Provides a menu-driven, interactive command-line interface that lets
the user manage books, members, and loans.

Run with:
    python main.py
"""

from library import Library


def print_menu():
    """Display the main menu options to the user."""
    print("\n===== Library Management System =====")
    print("1. Add a new book")
    print("2. Add a new member")
    print("3. Borrow a book")
    print("4. Return a book")
    print("5. View all books")
    print("6. View all members")
    print("7. View all loans")
    print("8. Search books by title")
    print("0. Save and Exit")
    print("=======================================")


def handle_add_book(library):
    """
    Prompt the user for new book details and add the book to the library.

    Args:
        library (Library): The active Library instance.
    """
    print("\n-- Add a New Book --")
    isbn = input("Enter ISBN: ").strip()
    title = input("Enter title: ").strip()
    author = input("Enter author: ").strip()

    try:
        total_copies = int(input("Enter total copies: ").strip())
        library.add_book(isbn, title, author, total_copies)
        print(f"Success: '{title}' was added with {total_copies} copies.")
    except ValueError as error:
        # Catches both invalid number input (int() failure) and
        # business-rule violations raised inside add_book().
        print(f"Error: Could not add book. {error}")


def handle_add_member(library):
    """
    Prompt the user for new member details and register the member.

    Args:
        library (Library): The active Library instance.
    """
    print("\n-- Add a New Member --")
    member_id = input("Enter member ID: ").strip()
    name = input("Enter member name: ").strip()
    email = input("Enter member email: ").strip()

    try:
        library.add_member(member_id, name, email)
        print(f"Success: Member '{name}' was registered with ID '{member_id}'.")
    except ValueError as error:
        print(f"Error: Could not add member. {error}")


def handle_borrow_book(library):
    """
    Prompt the user for a member ID and an ISBN, then process the loan.

    Args:
        library (Library): The active Library instance.
    """
    print("\n-- Borrow a Book --")
    member_id = input("Enter member ID: ").strip()
    isbn = input("Enter book ISBN: ").strip()

    try:
        loan = library.borrow_book(member_id, isbn)
        print(f"Success: Loan created -> {loan}")
    except KeyError as error:
        # Member or book ID did not exist.
        print(f"Error: {error}")
    except ValueError as error:
        # Book has no available copies.
        print(f"Error: {error}")


def handle_return_book(library):
    """
    Prompt the user for a loan ID and process the return.

    Args:
        library (Library): The active Library instance.
    """
    print("\n-- Return a Book --")
    loan_id = input("Enter loan ID: ").strip()

    try:
        loan = library.return_book(loan_id)
        print(f"Success: Loan returned -> {loan}")
    except KeyError as error:
        print(f"Error: {error}")
    except ValueError as error:
        print(f"Error: {error}")


def handle_view_books(library):
    """Display all books currently in the catalogue."""
    print("\n-- All Books --")
    if not library.books:
        print("No books in the catalogue yet.")
        return
    for book in library.books.values():
        print(book)


def handle_view_members(library):
    """Display all registered members."""
    print("\n-- All Members --")
    if not library.members:
        print("No members registered yet.")
        return
    for member in library.members.values():
        print(member)


def handle_view_loans(library):
    """Display all loan records (active and returned)."""
    print("\n-- All Loans --")
    if not library.loans:
        print("No loan records yet.")
        return
    for loan in library.loans.values():
        print(loan)


def handle_search_books(library):
    """Prompt for a keyword and display matching books."""
    print("\n-- Search Books by Title --")
    keyword = input("Enter a keyword to search for: ").strip()
    results = library.search_books_by_title(keyword)

    if not results:
        print(f"No books found matching '{keyword}'.")
        return

    print(f"Found {len(results)} matching book(s):")
    for book in results:
        print(book)


def main():
    """
    Main program loop: initialises the Library, displays the menu
    repeatedly, and dispatches user choices to the relevant handler
    functions until the user chooses to exit.
    """
    library = Library(data_folder="data")

    # Maps each menu option (as a string) to the function that handles it.
    menu_actions = {
        "1": handle_add_book,
        "2": handle_add_member,
        "3": handle_borrow_book,
        "4": handle_return_book,
        "5": handle_view_books,
        "6": handle_view_members,
        "7": handle_view_loans,
        "8": handle_search_books,
    }

    while True:
        print_menu()
        choice = input("Enter your choice: ").strip()

        if choice == "0":
            library.save_all_data()
            print("Data saved. Goodbye!")
            break
        elif choice in menu_actions:
            # Look up and call the matching handler function.
            menu_actions[choice](library)
        else:
            print("Invalid choice. Please select a valid menu option.")


if __name__ == "__main__":
    main()
