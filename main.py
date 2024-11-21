import json
from datetime import date
from enum import Enum


class Status(Enum):
    AVAILABLE = "в наличии"
    BORROWED = "выдана"


class Book:
    def __init__(
        self,
        title: str,
        author: str,
        year: int,
        id: int = None,
        status: str = Status.AVAILABLE.value,
    ):
        self.id: int = id
        self.title: str = title
        self.author: str = author
        self.year: int = year
        self.status: str = status

    def __str__(self):
        return str(self.to_dict())

    def __repr__(self):
        return f"{self.__class__.__name__}({self.title})"

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
        return cls(
            id=int(data.get("id")),
            title=data.get("title"),
            author=data.get("author"),
            year=int(data.get("year")),
            status=data.get("status"),
        )

    def __eq__(self, other: "Book"):
        return (self.title, self.author, self.year) == (
            other.title,
            other.author,
            other.year,
        )

    @property
    def id(self):
        return self.__id

    @id.setter
    def id(self, value):
        if not isinstance(value, int) or value < 1:
            raise ValueError(
                "ID книги должно быть целым положительным числом."
            )
        self.__id = value

    @property
    def title(self):
        return self.__title

    @title.setter
    def title(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название книги должно быть непустой строкой.")
        self.__title = value.strip()

    @property
    def author(self):
        return self.__author

    @author.setter
    def author(self, value):
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя автора должно быть непустой строкой.")
        self.__author = value.strip()

    @property
    def year(self):
        return self.__year

    @year.setter
    def year(self, value):
        if not isinstance(value, int):
            raise ValueError("Год издания должен быть целым числом.")
        current_year = date.today().year
        if value > current_year:
            raise ValueError("Год издания не может быть больше текущего года.")
        self.__year = value

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, value):
        if value not in {s.value for s in Status}:
            raise ValueError(
                "Статус книги должен быть одним из: "
                f"{', '.join(s.value for s in Status)}"
            )
        self.__status = value


class LibraryManager:
    def __init__(self, book: Book, filename: str = "library.json"):
        self.filename: str = filename
        self.book = book
        self.books: dict[str, Book] = {}
        self.load_book()

    def load_book(self):
        try:
            with open(self.filename, encoding="utf-8") as file:
                data = json.load(file)
                self.books = {
                    key: self.book.from_dict(value)
                    for key, value in data.items()
                }
        except FileNotFoundError:
            print(f"Файла `{self.filename}` не существует.")

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as file:
            data = {book.title: book.to_dict() for book in self.books.values()}
            json.dump(data, file, ensure_ascii=False, indent=4)

    def get_book(self, id: int):
        return self._binary_search(list(self.books.values()), id)

    def get_books(self):
        yield from self.books.values()

    def add_book(self, title: str, author: str, year: int):
        book = Book(title=title, author=author, year=year)
        if book.title in self.books and book == self.books[book.title]:
            print(f"Книга `{book.title}` уже существует.")
            return
        next_id = max(book.id for book in self.books.values()) + 1
        book.id = next_id
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
        field = field.lower()
        return getattr(self, f"_get_book_by_{field}")(query)

    def _binary_search(self, objs: list[Book], id: int):
        if objs[0].id > id or objs[-1].id < id:
            return None
        left = 0
        right = len(objs)
        while left < right:
            middle = (left + right) // 2
            obj = objs[middle]
            if id > obj.id:
                left = middle + 1
            elif id < obj.id:
                right = middle
            else:
                return obj
        return objs[left] if objs[left].id == id else None

    def _get_book_by_author(self, author: str):
        output = []
        for book in self.books.values():
            if book.author == author:
                output.append(book)
        return output

    def _get_book_by_title(self, title: str):
        return [self.books.get(title)]

    def _get_book_by_year(self, year: str):
        output = []
        for book in self.books.values():
            if book.year == year:
                output.append(book)
        return output


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
