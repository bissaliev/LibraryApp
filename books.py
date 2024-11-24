from datetime import date
from enum import Enum


class Status(Enum):
    """Статусы книг."""

    AVAILABLE: str = "в наличии"
    BORROWED: str = "выдана"


class Book:
    """Класс книг."""

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

    def __str__(self) -> str:
        return (
            f"id: {self.id}\n"
            f"title: {self.title}\n"
            f"author: {self.author}\n"
            f"year: {self.year}\n"
            f"status: {self.status}"
        )

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title})"

    def to_dict(self) -> dict[str, str | int]:
        """Преобразование объекта в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str : str | int]) -> "Book":
        """Классовый метод для создания объекта из словаря."""
        return cls(
            id=data.get("id"),
            title=data.get("title"),
            author=data.get("author"),
            year=data.get("year"),
            status=data.get("status", Status.AVAILABLE.value),
        )

    def __eq__(self, other: object) -> bool:
        """Метод сравнения объектов по полям title, author, year."""
        if not isinstance(other, Book):
            return NotImplemented
        return (
            self.title.lower() == other.title.lower()
            and self.author.lower() == other.author.lower()
            and self.year == other.year
        )

    @property
    def id(self) -> int:
        """Геттер для атрибута id."""
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        """Сеттер для атрибута id."""
        if not isinstance(value, int) or value < 1:
            raise ValueError(
                "ID книги должно быть целым положительным числом."
            )
        self.__id = value

    @property
    def title(self) -> str:
        """Геттер для атрибута title."""
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        """Сеттер для атрибута title."""
        self.__title = self.validate_non_empty_string("title", value)

    @property
    def author(self) -> str:
        """Геттер для атрибута author."""
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        """Сеттер для атрибута author."""
        self.__author = self.validate_non_empty_string("author", value)

    @property
    def year(self) -> int:
        """Геттер для атрибута year."""
        return self.__year

    @year.setter
    def year(self, value: int) -> None:
        """Сеттер для атрибута year."""
        if not isinstance(value, int):
            raise ValueError("Год издания должен быть целым числом.")
        current_year = date.today().year
        if value > current_year:
            raise ValueError("Год издания не может быть больше текущего года.")
        self.__year = value

    @property
    def status(self) -> str:
        """Геттер для атрибута status."""
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        """Сеттер для атрибута status."""
        if value not in {s.value for s in Status}:
            raise ValueError(
                "Статус книги должен быть одним из: "
                f"{', '.join(s.value for s in Status)}"
            )
        self.__status = value.strip().lower()

    @staticmethod
    def validate_non_empty_string(field_name: str, value: str) -> str:
        """Валидатор проверяет, что атрибут является непустой строкой."""
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError(
                f"Поле {field_name} должно быть непустой строкой."
            )
        return value.strip()
