import sqlite3
from datetime import datetime, timedelta
import uuid
global user_id

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


SQL_LOGIN_QUERY = """
                SELECT username, password, user_id 
                FROM Users
                WHERE username = ? AND password = ?
                """

SQL_SEARCH_BOOK = """
                SELECT book_id, title, author, quantity
                FROM Books
                WHERE title LIKE ? or author LIKE ? or book_id LIKE ?
                """

SQL_BORROW_BOOK = """
                UPDATE Books
                SET quantity = quantity - 1
                WHERE book_id = ?
                """

SQL_INSERT_BOOK = """
                INSERT INTO Borrowed
                (borrowed_id, user_id, book_id, borrow_date, due_date) 
                VALUES (?, ?, ?, ?, ?)
                """

def generate_book_id() -> None:
    return str(uuid.uuid4())

def get_book(book) -> list:
    """
                            GET BOOK
    This function search for the possible books the user input
    in the search_book() function.

    This function fetches all the information of the book such as:

    1. book_id -> unique identification of the book
    2. title -> name of the book
    3. author -> writer of the book
    4. quantity -> number of copies left of the book in the library

    This function will return all of that information when called
    """
    keyword = f"%{book}%"
    cursor.execute(SQL_SEARCH_BOOK, (keyword, keyword, keyword))
    return cursor.fetchall()

    
def display_book(selected_book) -> None:
    """
                            DISPLAY BOOK
    This function displays all of the information of the books such
    as:

    1. book_id -> unique identification of the book
    2. title -> name of the book
    3. author -> writer of the book
    4. quantity -> number of copies left of the book in the library

    This will also ask the user if they want to borrow the book displayed
    in the console. If they didn't wish to borrow it. They will be directed
    to the borrow_interface()
    """
    book_id, title, author, quantity = selected_book[0]

    print(f"Book ID: {book_id}")
    print(f"Title: {title}")
    print(f"Author: {author}")
    print(f"Available Copies: {quantity}")

    choice = str(input("Would you like to borrow this book?: "))
    print(choice.capitalize())
    if choice.upper() in ["YES", "Y"]:

        borrow_date = datetime.now()
        due_date = borrow_date + timedelta(days = 14)
        borrow_id = generate_book_id()

        cursor.execute(SQL_INSERT_BOOK, (borrow_id, user_id, book_id, borrow_date, due_date))
        cursor.execute(SQL_BORROW_BOOK, (book_id,))
        connection.commit()
        print("You have borrowed a book!")
    elif choice.upper() in ["NO", "N"]:
        borrow_interface()
    else:
        print('Not Working')
        display_book(selected_book)

def search_book(book) -> bool:
    """
                            SEARCH BOOK
    This function displays all of the related books given by the keyword
    that the user provided in the function "get_book()"

    The function will display several/no books that consists of:

    1. book[0] -> unique identification of the book
    2. book[1] -> name of the book
    3. book[2] -> writer of the book
    4. book[3] -> number of copies left of the book in the library
    """
    results = get_book(book)
    if results:
        for book in results:
            print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Available Copies: {book[3]}")
            return True
    return False

def borrow_interface() -> None:
    book: str = input(str("What book would you like to borrow? "))

    if search_book(book):
        selected_book = str(input("Please enter the ID of the book you want to borrow: "))
        result = get_book(selected_book)
        _, _, _, quantity = result[0]
        if result:
            if quantity > 0:
                display_book(result)
            else: 
                print("No available copies of that book. Borrow other books instead.")
    else: 
        print("No books are found. Try again")
        borrow_interface()


def return_interface() -> None:
    print("")

def switch_interface(action) -> None:
    match action:
        case 1:
            borrow_interface()
        case 2:
            return_interface()
        case 3:
            login_interface()
        case _:
            print("Invalid Choice. Select Again")
            main_interface()


def main_interface() -> None:
    """
                            MAIN INTERFACE
    This function is the main interface of the system. The function
    consists of three choices such as:

    1. Borrow Book
        - Will be directed to an interface that lets the user search 
        for books they want.

    2. Return Book
        - Will be directed to an interface that lets the user return 
        the books they have borrowed before.
    
    3. Logout 
        - Will let the user logout in the system and will be directed 
        to the login interface of the system.
    """

    print("[1] Borrow Book")
    print("[2] Return Book")
    print("[3] Logout")
    action: int = int(input("What would you like to do?"))
    

    switch_interface(action)

def validate_login(username, password) -> bool:
    global user_id
    cursor.execute(SQL_LOGIN_QUERY, (username, password))
    user_credentials = cursor.fetchall()
    if user_credentials:
        return True
    return False

def login_interface() -> None:
    print("LIBRARY MANAGEMENT SYSTEM")
    username: str = str(input("Username: "))

    password: str = str(input("Password: "))

    if validate_login(username, password):
        main_interface()
    else:
        print("Mali ka. Try again.")
        login_interface()

def main() -> None:
    login_interface()
    

if __name__ == '__main__':
    main()