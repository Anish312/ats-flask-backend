import spacy

class SynonymService:
    def __init__(self):
        # Load lightweight spaCy model (10MB)
        self.nlp = spacy.load("en_core_web_sm")

    def map_synonyms(self, tokens, resume_tokens):
        mapped = {}
        tokens = [str(t).lower().strip() for t in set(tokens)]
        resume_tokens = [str(t).lower().strip() for t in set(resume_tokens)]

        if not tokens or not resume_tokens:
            return mapped

        # Convert to docs
        token_docs = [self.nlp(tok) for tok in tokens]
        resume_docs = [self.nlp(tok) for tok in resume_tokens]

        for r_doc, r_tok in zip(resume_docs, resume_tokens):
            best_match, best_score = None, -1
            for t_doc, t_tok in zip(token_docs, tokens):
                score = r_doc.similarity(t_doc)
                if score > best_score:
                    best_score, best_match = score, t_tok

            mapped[r_tok] = {"best_match": best_match, "score": round(best_score, 3)}

        return mapped
