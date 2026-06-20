"""
book.py

Defines the Book class, which represents a single book record
in the Library Management System.
"""


class Book:
    """
    Represents a book held by the library.

    Attributes:
        isbn (str): Unique identifier for the book (used as its key).
        title (str): Title of the book.
        author (str): Author of the book.
        total_copies (int): Total number of copies the library owns.
        available_copies (int): Number of copies currently available
            to borrow (i.e., not currently on loan).
    """

    def __init__(self, isbn, title, author, total_copies):
        """
        Initialise a new Book instance.

        Args:
            isbn (str): Unique ISBN/code for the book.
            title (str): Title of the book.
            author (str): Author's name.
            total_copies (int): Total copies owned by the library.
        """
        self.isbn = isbn
        self.title = title
        self.author = author
        self.total_copies = int(total_copies)
        # When a book is first added, all copies are available.
        self.available_copies = int(total_copies)

    def is_available(self):
        """
        Check whether at least one copy of the book can be borrowed.

        Returns:
            bool: True if available_copies > 0, otherwise False.
        """
        return self.available_copies > 0

    def borrow_copy(self):
        """
        Decrease available_copies by one when a copy is borrowed.

        Raises:
            ValueError: If there are no available copies to borrow.
        """
        if not self.is_available():
            raise ValueError(f"No available copies of '{self.title}' to borrow.")
        self.available_copies -= 1

    def return_copy(self):
        """
        Increase available_copies by one when a copy is returned.

        Raises:
            ValueError: If returning the copy would exceed total_copies
                (this would indicate a data inconsistency).
        """
        if self.available_copies >= self.total_copies:
            raise ValueError(f"All copies of '{self.title}' are already marked as returned.")
        self.available_copies += 1

    def to_dict(self):
        """
        Convert the Book object into a dictionary, used when writing
        this book's data to a CSV file.

        Returns:
            dict: A dictionary representation of the book's fields.
        """
        return {
            "isbn": self.isbn,
            "title": self.title,
            "author": self.author,
            "total_copies": self.total_copies,
            "available_copies": self.available_copies,
        }

    def __str__(self):
        """
        Return a human-readable string representation of the book,
        used when displaying book details in the menu interface.
        """
        return (f"ISBN: {self.isbn} | Title: {self.title} | Author: {self.author} | "
                f"Available: {self.available_copies}/{self.total_copies}")
