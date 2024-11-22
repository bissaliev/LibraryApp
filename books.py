from datetime import date
from enum import Enum


class Status(Enum):
    AVAILABLE: str = "в наличии"
    BORROWED: str = "выдана"


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

    def __str__(self) -> str:
        return str(self.to_dict())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({self.title})"

    def to_dict(self) -> dict[str, str | int]:
        """Преобразование объекта книги в словарь."""
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data: dict[str : str | int]) -> "Book":
        """Создание объекта книги из словаря."""
        return cls(
            id=int(data.get("id")),
            title=data.get("title"),
            author=data.get("author"),
            year=int(data.get("year")),
            status=data.get("status"),
        )

    def __eq__(self, other: "Book") -> bool:
        return (self.title, self.author, self.year) == (
            other.title,
            other.author,
            other.year,
        )

    @property
    def id(self) -> int:
        return self.__id

    @id.setter
    def id(self, value: int) -> None:
        if not isinstance(value, int) or value < 1:
            raise ValueError(
                "ID книги должно быть целым положительным числом."
            )
        self.__id = value

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Название книги должно быть непустой строкой.")
        self.__title = value.strip().capitalize()

    @property
    def author(self) -> str:
        return self.__author

    @author.setter
    def author(self, value: str) -> None:
        if not isinstance(value, str) or value.strip() == "":
            raise ValueError("Имя автора должно быть непустой строкой.")
        self.__author = value.strip().title()

    @property
    def year(self) -> int:
        return self.__year

    @year.setter
    def year(self, value: int) -> None:
        if not isinstance(value, int):
            raise ValueError("Год издания должен быть целым числом.")
        current_year = date.today().year
        if value > current_year:
            raise ValueError("Год издания не может быть больше текущего года.")
        self.__year = value

    @property
    def status(self) -> str:
        return self.__status

    @status.setter
    def status(self, value: str) -> None:
        if value not in {s.value for s in Status}:
            raise ValueError(
                "Статус книги должен быть одним из: "
                f"{', '.join(s.value for s in Status)}"
            )
        self.__status = value.strip().lower()
