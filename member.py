"""
member.py

Defines the Member class, which represents a library member
(a person registered to borrow books).
"""


class Member:
    """
    Represents a registered library member.

    Attributes:
        member_id (str): Unique identifier for the member.
        name (str): Full name of the member.
        email (str): Contact email address of the member.
        borrowed_isbns (list): List of ISBNs the member currently has
            on loan.
    """

    def __init__(self, member_id, name, email, borrowed_isbns=None):
        """
        Initialise a new Member instance.

        Args:
            member_id (str): Unique ID for the member.
            name (str): Member's full name.
            email (str): Member's email address.
            borrowed_isbns (list, optional): ISBNs already on loan to
                this member. Defaults to an empty list.
        """
        self.member_id = member_id
        self.name = name
        self.email = email
        self.borrowed_isbns = borrowed_isbns if borrowed_isbns is not None else []

    def has_borrowed(self, isbn):
        """
        Check whether this member currently has a specific book on loan.

        Args:
            isbn (str): ISBN to check for.

        Returns:
            bool: True if the ISBN is in this member's borrowed list.
        """
        return isbn in self.borrowed_isbns

    def add_borrowed_book(self, isbn):
        """
        Record that this member has borrowed a book with the given ISBN.

        Args:
            isbn (str): ISBN of the borrowed book.
        """
        self.borrowed_isbns.append(isbn)

    def remove_borrowed_book(self, isbn):
        """
        Remove a book from this member's borrowed list (on return).

        Args:
            isbn (str): ISBN of the book being returned.

        Raises:
            ValueError: If the member's record does not contain this ISBN.
        """
        if isbn not in self.borrowed_isbns:
            raise ValueError(f"{self.name} does not currently have this book on loan.")
        self.borrowed_isbns.remove(isbn)

    def to_dict(self):
        """
        Convert the Member object into a dictionary, used when writing
        this member's data to a CSV file.

        Returns:
            dict: A dictionary representation of the member's fields.
            The borrowed_isbns list is joined into a single string
            (separated by semicolons) since CSV cells store plain text.
        """
        return {
            "member_id": self.member_id,
            "name": self.name,
            "email": self.email,
            "borrowed_isbns": ";".join(self.borrowed_isbns),
        }

    def __str__(self):
        """
        Return a human-readable string representation of the member,
        used when displaying member details in the menu interface.
        """
        borrowed = ", ".join(self.borrowed_isbns) if self.borrowed_isbns else "None"
        return (f"ID: {self.member_id} | Name: {self.name} | Email: {self.email} | "
                f"Borrowed: {borrowed}")
