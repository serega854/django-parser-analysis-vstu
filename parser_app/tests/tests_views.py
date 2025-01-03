import json
from django.test import TestCase
from unittest.mock import patch
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.edge.service import Service
from parser_app.models import Author, Publication, PublicationStatistics



class ParseLibraryTestCase(TestCase):

    def setUp(self):
        # Создаём тестового автора
        self.author_name = "Новрузов С.Р."
        self.author = Author.objects.create(full_name=self.author_name, publication_count=0)


    @patch('selenium.webdriver.Edge')
    def test_parse_library_author_exists(self, MockWebDriver):
        # Создаём существующего автора в базе данных
        Author.objects.create(full_name=self.author_name, publication_count=0)

        # Пример данных для POST-запроса
        data = {
            "surname": self.author_name,
        }

        response = self.client.post('/parse_library/', data, content_type="application/json")

        # Проверка, что запрос отклонён
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], "Author with this surname already exists in the database.")

    @patch('selenium.webdriver.Edge')
    def test_parse_library_invalid_json(self, MockWebDriver):
        # Пример неправильного JSON (неполный или с ошибкой)
        data = '{"surname": "Новрузов С.Р."'

        response = self.client.post('/parse_library/', data, content_type="application/json")

        # Проверка, что ответ содержит ошибку
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], "Invalid JSON.")

    @patch('selenium.webdriver.Edge')
    def test_parse_library_missing_surname(self, MockWebDriver):
        # Пример данных с отсутствующей фамилией
        data = {}

        response = self.client.post('/parse_library/', json.dumps(data), content_type="application/json")

        # Проверка, что ошибка "Surname is required"
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['success'], False)
        self.assertEqual(response.json()['error'], "Surname is required.")
