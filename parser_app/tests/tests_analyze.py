import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from parser_app.services.statistics_analyzer import StatisticsAnalyzer  # Убедитесь, что импорт правильный
import matplotlib.pyplot as plt
import io
import base64

class TestStatisticsAnalyzer(unittest.TestCase):

    def setUp(self):
        # Мокируем объекты для queryset
        self.mock_stat1 = MagicMock()
        self.mock_stat1.author.full_name = 'Иванов И.И.'
        self.mock_stat1.year = 2023
        self.mock_stat1.monograph = 5
        self.mock_stat1.textbook = 3
        self.mock_stat1.tutorial = 2
        self.mock_stat1.tutorial_griff = 1
        self.mock_stat1.article_russian_journal = 10
        self.mock_stat1.article_foreign_journal = 4
        self.mock_stat1.izvestia_vstu = 7
        self.mock_stat1.journals_vstu = 6
        self.mock_stat1.article_russian_collection = 3
        self.mock_stat1.article_foreign_collection = 2
        self.mock_stat1.theses = 1
        self.mock_stat1.educational_complex = 0
        self.mock_stat1.deposited_manuscript = 0
        self.mock_stat1.patent_document = 0
        self.mock_stat1.certificate = 0
        self.mock_stat1.other_publications = 0

        self.mock_stat2 = MagicMock()
        self.mock_stat2.author.full_name = 'Петров П.П.'
        self.mock_stat2.year = 2023
        self.mock_stat2.monograph = 3
        self.mock_stat2.textbook = 4
        self.mock_stat2.tutorial = 6
        self.mock_stat2.tutorial_griff = 2
        self.mock_stat2.article_russian_journal = 12
        self.mock_stat2.article_foreign_journal = 5
        self.mock_stat2.izvestia_vstu = 8
        self.mock_stat2.journals_vstu = 7
        self.mock_stat2.article_russian_collection = 4
        self.mock_stat2.article_foreign_collection = 3
        self.mock_stat2.theses = 2
        self.mock_stat2.educational_complex = 1
        self.mock_stat2.deposited_manuscript = 0
        self.mock_stat2.patent_document = 1
        self.mock_stat2.certificate = 0
        self.mock_stat2.other_publications = 1

        # Создаем DataFrame с тестовыми данными
        self.queryset = [self.mock_stat1, self.mock_stat2]

        # Инициализация объекта статистики
        self.analyzer = StatisticsAnalyzer(self.queryset)

    @patch('parser_app.services.statistics_analyzer.StatisticsAnalyzer._prepare_data')
    def test_aggregate_statistics(self, mock_prepare_data):
        # Мокируем _prepare_data, чтобы возвращать тестовые данные
        mock_prepare_data.return_value = pd.DataFrame([
            {'author': 'Иванов И.И.', 'year': 2023, 'monograph': 5, 'textbook': 3},
            {'author': 'Петров П.П.', 'year': 2023, 'monograph': 3, 'textbook': 4}
        ])

        # Тестируем метод агрегации для 'monograph'
        result_monograph = self.analyzer.aggregate_statistics('monograph')
        self.assertEqual(result_monograph['sum'], 8)  # Сумма 5 + 3 = 8
        self.assertEqual(result_monograph['average'], 4)  # Среднее (5 + 3) / 2 = 4
        self.assertEqual(result_monograph['median'], 4)  # Медиана для 5 и 3 = 4
        self.assertEqual(result_monograph['max'], 5)  # Максимум 5
        self.assertEqual(result_monograph['min'], 3)  # Минимум 3

        # Тестируем метод агрегации для 'textbook'
        result_textbook = self.analyzer.aggregate_statistics('textbook')
        self.assertEqual(result_textbook['sum'], 7)  # Сумма 3 + 4 = 7
        self.assertEqual(result_textbook['average'], 3.5)  # Среднее (3 + 4) / 2 = 3.5
        self.assertEqual(result_textbook['median'], 3.5)  # Медиана для 3 и 4 = 3.5
        self.assertEqual(result_textbook['max'], 4)  # Максимум 4
        self.assertEqual(result_textbook['min'], 3)  # Минимум 3

    @patch('parser_app.services.statistics_analyzer.StatisticsAnalyzer._prepare_data')
    def test_invalid_column_for_aggregation(self, mock_prepare_data):
        # Мокируем _prepare_data, чтобы возвращать тестовые данные
        mock_prepare_data.return_value = pd.DataFrame([
            {'author': 'Иванов И.И.', 'year': 2023, 'monograph': 5, 'textbook': 3}
        ])

        # Тестируем, что метод выбрасывает ошибку, если передан некорректный столбец
        with self.assertRaises(ValueError):
            self.analyzer.aggregate_statistics('invalid_column')

    @patch('parser_app.services.statistics_analyzer.StatisticsAnalyzer._prepare_data')
    def test_analyze(self, mock_prepare_data):
        # Мокируем _prepare_data, чтобы возвращать тестовые данные
        mock_prepare_data.return_value = pd.DataFrame([
            {'author': 'Иванов И.И.', 'year': 2023, 'monograph': 5, 'textbook': 3},
            {'author': 'Петров П.П.', 'year': 2023, 'monograph': 3, 'textbook': 4}
        ])

        # Тестируем метод анализа для всех колонок
        results = self.analyzer.analyze()

        # Проверяем агрегацию для 'monograph'
        self.assertIn('monograph', results)
        self.assertEqual(results['monograph']['sum'], 8)
        self.assertEqual(results['monograph']['average'], 4)
        self.assertEqual(results['monograph']['median'], 4)
        self.assertEqual(results['monograph']['max'], 5)
        self.assertEqual(results['monograph']['min'], 3)

        # Проверяем агрегацию для 'textbook'
        self.assertIn('textbook', results)
        self.assertEqual(results['textbook']['sum'], 7)
        self.assertEqual(results['textbook']['average'], 3.5)
        self.assertEqual(results['textbook']['median'], 3.5)
        self.assertEqual(results['textbook']['max'], 4)
        self.assertEqual(results['textbook']['min'], 3)

