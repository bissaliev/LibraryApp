import json
from pathlib import Path

from books import Book


class LibraryManager:
    def __init__(self, book: Book, filename: str = "library.json"):
        self.filename: str = filename
        self.file = self.get_file()
        self.book = book  # TODO Указать правильно аннотацию класса
        self.books: dict[str, Book] = self.load_book()

    def get_file(self) -> Path:
        file = Path(__file__).parent / self.filename
        if not file.exists():
            raise FileNotFoundError(f"Файла `{self.filename}` не существует.")
        return file

    def load_book(self) -> dict[str, Book]:
        # TODOОбработать ошибку JSONDecodeError
        with self.file.open(encoding="utf-8") as f:
            data = json.load(f)
            books = {
                int(key): self.book.from_dict(value)
                for key, value in data.items()
            }
        return books

    def save_books(self):
        with self.file.open("w", encoding="utf-8") as file:
            data = {book.id: book.to_dict() for book in self.books.values()}
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_book(self, id: int):
        return self.books.get(id)

    def get_books(self):
        yield from self.books.values()

    def add_book(self, title: str, author: str, year: int):
        # TODO Придумать как хранить состояние id в классе
        next_id = max(book.id for book in self.books.values()) + 1
        book = Book(title=title, author=author, year=year, id=next_id)
        for bk in self.books.values():
            if bk == book:
                print(f"Книга `{book.title}` уже существует.")
                return
        self.books[book.id] = book
        self.save_books()
        return book

    def delete_book(self, id: int):
        # TODO Исправить удаление по id
        try:
            current_book = self.books[id]
        except KeyError:
            print(f"Книги с id `{id}` не существует.")
        else:
            del self.books[id]
            self.save_books()
            print(f"Книга `{current_book.title}` удалена.")

    def update_book_status(self, id: int, status: str):
        # TODO Исправить обновление по id
        try:
            current_book = self.books[id]
        except KeyError:
            print(f"Книга `{current_book.title}` удалена.")
        else:
            current_book.status = status
            self.save_books()
            print(
                f"Статус книги `{current_book.title}` изменён на `{status}`."
            )

    def search_book(self, field: str, query: str):
        """Поиск книг по полям title, author, year."""
        field = field.lower()
        return getattr(self, f"_get_book_by_{field}")(query)

    def _get_book_by_author(self, author: str):
        output = []
        for book in self.books.values():
            if book.author == author:
                output.append(book)
        return output

    def _get_book_by_title(self, title: str):
        output = []
        for book in self.books.values():
            if book.title == title:
                output.append(book)
        return output

    def _get_book_by_year(self, year: str):
        output = []
        for book in self.books.values():
            if book.year == year:
                output.append(book)
        return output
