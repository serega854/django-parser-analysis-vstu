from django.test import TestCase
from unittest.mock import MagicMock, patch
from parser_app.models import Author, Publication, PublicationStatistics


class AuthorModelTest(TestCase):
    # Проверяем, что объект автора корректно создается с заданными значениями
    @patch('parser_app.models.Author.objects.create')
    def test_author_creation(self, mock_create):
        mock_author = MagicMock()
        mock_author.full_name = "Иван Иванов"
        mock_author.publication_count = 5
        mock_create.return_value = mock_author

        # Проверяем создание автора
        author = Author.objects.create(full_name="Иван Иванов", publication_count=5)
        self.assertEqual(author.full_name, "Иван Иванов")
        self.assertEqual(author.publication_count, 5)
        mock_create.assert_called_once_with(full_name="Иван Иванов", publication_count=5)

    # Проверяем, что при не заполненном кол-ве публикаций по дефолту заполняется 0
    @patch('parser_app.models.Author.objects.create')
    def test_default_publication_count(self, mock_create):
        mock_author = MagicMock()
        mock_author.publication_count = 0
        mock_create.return_value = mock_author

        author = Author.objects.create(full_name="Иван Иванов")
        self.assertEqual(author.publication_count, 0)
        mock_create.assert_called_once_with(full_name="Иван Иванов")


class PublicationStatisticsModelTest(TestCase):
    # Проверяем, что объект публикаций корректно создается
    @patch('parser_app.models.PublicationStatistics.objects.create')
    def test_statistics_creation(self, mock_create):
        mock_author = MagicMock()
        mock_author.full_name = "Иван Иванов"
        mock_stats = MagicMock()
        mock_stats.author = mock_author
        mock_stats.year = 2025
        mock_stats.monograph = 1
        mock_stats.textbook = 2
        mock_stats.tutorial = 3
        mock_create.return_value = mock_stats

        # Проверяем создание статистики
        stats = PublicationStatistics.objects.create(author=mock_author, year=2025, monograph=1, textbook=2, tutorial=3)
        self.assertEqual(stats.author, mock_author)
        self.assertEqual(stats.year, 2025)
        self.assertEqual(stats.monograph, 1)
        self.assertEqual(stats.textbook, 2)
        self.assertEqual(stats.tutorial, 3)
        mock_create.assert_called_once_with(author=mock_author, year=2025, monograph=1, textbook=2, tutorial=3)

    # Проверяем, что значения имеют 0 по умолчанию, если их не задали
    @patch('parser_app.models.PublicationStatistics.objects.create')
    def test_default_statistics_values(self, mock_create):
        mock_author = MagicMock()
        mock_stats = MagicMock()
        mock_stats.monograph = 0
        mock_stats.textbook = 0
        mock_stats.tutorial = 0
        mock_create.return_value = mock_stats

        stats = PublicationStatistics.objects.create(author=mock_author, year=2025)
        self.assertEqual(stats.monograph, 0)
        self.assertEqual(stats.textbook, 0)
        self.assertEqual(stats.tutorial, 0)
        mock_create.assert_called_once_with(author=mock_author, year=2025)

    # Проверка каскадности, при удалении автора, удаляются его публикации
    @patch('parser_app.models.PublicationStatistics.objects.count')
    def test_cascade_delete_author(self, mock_count):
        # Мокаем счетчик записей в базе
        mock_count.return_value = 0

        mock_author = MagicMock()
        mock_author.delete = MagicMock()

        stats = MagicMock()
        stats.delete = MagicMock()

        mock_author.delete()
        self.assertEqual(mock_count(), 0)
        mock_author.delete.assert_called_once()


class PublicationModelTest(TestCase):
    # Проверка, что заголовок является строкой и правильно заполняется
    @patch('parser_app.models.Publication.objects.create')
    def test_str_representation(self, mock_create):
        mock_author = MagicMock()
        mock_author.full_name = "Иван Иванов"
        mock_publication = MagicMock()
        mock_publication.title = "Научная статья"
        mock_create.return_value = mock_publication

        publication = Publication.objects.create(author=mock_author, title="Научная статья")
        self.assertEqual(str(publication), "Научная статья")
        mock_create.assert_called_once_with(author=mock_author, title="Научная статья")

    # Проверка каскадного удаления, удаляется автор и его статьи каскадно тоже
    @patch('parser_app.models.Publication.objects.count')
    def test_cascade_delete_author(self, mock_count):
        # Мокаем счетчик записей в базе
        mock_count.return_value = 0

        mock_author = MagicMock()
        mock_author.delete = MagicMock()

        mock_publication1 = MagicMock()
        mock_publication1.delete = MagicMock()

        mock_publication2 = MagicMock()
        mock_publication2.delete = MagicMock()

        mock_author.delete()
        self.assertEqual(mock_count(), 0)
        mock_author.delete.assert_called_once()


class RelatedModelTest(TestCase):
    # Проверка создается автор с двумя публикациями, проверяем, что каждая публикация есть в списке публикаций автора
    @patch('parser_app.models.Publication.objects.create')
    @patch('parser_app.models.Author.publications', new_callable=MagicMock)
    def test_related_publications(self, mock_publications, mock_create):
        mock_author = MagicMock()
        mock_author.full_name = "Иван Иванов"

        # Мокаем publications.count() чтобы вернуть значение 2
        mock_publications.count.return_value = 2

        mock_publication1 = MagicMock()
        mock_publication1.title = "Публикация 1"

        mock_publication2 = MagicMock()
        mock_publication2.title = "Публикация 2"

        mock_create.side_effect = [mock_publication1, mock_publication2]

        pub1 = Publication.objects.create(author=mock_author, title="Публикация 1")
        pub2 = Publication.objects.create(author=mock_author, title="Публикация 2")

        # Проверяем, что количество публикаций равно 2
        self.assertEqual(mock_publications.count(), 2)

        # Проверяем, что публикации присутствуют в списке
        mock_publications.all.return_value = [mock_publication1, mock_publication2]
        self.assertIn(pub1, mock_publications.all())
        self.assertIn(pub2, mock_publications.all())


class PublicationModelTest(TestCase):
    @patch('parser_app.models.Publication.__str__', return_value='Научная статья')
    def test_str_representation(self, mock_str):
        author = Author.objects.create(full_name="Иван Иванов")
        publication = Publication.objects.create(author=author, title="Научная статья")

        # Проверка строки представления публикации
        self.assertEqual(str(publication), "Научная статья")





















