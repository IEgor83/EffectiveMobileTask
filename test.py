import unittest
import os
from main import Library


class TestLibrary(unittest.TestCase):
    def setUp(self):
        """Инициализация временной библиотеки перед каждым тестом."""
        self.library = Library("test_books.json")  # Используем тестовый файл для данных

    def tearDown(self):
        """Удаление временного файла после каждого теста."""
        if os.path.exists("test_books.json"):
            os.remove("test_books.json")

    def test_add_book(self):
        """Тест добавления книги."""
        self.library.add_book("Test Title", "Test Author", 2024)
        self.assertEqual(len(self.library.books), 1)
        self.assertEqual(self.library.books[0].title, "Test Title")

    def test_remove_book(self):
        """Тест удаления книги."""
        book = self.library.add_book("Test Title", "Test Author", 2024)
        self.library.delete_book(book.id)
        self.assertEqual(len(self.library.books), 0)

    def test_remove_nonexistent_book(self):
        """Тест удаления несуществующей книги."""
        self.library.add_book("Test Title", "Test Author", 2024)
        initial_count = len(self.library.books)
        self.library.delete_book(999)
        self.assertEqual(len(self.library.books), initial_count)

    def test_find_book_by_id(self):
        """Тест поиска книги по ID."""
        book = self.library.add_book("Test Title", "Test Author", 2024)
        found_book = self.library.find_book_by_id(book.id)
        self.assertIsNotNone(found_book)
        self.assertEqual(found_book.title, "Test Title")

    def test_find_nonexistent_book_by_id(self):
        """Тест поиска книги по несуществующему ID."""
        self.assertIsNone(self.library.find_book_by_id(999))

    def test_update_status(self):
        """Тест обновления статуса книги."""
        book = self.library.add_book("Test Title", "Test Author", 2024)
        self.library.update_status(book.id, "выдана")
        self.assertEqual(book.status, "выдана")

    def test_update_status_invalid(self):
        """Тест попытки обновить статус на некорректный."""
        book = self.library.add_book("Test Title", "Test Author", 2024)
        initial_status = book.status
        self.library.update_status(book.id, "неизвестный статус")
        self.assertEqual(book.status, initial_status)

    def test_display_books(self):
        """Тест отображения всех книг."""
        self.library.add_book("Title 1", "Author 1", 2024)
        self.library.add_book("Title 2", "Author 2", 2023)
        books = self.library.find_books()
        self.assertEqual(len(books), 2)
        self.assertTrue(any(book.title == "Title 1" for book in books))
        self.assertTrue(any(book.title == "Title 2" for book in books))

    def test_save_and_load_books(self):
        """Тест сохранения и загрузки книг из файла."""
        self.library.add_book("Test Title", "Test Author", 2024)
        new_library = Library("test_books.json")
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "Test Title")

    def test_load_invalid_books(self):
        """Тест загрузки некорректных данных."""
        with open("test_books.json", "w", encoding="utf-8") as f:
            f.write('[{"id": 1, "title": "Valid Book", "author": "a3", "year": 2003,"status": "в наличии"}, {"id": 2}]')  # Второй объект некорректен

        new_library = Library("test_books.json")
        self.assertEqual(len(new_library.books), 1)
        self.assertEqual(new_library.books[0].title, "Valid Book")


if __name__ == "__main__":
    unittest.main()
