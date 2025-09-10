from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, List

# Import preprocessing functions from normalization_service
from app.services.normalization_service import (
    preprocess_text,
    handle_spelling_variants,
    remove_stopwords,
    lemmatize_text,
    normalize_tech_stack
)
from app.services.skill_extractor import extract_skills

router = APIRouter()

# --- Request Models ---
class TextRequest(BaseModel):
    text: str
    options: Dict = {}

class BatchRequest(BaseModel):
    texts: List[str]
    options: Dict = {}

class JobDesc(BaseModel):
    text: str

# --- Routes ---
@router.post('/extract-skills')
def extract_skills_endpoint(job: JobDesc):
    try:
        skills = extract_skills(job.text)
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get('/health')
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "text-preprocessor"}


@router.post('/preprocess')
def preprocess(request: TextRequest):
    """
    Main preprocessing endpoint
    """
    try:
        text = request.text
        options = request.options or {}

        # Get options with defaults
        remove_stopwords_flag = options.get('remove_stopwords', True)
        lemmatize = options.get('lemmatize', True)
        normalize_tech = options.get('normalize_tech', True)
        handle_spelling = options.get('handle_spelling', True)
        keep_words = set(options.get('keep_words', []))

        # Step 1: Basic preprocessing
        processed_text = preprocess_text(text)

        # Step 2: Handle spelling variants
        if handle_spelling:
            processed_text = handle_spelling_variants(processed_text)

        # Step 3: Normalize tech stack
        if normalize_tech:
            processed_text = normalize_tech_stack(processed_text)

        # Step 4: Remove stopwords (unless specified to keep)
        if remove_stopwords_flag:
            processed_text = remove_stopwords(processed_text, keep_words)

        # Step 5: Lemmatization
        if lemmatize:
            processed_text = lemmatize_text(processed_text)

        return {
            "original_text": text,
            "processed_text": processed_text.strip(),
            "options_used": options
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/batch_preprocess')
def batch_preprocess(request: BatchRequest):
    """
    Batch preprocessing endpoint for multiple texts
    """
    try:
        texts = request.texts
        options = request.options or {}

        results = []
        for text in texts:
            result = preprocess_text(text)

            if options.get('handle_spelling', True):
                result = handle_spelling_variants(result)
            if options.get('normalize_tech', True):
                result = normalize_tech_stack(result)
            if options.get('remove_stopwords', True):
                result = remove_stopwords(result, set(options.get('keep_words', [])))
            if options.get('lemmatize', True):
                result = lemmatize_text(result)

            results.append(result.strip())

        return {
            "original_texts": texts,
            "processed_texts": results,
            "options_used": options
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post('/normalize_tech')
def normalize_tech_endpoint(request: TextRequest):
    """
    Specialized endpoint for tech stack normalization only
    """
    try:
        text = request.text
        normalized_text = normalize_tech_stack(text.lower())

        return {
            "original_text": text,
            "normalized_tech_text": normalized_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
