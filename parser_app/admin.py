from django.contrib import admin
from .models import Author, PublicationStatistics, Publication

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ("full_name", "publication_count")  # Все поля модели Author
    search_fields = ("full_name",)  # Поиск по ФИО автора

@admin.register(PublicationStatistics)
class PublicationStatisticsAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "year",
        "monograph",
        "textbook",
        "tutorial",
        "tutorial_griff",
        "article_russian_journal",
        "article_foreign_journal",
        "izvestia_vstu",
        "journals_vstu",
        "article_russian_collection",
        "article_foreign_collection",
        "theses",
        "educational_complex",
        "deposited_manuscript",
        "patent_document",
        "certificate",
        "other_publications",
    )  # Все поля модели PublicationStatistics
    list_filter = ("year", "author")  # Фильтрация по году и автору
    search_fields = ("author__full_name",)  # Поиск по ФИО автора

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ("author", "title")  # Все поля модели Publication
    search_fields = ("author__full_name", "title")  # Поиск по ФИО автора и названию публикации
