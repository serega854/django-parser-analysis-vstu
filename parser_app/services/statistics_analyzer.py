from collections import defaultdict


class StatisticsAnalyzer:
    def __init__(self, authors_data):
        self.authors_data = authors_data
        self.aggregates = defaultdict(lambda: defaultdict(int))

    def aggregate_data(self):
        """
        Aggregates publication data for each author.
        """
        for author in self.authors_data:
            # Fetch related publications for the author using .all()
            publications = author.publications.all()  # Ensure you're calling .all()

            for publication in publications:
                # Aggregating based on publication type (monographs, textbooks, etc.)
                pub_type = publication.type
                self.aggregates[author.full_name][pub_type] += publication.sum

    def generate_graphs(self):
        """
        Generates graphs for aggregated data (e.g., Monographs, Textbooks).
        """
        data = pd.DataFrame(self.aggregates).T
        fig, axes = plt.subplots(1, len(data.columns), figsize=(10, 5))

        for idx, column in enumerate(data.columns):
            ax = axes[idx]
            data[column].plot(kind='bar', ax=ax, title=column, color='skyblue')
            ax.set_ylabel('Total')
            ax.set_xlabel('Author')

        plt.tight_layout()
        plt.savefig("static/graphs/authors_publications.png")
        plt.close()

    def get_aggregated_data(self):
        """
        Returns aggregated data for use in templates.
        """
        return self.aggregates
