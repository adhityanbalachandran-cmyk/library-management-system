"""
loan.py

Defines the Loan class, which represents a single borrowing record
linking a Member to a Book.
"""

from datetime import date


class Loan:
    """
    Represents a record of one book being borrowed by one member.

    Attributes:
        loan_id (str): Unique identifier for this loan record.
        member_id (str): ID of the member who borrowed the book.
        isbn (str): ISBN of the borrowed book.
        borrow_date (date): The date the book was borrowed.
        return_date (date or None): The date the book was returned,
            or None if it has not been returned yet.
    """

    def __init__(self, loan_id, member_id, isbn, borrow_date=None, return_date=None):
        """
        Initialise a new Loan instance.

        Args:
            loan_id (str): Unique ID for this loan.
            member_id (str): ID of the borrowing member.
            isbn (str): ISBN of the book being borrowed.
            borrow_date (date, optional): Date borrowed. Defaults to today.
            return_date (date, optional): Date returned, if already known.
        """
        self.loan_id = loan_id
        self.member_id = member_id
        self.isbn = isbn
        self.borrow_date = borrow_date if borrow_date else date.today()
        self.return_date = return_date

    def is_returned(self):
        """
        Check whether this loan has been marked as returned.

        Returns:
            bool: True if return_date is set, otherwise False.
        """
        return self.return_date is not None

    def mark_returned(self, return_date=None):
        """
        Mark this loan as returned on a given date (defaults to today).

        Args:
            return_date (date, optional): The date of return.

        Raises:
            ValueError: If the loan has already been marked as returned.
        """
        if self.is_returned():
            raise ValueError(f"Loan {self.loan_id} has already been returned.")
        self.return_date = return_date if return_date else date.today()

    def to_dict(self):
        """
        Convert the Loan object into a dictionary, used when writing
        this loan's data to a CSV file. Dates are converted to ISO
        format strings (YYYY-MM-DD) since CSV cells store plain text.

        Returns:
            dict: A dictionary representation of the loan's fields.
        """
        return {
            "loan_id": self.loan_id,
            "member_id": self.member_id,
            "isbn": self.isbn,
            "borrow_date": self.borrow_date.isoformat(),
            "return_date": self.return_date.isoformat() if self.return_date else "",
        }

    def __str__(self):
        """
        Return a human-readable string representation of the loan,
        used when displaying loan details in the menu interface.
        """
        status = f"Returned on {self.return_date}" if self.is_returned() else "On loan"
        return (f"Loan ID: {self.loan_id} | Member: {self.member_id} | ISBN: {self.isbn} | "
                f"Borrowed: {self.borrow_date} | Status: {status}")
