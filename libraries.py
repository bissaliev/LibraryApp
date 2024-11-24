from books import Book
from filemanagers import FileManager


class LibraryManager:
    def __init__(self, book_class: type[Book], file_manager: FileManager):
        self.file_manager = file_manager
        self.book_class: type[Book] = book_class
        self._books: dict[int, Book] = self._load_book()
        self.next_id: int = self.get_next_id()

    def _load_book(self) -> dict[int, Book]:
        data = self.file_manager.load()
        books = {item["id"]: self.book_class.from_dict(item) for item in data}
        return books

    def get_next_id(self) -> int:
        if self._books:
            return max(int(id) for id in self._books) + 1
        return 1

    def _save_books(self) -> None:
        data = [book.to_dict() for book in self._books.values()]
        self.file_manager.save(data)

    def get_book(self, id: int) -> Book:
        try:
            book = self._books[id]
        except KeyError as error:
            raise ValueError(f"Книга с id `{id}` не найдена.") from error
        return book

    def get_books(self) -> list[Book]:
        return [book for book in self._books.values()]

    def add_book(self, title: str, author: str, year: int) -> Book:
        try:
            new_book = self.book_class(
                title=title,
                author=author,
                year=year,
                id=self.next_id,
            )
        except ValueError as error:
            raise ValueError(str(error)) from error
        for book in self._books.values():
            if book == new_book:
                raise ValueError(f"Книга `{new_book.title}` уже существует.")
        self._books[new_book.id] = new_book
        self._save_books()
        self.next_id += 1
        return new_book

    def delete_book(self, id: int) -> Book:
        try:
            remote_book = self._books.pop(id)
        except KeyError as error:
            raise ValueError(f"Книга с id `{id}` не найдена.") from error
        else:
            self._save_books()
            return remote_book

    def update_book_status(self, id: int, status: str) -> Book:
        try:
            updated_book = self._books[id]
        except KeyError as error:
            raise ValueError(f"Книга с id `{id}` не найдена.") from error
        else:
            updated_book.status = status
            self._save_books()
            return updated_book

    def search_book(self, field: str, query: str | int) -> list[Book]:
        field = field.strip().lower()
        query = str(query).strip().lower()
        output = []
        for book in self._books.values():
            value = str(getattr(book, field)).lower()
            if (value == query) or (query in value):
                output.append(book)
        return output
