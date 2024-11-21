from books import Book, Status
from libraries import LibraryManager

if __name__ == "__main__":
    library = LibraryManager(Book)
    book = Book(
        title="Преступление и наказание",
        author="Федор Достоевский",
        year=1866,
        id=1,
    )
    print(book.status)
    book.status = Status.BORROWED.value
    print(book.status)
