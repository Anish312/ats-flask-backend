from sentence_transformers import SentenceTransformer, util
import torch

class SynonymService:
    def __init__(self):
        # Lightweight embedding model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def map_synonyms(self, tokens, resume_tokens):
        """
        Map resume tokens to job tokens using semantic similarity.
        Returns dict: {resume_token: {"best_match": jd_term, "score": similarity}}
        """
        mapped = {}

        # Ensure uniqueness & convert to list of strings
        tokens = [str(t).lower().strip() for t in set(tokens)]
        resume_tokens = [str(t).lower().strip() for t in set(resume_tokens)]

        if not tokens or not resume_tokens:
            return mapped  # nothing to compare

        # Encode
        jd_embeddings = self.model.encode(tokens, convert_to_tensor=True)
        resume_embeddings = self.model.encode(resume_tokens, convert_to_tensor=True)

        # Compute cosine similarity
        cosine_scores = util.cos_sim(resume_embeddings, jd_embeddings)

        # Map each resume token to its best JD match
        for i, resume_token in enumerate(resume_tokens):
            # Get best match index
            best_match_idx = torch.argmax(cosine_scores[i]).item()
            best_score = cosine_scores[i][best_match_idx].item()

            mapped[resume_token] = {
                "best_match": tokens[best_match_idx],
                "score": round(float(best_score), 3),
            }

        return mapped
