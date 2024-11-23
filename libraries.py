from typing import Type

from books import Book
from filemanagers import FileManager


class LibraryManager:
    def __init__(self, book_class: Type[Book], file_manager: FileManager):
        self.file_manager = file_manager
        self.book_class: Type[Book] = book_class
        self.books: dict[int, Book] = self._load_book()
        self.next_id: int = self.get_next_id()

    def _load_book(self) -> dict[int, Book]:
        data = self.file_manager.load()
        books = {item["id"]: self.book_class.from_dict(item) for item in data}
        return books

    def get_next_id(self) -> int:
        if self.books:
            return max(int(id) for id in self.books) + 1
        return 1

    def _save_books(self) -> None:
        data = [book.to_dict() for book in self.books.values()]
        self.file_manager.save(data)

    def get_book(self, id: int) -> Book | None:
        return self.books.get(id, None)

    def get_books(self):
        yield from self.books.values()

    def add_book(self, title: str, author: str, year: int) -> Book:
        new_book = Book(title=title, author=author, year=year, id=self.next_id)
        for book in self.books.values():
            if book == new_book:
                raise ValueError(f"Книга `{new_book.title}` уже существует.")
        self.books[new_book.id] = new_book
        self._save_books()
        self.next_id += 1
        return new_book

    def delete_book(self, id: int) -> Book | None:
        try:
            remote_book = self.books.pop(id)
        except KeyError:
            return None
        else:
            self._save_books()
            return remote_book

    def update_book_status(self, id: int, status: str) -> Book | None:
        try:
            updated_book = self.books[id]
        except KeyError:
            return None
        else:
            updated_book.status = status
            self._save_books()
            return updated_book

    def search_book(self, field, query):
        field = field.lower()
        query = str(query).lower()
        output = []
        for book in self.books.values():
            value = str(getattr(book, field)).lower()
            if (value == query) or (query in value):
                output.append(book)
        return output
