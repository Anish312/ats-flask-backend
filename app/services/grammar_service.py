from textblob import TextBlob

class GrammarService:
    def __init__(self, lang="en"):
        self.lang = lang

    def check_text(self, text: str):
        """Check text for spelling and simple grammar issues using TextBlob"""
        blob = TextBlob(text)

        # Spelling corrected text
        corrected_text = str(blob.correct())

        errors = []
        # Compare each word with corrected version
        for original, corrected in zip(blob.words, TextBlob(corrected_text).words):
            if original.lower() != corrected.lower():
                errors.append({
                    "message": f"Possible spelling mistake in '{original}'",
                    "error_text": original,
                    "suggestions": [corrected],
                    "context": text,
                    "offset": text.find(original),
                    "length": len(original)
                })

        return {
            "original_text": text,
            "corrected_text": corrected_text,
            "errors": errors,
            "total_errors": len(errors)
        }
