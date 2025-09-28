import pandas as pd
from data_loader import load_tickets
from prefilter import PreFilter
from semantic_similarity import SemanticSimilarity

class SimilarityEngine:
    def __init__(self, tickets: pd.DataFrame):
        self.tickets = load_tickets(tickets)
        self.prefilter = PreFilter()
        self.prefilter.fit(self.tickets['text'])
        self.semantic = SemanticSimilarity()

    def find_similar(self, query_index: int, top_k: int = 5, final_n_filter: int = 3):
        """
        Find most similar tickets for a given query ticket index.
        
        Args:
            query_index (int): Index of the query ticket.
            top_k (int): Number of candidates to keep after TF-IDF prefilter.
            final_n_filter (int): Number of top results to return after semantic similarity.
        """
        # ----- Stage 1: Pre-filter -----
        candidate_indices = self.prefilter.get_top_candidates(query_index, top_k)
        candidates = self.tickets.iloc[candidate_indices]

        # ----- Stage 2: Semantic similarity -----
        query_text = self.tickets.iloc[query_index]['Summary'] + " " + self.tickets.iloc[query_index]['Description']
        candidate_texts = (candidates['Summary'] + " " + candidates['Description']).tolist()
        scores = self.semantic.compute_scores(query_text, candidate_texts)

        # Attach scores
        results = candidates.copy()
        results['score'] = scores

        # Sort and apply final filter
        results = results.sort_values(by='score', ascending=False).head(final_n_filter)
        return results
