import re
from typing import List, Dict
import spacy


class TokenizerService:
    def __init__(self):
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            raise RuntimeError("SpaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")

    def tokenize(self, text: str) -> Dict[str, List[str]]:
        if not text or not text.strip():
            return {"tokens": [], "phrases": []}

        doc = self.nlp(text)

        # Clean tokens: use text, not just lemma, keep alphanum, dots, hyphens
        tokens = sorted(set(
            re.sub(r"[^a-zA-Z0-9.\-]", "", token.text.lower())
            for token in doc
            if token.text.strip() 
            and not token.is_stop
            and re.sub(r"[^a-zA-Z0-9.\-]", "", token.text)  # ensure valid
        ))

        # Phrases = noun chunks + entities (keep spaces, dots, hyphens)
        raw_phrases = [
            chunk.text for chunk in doc.noun_chunks
        ] + [
            ent.text for ent in doc.ents
        ]

        phrases = sorted(set(
            re.sub(r"[^a-zA-Z0-9.\-\s]", "", phrase).strip().lower()
            for phrase in raw_phrases
            if phrase.strip() and any(c.isalpha() for c in phrase)
        ))

        return {
            "tokens": tokens,
            "phrases": phrases
        }
