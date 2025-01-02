#models.py

from django.db import models

class Author(models.Model):
    full_name = models.CharField(max_length=255, verbose_name="ФИО автора")
    publication_count = models.PositiveIntegerField(default=0, verbose_name="Количество публикаций")

    def __str__(self):
        return self.full_name

class PublicationStatistics(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="statistics")
    year = models.PositiveIntegerField(verbose_name="Год")
    monograph = models.PositiveIntegerField(default=0, verbose_name="Монография")
    textbook = models.PositiveIntegerField(default=0, verbose_name="Учебник")
    tutorial = models.PositiveIntegerField(default=0, verbose_name="Учебное пособие")
    tutorial_griff = models.PositiveIntegerField(default=0, verbose_name="Учебное пособие (гриф)")
    article_russian_journal = models.PositiveIntegerField(default=0, verbose_name="Статья из российского журнала")
    article_foreign_journal = models.PositiveIntegerField(default=0, verbose_name="Статья из зарубежного журнала")
    izvestia_vstu = models.PositiveIntegerField(default=0, verbose_name="Известия ВолгГТУ")
    journals_vstu = models.PositiveIntegerField(default=0, verbose_name="Журналы ВолгГТУ")
    article_russian_collection = models.PositiveIntegerField(default=0, verbose_name="Статья из российского сборника")
    article_foreign_collection = models.PositiveIntegerField(default=0, verbose_name="Статья из зарубежного сборника")
    theses = models.PositiveIntegerField(default=0, verbose_name="Тезисы докладов")
    educational_complex = models.PositiveIntegerField(default=0, verbose_name="Учебно-методический комплекс")
    deposited_manuscript = models.PositiveIntegerField(default=0, verbose_name="Депонированная рукопись")
    patent_document = models.PositiveIntegerField(default=0, verbose_name="Патентный документ")
    certificate = models.PositiveIntegerField(default=0, verbose_name="Свидетельство")
    other_publications = models.PositiveIntegerField(default=0, verbose_name="Прочие публикации")

    def __str__(self):
        return f"Статистика публикаций {self.author.full_name} за {self.year} год"

class Publication(models.Model):
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name="publications")
    title = models.TextField(verbose_name="Название публикации")

    def __str__(self):
        return self.title
