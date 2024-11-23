from json import JSONDecodeError
from typing import Callable

from books import Book, Status
from filemanagers import JsonFileManager
from libraries import LibraryManager

menu_items = {
    "1": "Показать все книги",
    "2": "Получить книгу по ID",
    "3": "Добавить книгу",
    "4": "Удалить книгу",
    "5": "Изменить статус книги",
    "6": "Найти книгу",
    "7": "Выход",
}


def display_menu():
    """Отображение меню."""
    for key, value in menu_items.items():
        print(f"{key}. {value}")


def display_books(library: LibraryManager):
    """Отображение всех книг."""
    books = library.get_books()
    print("\n\n".join(str(book) for book in books), end="\n\n")


def display_book_by_id(library: LibraryManager) -> None:
    """Отображение книги по её ID."""
    try:
        book_id = int(input("Введите ID нужной книги: "))
    except ValueError:
        print("\nОшибка: ID книги должен быть числом.\n")
        return
    book = library.get_book(book_id)
    if not book:
        print(f"\nКнига с ID: {book_id} не найдена.\n")
    else:
        print("\nНайдена книга:\n")
        print(book, end="\n\n")


def add_book(library: LibraryManager):
    """Добавление книги в библиотеку."""
    title = input("Введите заголовок книги: ").strip()
    author = input("Введите автора книги: ").strip()
    try:
        year = int(input("Введите год публикации книги: ").strip())
    except ValueError:
        print("\nОшибка: год книги должен быть числом.\n")
        return
    try:
        book = library.add_book(title, author, year)
    except ValueError as error:
        print(f"\nОшибка: {error}\n")
    else:
        print(f"\nДобавлена новая книга в библиотеку:\n{book}\n\n")


def delete_book(library: LibraryManager):
    """Удаление книги по ID."""
    try:
        book_id = int(input("Введите id книги которую хотите удалить: "))
    except ValueError:
        print("\nОшибка: ID книги должен быть числом.\n")
        return
    remote_book = library.delete_book(book_id)
    if not remote_book:
        print(f"\nВ библиотеке нет книги с таким id `{book_id}`\n\n")
    else:
        print(f"\nКнига удалена:\n{remote_book}\n\n")


def update_status_of_book(library: LibraryManager):
    try:
        book_id = int(input("Введите id книги, которую хотите изменить: "))
    except ValueError:
        print("\nОшибка: ID книги должен быть числом.\n")
        return
    # Отображение выбора статусов
    print(f"\n1. {Status.AVAILABLE.value}\n2. {Status.BORROWED.value}\n")
    try:
        option = int(input("Выберите число нужного варианта: "))
        if option not in (1, 2):
            raise ValueError
    except ValueError:
        print("\nОшибка: Выбран неверный вариант.\n")
        return

    # Определяем статус в зависимости от выбора
    new_status = (
        Status.AVAILABLE.value if option == 1 else Status.BORROWED.value
    )

    # Обновляем статус книги
    updated_book = library.update_book_status(book_id, new_status)
    if not updated_book:
        print(f"\nВ библиотеке нет книги с таким ID `{book_id}`.\n")
    else:
        print(f"\nСтатус книги изменен:\n{updated_book}\n\n")


def search_book(library: LibraryManager):
    options = {"1": "title", "2": "author", "3": "year"}
    print("\n".join(f"{num}. {option}" for num, option in options.items()))
    option = input("\nВведите число поля по которому нужно найти книгу: ")
    match options.get(option):
        case "title":
            query = input("Введите название книги: ")
        case "author":
            query = input("Введите автора книги: ")
        case "year":
            query = input("Введите год книги: ")
        case None:
            print("\nТакой опции нет!\n")
            return
    books = library.search_book(options[option], query)
    print(f"\nПо вашему запросу найдено {len(books)} совпадений:\n")
    for book in books:
        print(book, end="\n\n")


choices: dict[str, Callable[[LibraryManager], None]] = {
    "1": display_books,
    "2": display_book_by_id,
    "3": add_book,
    "4": delete_book,
    "5": update_status_of_book,
    "6": search_book,
}


if __name__ == "__main__":
    try:
        file_manager = JsonFileManager("library.json")
        library = LibraryManager(Book, file_manager)
        while True:
            try:
                display_menu()
                choice = input("Введите число выбора: ")
                if choice in choices:
                    choices[choice](library)
                elif choice == "7":
                    print("\nДо свидания!!!\n")
                    break
                else:
                    print("Вы ввели некорректное значение.")
            except ValueError as error:
                print(f"\nОшибка ввода: {error}\n")
            except Exception as error:
                print(f"\nОшибка: {error}\n")
    except FileNotFoundError as error:
        print(f"Ошибка: {error}")
    except JSONDecodeError as error:
        print(f"Ошибка: {error}")
    except Exception as error:
        print(f"Произошла неизвестная ошибка: {error}")
    finally:
        print("Программа завершена")
