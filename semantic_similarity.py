from sentence_transformers import SentenceTransformer, util

class SemanticSimilarity:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(model_name)

    def compute_scores(self, query_text: str, candidate_texts: list):
        """
        Compute cosine similarity scores between query and candidate texts using embeddings.
        """
        query_emb = self.model.encode(query_text, convert_to_tensor=True)
        candidate_embs = self.model.encode(candidate_texts, convert_to_tensor=True)
        scores = util.cos_sim(query_emb, candidate_embs)[0].cpu().numpy()
        return scores
