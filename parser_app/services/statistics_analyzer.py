import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from io import BytesIO
import base64

class StatisticsAnalyzer:
    def __init__(self, queryset):
        """
        Инициализация с использованием queryset из базы данных.
        """
        self.data = self._prepare_data(queryset)

    def _prepare_data(self, queryset):
        """
        Преобразование queryset в DataFrame для анализа.
        """
        records = [
            {
                'author': stat.author.full_name,
                'year': stat.year,
                'monograph': stat.monograph,
                'textbook': stat.textbook,
                'tutorial': stat.tutorial,
                'other_publications': stat.other_publications,
            }
            for stat in queryset
        ]
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
        for column in ['monograph', 'textbook', 'tutorial', 'other_publications']:
            if column in self.data.columns:
                results[column] = self.aggregate_statistics(column)
        return results

    def generate_graphs(self):
        """
        Создание графиков на основе данных.
        """
        graphs = {}

        # Распределение публикаций
        plt.figure(figsize=(10, 6))
        sns.histplot(self.data[['monograph', 'textbook', 'tutorial', 'other_publications']], kde=True, palette='muted')
        plt.title('Распределение публикаций по типам')
        graphs['distribution'] = self._save_plot()

        # Boxplot для сравнения типов публикаций
        plt.figure(figsize=(10, 6))
        sns.boxplot(data=self.data[['monograph', 'textbook', 'tutorial', 'other_publications']], palette='coolwarm')
        plt.title('Boxplot публикаций')
        graphs['boxplot'] = self._save_plot()

        # Парные графики (Pairplot)
        sns.pairplot(self.data[['monograph', 'textbook', 'tutorial', 'other_publications']])
        plt.suptitle('Парные графики', y=1.02)
        graphs['pairplot'] = self._save_plot()

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