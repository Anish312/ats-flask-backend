from fastapi import FastAPI
from app.routes import nlp_routes
from app.routes import tokenization_routes
from app.routes import synonym_routes
from app.routes import matching_routes
from app.routes import weighting_routes
from app.routes import scoring_routes
from app.routes import ats_extra_routes
from app.routes import ats_score_routes
from app.routes import result_routes
from app.routes import grammar_routes  
app = FastAPI()

# Include your router
app.include_router(nlp_routes.router, tags=["NLP"])
app.include_router(tokenization_routes.router, tags=["Tokenizer"])
app.include_router(synonym_routes.router, tags=["synonym"])
app.include_router(matching_routes.router, tags=["matching"])
app.include_router(weighting_routes.router, tags=["weighting"])
app.include_router(scoring_routes.router, tags=["scoring"])
app.include_router(ats_extra_routes.router, tags=["extra"])
app.include_router(ats_score_routes.router, tags=["ats"])
app.include_router(result_routes.router, tags=["result"])
app.include_router(grammar_routes.router, prefix="/grammar", tags=["Grammar"])

@app.get("/")
def read_root():
    
    return {"message": "ATS Scoring API is running!"} 