# Library Management System

## Project Title and Purpose

The Library Management System is a Python-based command-line application designed for small and medium-sized libraries. The system helps library staff manage books, register members, and track book borrowing and returning activities.

All information is stored in CSV files, allowing data to remain saved even after the program is closed. The project was developed as part of the B100 Introduction to Computer Programming with Python assignment and demonstrates the use of object-oriented programming, file handling, exception handling, control structures, and modular programming.

## Features

The system provides the following features:

* Add new books to the library catalogue.
* Support multiple copies of the same book.
* Register new library members.
* Borrow books if copies are available.
* Return borrowed books.
* View all books in the catalogue.
* View registered members.
* View borrowing records.
* Search for books by title.
* Automatically save and load data using CSV files.

## Project Structure

The project is divided into multiple Python files to keep the code organised and easy to maintain.

**main.py**

* The main program file.
* Displays the menu and handles user interaction.

**library.py**

* Contains the Library class.
* Manages books, members, loans, and file operations.

**book.py**

* Contains the Book class.
* Stores information about each book and its availability.

**member.py**

* Contains the Member class.
* Stores member details.

**loan.py**

* Contains the Loan class.
* Stores information about book borrowing and returning.

**books.csv**

* Stores book information.

**members.csv**

* Stores member information.

**loans.csv**

* Stores loan records.

## Installation

To run the system, Python 3.8 or a later version must be installed on the computer.

No external libraries are required because the project only uses Python's built-in modules such as:

* csv
* os
* datetime

Download or copy the project files into a folder and ensure all Python files and CSV files are placed in the correct locations.

## Running the Program

Open a terminal or command prompt and navigate to the project folder.

Run the program using the following command:

python3 main.py

The system will display a menu with different options. Users can enter the number of the required action and follow the instructions shown on the screen.

## Example of System Operation

When a member borrows a book, the user enters the member ID and book ISBN. If a copy is available, the system creates a loan record and updates the available copies of the book.

Example:

Member ID: M001

Book ISBN: 9780132350884

Result:

Loan ID: L001

Member: M001

ISBN: 9780132350884

Status: On Loan

The borrowing information is automatically saved in the loan records file.

## Data Management

The system stores all information in CSV files.

* books.csv stores book details.
* members.csv stores member details.
* loans.csv stores borrowing records.

Data is automatically loaded when the program starts and saved when changes are made.

## Error Handling

The program includes exception handling to prevent crashes and provide user-friendly error messages.

Examples include:

* Borrowing a book that is not available.
* Entering invalid information.
* Missing data files.

If a CSV file is missing, the system starts with an empty collection instead of stopping unexpectedly.

## Conclusion

The Library Management System successfully demonstrates the application of Python programming concepts in a real-world scenario. The project uses object-oriented programming, modular design, file handling, and exception handling to create a simple and effective library management solution. The system provides an easy way to manage books, members, and loan records while ensuring that data is stored permanently using CSV files.
