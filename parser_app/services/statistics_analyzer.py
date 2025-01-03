import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
import base64
from matplotlib import rcParams

class StatisticsAnalyzer:
    def __init__(self, queryset):
        """
        Инициализация с использованием queryset из базы данных.
        """
        self.data = self._prepare_data(queryset)


        rcParams['font.family'] = 'Arial'
        rcParams['axes.unicode_minus'] = False

    def _prepare_data(self, queryset):
        records = []
        for stat in queryset:
            print(f"Processing: {stat.author.full_name} - {stat.year}")
            records.append({
                'author': stat.author.full_name,
                'year': stat.year,
                'monograph': stat.monograph,
                'textbook': stat.textbook,
                'tutorial': stat.tutorial,
                'tutorial_griff': stat.tutorial_griff,
                'article_russian_journal': stat.article_russian_journal,
                'article_foreign_journal': stat.article_foreign_journal,
                'izvestia_vstu': stat.izvestia_vstu,
                'journals_vstu': stat.journals_vstu,
                'article_russian_collection': stat.article_russian_collection,
                'article_foreign_collection': stat.article_foreign_collection,
                'theses': stat.theses,
                'educational_complex': stat.educational_complex,
                'deposited_manuscript': stat.deposited_manuscript,
                'patent_document': stat.patent_document,
                'certificate': stat.certificate,
                'other_publications': stat.other_publications,
            })
        print(f"Records: {records}")
        return pd.DataFrame(records)

    def aggregate_statistics(self, column):
        """
        Вычисление агрегирующих значений для указанного столбца.
        """
        if column not in self.data.columns:
            raise ValueError(f"Столбец '{column}' не найден в данных.")

        series = self.data[column]
        return {
            "sum": series.sum(),
            "average": series.mean(),
            "median": series.median(),
            "max": series.max(),
            "min": series.min(),
        }

    def analyze(self):
        """
        Анализ данных и возвращение агрегирующих значений для всех колонок.
        """
        results = {}

        for column in [
            'monograph', 'textbook', 'tutorial', 'tutorial_griff',
            'article_russian_journal', 'article_foreign_journal',
            'izvestia_vstu', 'journals_vstu', 'article_russian_collection',
            'article_foreign_collection', 'theses', 'educational_complex',
            'deposited_manuscript', 'patent_document', 'certificate', 'other_publications'
        ]:
            if column in self.data.columns:
                results[column] = self.aggregate_statistics(column)
        return results

    def generate_graphs(self):
        """
        Создание графиков на основе данных.
        """
        graphs = {}


        renamed_columns = {
            'monograph': 'монография',
            'textbook': 'учебник',
            'tutorial': 'учебное_пособие',
            'tutorial_griff': 'учебное_пособие_с_грифом',
            'article_russian_journal': 'статья_в_российском_журнале',
            'article_foreign_journal': 'статья_в_зарубежном_журнале',
            'izvestia_vstu': 'известия_вту',
            'journals_vstu': 'журналы_вту',
            'article_russian_collection': 'статья_в_российском_сборнике',
            'article_foreign_collection': 'статья_в_зарубежном_сборнике',
            'theses': 'диссертации',
            'educational_complex': 'образовательный_комплекс',
            'deposited_manuscript': 'депонированный_рукопись',
            'patent_document': 'патентный_документ',
            'certificate': 'свидетельство',
            'other_publications': 'другие_публикации'
        }


        plt.figure(figsize=(12, 6))
        total_year_counts = self.data.groupby('year').sum()


        total_year_counts = total_year_counts.rename(columns=renamed_columns)

        total_year_counts.plot(kind='line', figsize=(12, 6))
        plt.title('Общее количество публикаций по годам')  # Русская надпись
        plt.xlabel('Год')  # Русская надпись
        plt.ylabel('Количество публикаций')  # Русская надпись
        graphs['total_publications'] = self._save_plot()

        return graphs

    def _save_plot(self):
        """
        Сохраняет текущий график в строку Base64.
        """
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight')
        plt.close()
        buffer.seek(0)
        img_data = buffer.getvalue()
        buffer.close()
        return base64.b64encode(img_data).decode('utf-8')
