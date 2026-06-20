"""
library.py

Defines the Library class, which manages collections of Book, Member,
and Loan objects, and handles all file input/output (loading from and
saving to CSV files).
"""

import csv
import os
from datetime import date

from book import Book
from member import Member
from loan import Loan


class Library:
    """
    Manages the overall library system: books, members, and loans.

    Attributes:
        books (dict): Maps ISBN (str) -> Book object.
        members (dict): Maps member_id (str) -> Member object.
        loans (dict): Maps loan_id (str) -> Loan object.
        data_folder (str): Path to the folder containing the CSV data files.
    """

    def __init__(self, data_folder="data"):
        """
        Initialise a new Library instance with empty collections, then
        attempt to load any existing data from the data folder.

        Args:
            data_folder (str): Folder path where CSV files are stored.
        """
        self.books = {}
        self.members = {}
        self.loans = {}
        self.data_folder = data_folder

        # Make sure the data folder exists so that file writes do not fail.
        os.makedirs(self.data_folder, exist_ok=True)

        self.load_all_data()

    # ------------------------------------------------------------------
    # Book-related methods
    # ------------------------------------------------------------------

    def add_book(self, isbn, title, author, total_copies):
        """
        Add a new book to the library's catalogue.

        Args:
            isbn (str): Unique ISBN for the book.
            title (str): Book title.
            author (str): Book author.
            total_copies (int): Number of copies to add.

        Raises:
            ValueError: If a book with this ISBN already exists, or if
                total_copies is not a positive integer.
        """
        if isbn in self.books:
            raise ValueError(f"A book with ISBN '{isbn}' already exists.")
        if total_copies <= 0:
            raise ValueError("total_copies must be a positive integer.")

        self.books[isbn] = Book(isbn, title, author, total_copies)

    def find_book(self, isbn):
        """
        Find a book by its ISBN.

        Args:
            isbn (str): ISBN to search for.

        Returns:
            Book: The matching Book object.

        Raises:
            KeyError: If no book with this ISBN exists.
        """
        if isbn not in self.books:
            raise KeyError(f"No book found with ISBN '{isbn}'.")
        return self.books[isbn]

    def search_books_by_title(self, keyword):
        """
        Search for books whose title contains the given keyword
        (case-insensitive).

        Args:
            keyword (str): Search term.

        Returns:
            list: A list of matching Book objects (empty if none found).
        """
        keyword = keyword.lower()
        return [book for book in self.books.values() if keyword in book.title.lower()]

    # ------------------------------------------------------------------
    # Member-related methods
    # ------------------------------------------------------------------

    def add_member(self, member_id, name, email):
        """
        Register a new member with the library.

        Args:
            member_id (str): Unique ID for the member.
            name (str): Member's full name.
            email (str): Member's email address.

        Raises:
            ValueError: If a member with this ID already exists.
        """
        if member_id in self.members:
            raise ValueError(f"A member with ID '{member_id}' already exists.")
        self.members[member_id] = Member(member_id, name, email)

    def find_member(self, member_id):
        """
        Find a member by their ID.

        Args:
            member_id (str): Member ID to search for.

        Returns:
            Member: The matching Member object.

        Raises:
            KeyError: If no member with this ID exists.
        """
        if member_id not in self.members:
            raise KeyError(f"No member found with ID '{member_id}'.")
        return self.members[member_id]

    # ------------------------------------------------------------------
    # Loan-related methods (borrowing and returning books)
    # ------------------------------------------------------------------

    def borrow_book(self, member_id, isbn):
        """
        Process a member borrowing a book: validates that the member
        and book exist and that a copy is available, then creates a
        new Loan record and updates the related Book and Member objects.

        Args:
            member_id (str): ID of the member borrowing the book.
            isbn (str): ISBN of the book to borrow.

        Returns:
            Loan: The newly created Loan object.

        Raises:
            KeyError: If the member or book does not exist.
            ValueError: If the book has no available copies.
        """
        member = self.find_member(member_id)
        book = self.find_book(isbn)

        # book.borrow_copy() raises ValueError if no copies are available;
        # that exception propagates up to the caller (main.py), which
        # catches it and displays a message to the user.
        book.borrow_copy()
        member.add_borrowed_book(isbn)

        loan_id = self._generate_loan_id()
        new_loan = Loan(loan_id, member_id, isbn)
        self.loans[loan_id] = new_loan
        return new_loan

    def return_book(self, loan_id):
        """
        Process the return of a borrowed book: marks the loan as
        returned and updates the related Book and Member objects.

        Args:
            loan_id (str): ID of the loan being returned.

        Returns:
            Loan: The updated Loan object.

        Raises:
            KeyError: If the loan does not exist.
            ValueError: If the loan was already marked as returned.
        """
        if loan_id not in self.loans:
            raise KeyError(f"No loan found with ID '{loan_id}'.")

        loan = self.loans[loan_id]
        loan.mark_returned()  # Raises ValueError if already returned.

        book = self.find_book(loan.isbn)
        member = self.find_member(loan.member_id)

        book.return_copy()
        member.remove_borrowed_book(loan.isbn)
        return loan

    def _generate_loan_id(self):
        """
        Generate a new unique loan ID based on the current count of loans.
        This is a private helper method (indicated by the leading underscore).

        Returns:
            str: A new loan ID, e.g. 'L004'.
        """
        return f"L{len(self.loans) + 1:03d}"

    # ------------------------------------------------------------------
    # File I/O methods (CSV read/write) with exception handling
    # ------------------------------------------------------------------

    def load_all_data(self):
        """
        Load books, members, and loans from their respective CSV files
        in self.data_folder. If a file does not exist yet (e.g. first
        run of the program), that collection simply starts empty rather
        than crashing the program.
        """
        self._load_books()
        self._load_members()
        self._load_loans()

    def _load_books(self):
        """Load book records from books.csv into self.books."""
        filepath = os.path.join(self.data_folder, "books.csv")
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    book = Book(
                        isbn=row["isbn"],
                        title=row["title"],
                        author=row["author"],
                        total_copies=int(row["total_copies"]),
                    )
                    # Preserve the saved availability rather than resetting it.
                    book.available_copies = int(row["available_copies"])
                    self.books[book.isbn] = book
        except FileNotFoundError:
            # No data yet; this is expected on the very first run.
            print(f"Note: '{filepath}' not found. Starting with an empty book catalogue.")
        except (csv.Error, KeyError, ValueError) as error:
            # Handles malformed CSV rows or missing/invalid columns.
            print(f"Warning: Could not fully read '{filepath}' due to a data error: {error}")

    def _load_members(self):
        """Load member records from members.csv into self.members."""
        filepath = os.path.join(self.data_folder, "members.csv")
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    borrowed = row["borrowed_isbns"].split(";") if row["borrowed_isbns"] else []
                    member = Member(
                        member_id=row["member_id"],
                        name=row["name"],
                        email=row["email"],
                        borrowed_isbns=borrowed,
                    )
                    self.members[member.member_id] = member
        except FileNotFoundError:
            print(f"Note: '{filepath}' not found. Starting with an empty member list.")
        except (csv.Error, KeyError) as error:
            print(f"Warning: Could not fully read '{filepath}' due to a data error: {error}")

    def _load_loans(self):
        """Load loan records from loans.csv into self.loans."""
        filepath = os.path.join(self.data_folder, "loans.csv")
        try:
            with open(filepath, mode="r", newline="", encoding="utf-8") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    returned_text = row["return_date"]
                    returned_date = date.fromisoformat(returned_text) if returned_text else None
                    loan = Loan(
                        loan_id=row["loan_id"],
                        member_id=row["member_id"],
                        isbn=row["isbn"],
                        borrow_date=date.fromisoformat(row["borrow_date"]),
                        return_date=returned_date,
                    )
                    self.loans[loan.loan_id] = loan
        except FileNotFoundError:
            print(f"Note: '{filepath}' not found. Starting with an empty loan history.")
        except (csv.Error, KeyError, ValueError) as error:
            print(f"Warning: Could not fully read '{filepath}' due to a data error: {error}")

    def save_all_data(self):
        """
        Save the current state of books, members, and loans to their
        respective CSV files in self.data_folder.
        """
        self._save_books()
        self._save_members()
        self._save_loans()

    def _save_books(self):
        """Write all Book records to books.csv."""
        filepath = os.path.join(self.data_folder, "books.csv")
        fieldnames = ["isbn", "title", "author", "total_copies", "available_copies"]
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for book in self.books.values():
                    writer.writerow(book.to_dict())
        except OSError as error:
            print(f"Error: Could not save book data to '{filepath}': {error}")

    def _save_members(self):
        """Write all Member records to members.csv."""
        filepath = os.path.join(self.data_folder, "members.csv")
        fieldnames = ["member_id", "name", "email", "borrowed_isbns"]
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for member in self.members.values():
                    writer.writerow(member.to_dict())
        except OSError as error:
            print(f"Error: Could not save member data to '{filepath}': {error}")

    def _save_loans(self):
        """Write all Loan records to loans.csv."""
        filepath = os.path.join(self.data_folder, "loans.csv")
        fieldnames = ["loan_id", "member_id", "isbn", "borrow_date", "return_date"]
        try:
            with open(filepath, mode="w", newline="", encoding="utf-8") as file:
                writer = csv.DictWriter(file, fieldnames=fieldnames)
                writer.writeheader()
                for loan in self.loans.values():
                    writer.writerow(loan.to_dict())
        except OSError as error:
            print(f"Error: Could not save loan data to '{filepath}': {error}")
