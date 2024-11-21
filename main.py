# • id (уникальный идентификатор, генерируется автоматически)
#  • title (название книги)
#  • author (автор книги)
#  • year (год издания)
#  • status (статус книги: “в наличии”, “выдана”)

import dataclasses
import json


@dataclasses
class Book2:
    title: str
    author: str
    year: int
    status: str = "в наличии"
    book_id: int | None = None


class Book:
    def __init__(self, title, author, year, id=None, status="в наличии"):
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def __str__(self):
        return (
            f"id: {self.id}, title: {self.title}, author: {self.author}, "
            f"year: {self.year}, status: {self.status}"
        )

    def to_dict(self):
        """Преобразование объекта книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        """Создание объекта книги из словаря."""
        return cls(**data)


class LibraryManager:
    def __init__(self, filename: str = "library.json"):
        self.filename = filename
        self.books = {}
        self.load_book()

    def load_book(self):
        with open(self.filename, encoding="utf-8") as file:
            data = json.load(file)
            for book_data in data:
                book = Book(**book_data)
                self.books[book.id] = book

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            data = [book.to_dict() for book in self.books.values()]
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_books(self):
        for book in self.books.values():
            print(book)

    def add_book(self, title: str, author: str, year: int):
        book_id = max(self.books.keys()) + 1
        book = Book(title=title, author=author, year=year, id=book_id)
        self.books[book.id] = book
        self.save_books()
        return book

    def delete_book(self, id: int):
        try:
            current_book = self.books[id]
        except KeyError:
            print(f"Книги с id `{id}` не существует.")
        else:
            del self.books[id]
            self.save_books()
            print(f"Книга `{current_book.title}` удалена.")

    def update_book_status(self, id: int, status: str):
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
        for book in self.books.values():
            if (
                getattr(book, field.lower()) == query.title()
                if isinstance(query, str)
                else query
            ):
                print("Книга найдена:")
                print(book)
                return
        print(f"Книга со значением `{query}` не найдена.")


library = LibraryManager()
library.get_books()
# library.add_book(
#     title="Над пропастью во ржи2222", author="Лев Толстой", year=1869
# )
# library.delete_book(7)
# library.update_book_status(6, "выдана")
# library.get_books()
library.search_book("year", 1949)
