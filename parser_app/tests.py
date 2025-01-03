from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from .models import Author, Publication, PublicationStatistics

class AuthorModelTest(TestCase):
    #проверяем что объект автора корректно создается с заданными значениями
    def test_author_creation(self):
        author = Author.objects.create(full_name="Иван Иванов", publication_count=5)
        self.assertEqual(author.full_name, "Иван Иванов")
        self.assertEqual(author.publication_count, 5)

    #проверяем, что при не заполненном кол-ве публикаций по дефолту заполняется 0
    def test_default_publication_count(self):
        author = Author.objects.create(full_name="Иван Иванов")
        self.assertEqual(author.publication_count, 0)

class PublicationStatisticsModelTest(TestCase):
    def test_statistics_creation(self): #проверяем что объект публикаций корректно создается
        author = Author.objects.create(full_name="Иван Иванов")
        stats = PublicationStatistics.objects.create(
            author=author,
            year=2025,
            monograph=1,
            textbook=2,
            tutorial=3
        )
        self.assertEqual(stats.author, author)
        self.assertEqual(stats.year, 2025)
        self.assertEqual(stats.monograph, 1)
        self.assertEqual(stats.textbook, 2)
        self.assertEqual(stats.tutorial, 3) #проверяем соотсвутсвуют ли значения

    def test_default_statistics_values(self):
        author = Author.objects.create(full_name="Иван Иванов")
        stats = PublicationStatistics.objects.create(author=author, year=2025)
        self.assertEqual(stats.monograph, 0)
        self.assertEqual(stats.textbook, 0)#проверяем что значения имеют 0 по умолчанию если их не задали
        self.assertEqual(stats.tutorial, 0)

    def test_cascade_delete_author(self):
        author = Author.objects.create(full_name="Иван Иванов")
        PublicationStatistics.objects.create(author=author, year=2025) #проверка каскадности, при удалении автора, удаляются его публикации
        author.delete()
        self.assertEqual(PublicationStatistics.objects.count(), 0)


class PublicationModelTest(TestCase):
    def test_str_representation(self):
        author = Author.objects.create(full_name="Иван Иванов") #проверка, что заголовок является строкой и правильно заполняется
        publication = Publication.objects.create(author=author, title="Научная статья")
        self.assertEqual(str(publication), "Научная статья")

    def test_cascade_delete_author(self):
        author = Author.objects.create(full_name="Иван Иванов")
        Publication.objects.create(author=author, title="Публикация 1")
        Publication.objects.create(author=author, title="Публикация 2")
        self.assertEqual(author.publications.count(), 2)
        author.delete()
        self.assertEqual(Publication.objects.count(), 0)  #проверка каскадного удаления, удаляется автор и его статьи каскадно тоже


class RelatedModelTest(TestCase):
    def test_related_publications(self):
        author = Author.objects.create(full_name="Иван Иванов") #проверка создается автор с двумя публикациями, проверяем что каждая публикация есть в списке публикаций автора
        pub1 = Publication.objects.create(author=author, title="Публикация 1")
        pub2 = Publication.objects.create(author=author, title="Публикация 2")
        self.assertEqual(author.publications.count(), 2)
        self.assertIn(pub1, author.publications.all())
        self.assertIn(pub2, author.publications.all())
