from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class PreFilter:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()
        self.tfidf_matrix = None

    def fit(self, texts: pd.Series):
        """Fit TF-IDF on all ticket texts."""
        self.tfidf_matrix = self.vectorizer.fit_transform(texts)

    def get_top_candidates(self, query_idx: int, N: int = 20) -> list:
        """
        Returns indices of top-N most similar tickets (excluding the query itself).
        """
        query_vector = self.tfidf_matrix[query_idx]
        cos_sim = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
        """
        Since first index will belong to query ticket since that is what matches most, we have to exclude that.
        So, we find tickets from index 1 to N+1.
        """
        top_indices = cos_sim.argsort()[::-1][1:N+1]
        return top_indices
