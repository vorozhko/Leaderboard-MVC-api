from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from score_model import Score, ScoreCreate, ScorePublic
from database import SessionDep, lifespan
from score_service import ScoreService

app = FastAPI(lifespan=lifespan)


# Update score points
@app.put("/scores", response_model=ScorePublic)
def update_scores(user_id: int, points: int,  session: SessionDep):
    score_service = ScoreService(session)
    score_entry = score_service.score(user_id, points)
    if score_entry is None:
        raise HTTPException(status_code=404, detail=f"Score with user id {user_id} not found") 
    return score_entry

# Create score record
@app.post("/scores", response_model=ScorePublic)
def create_score(data: ScoreCreate, session: SessionDep):
    score_service = ScoreService(session)
    try:
        score_entry = score_service.create(data)    
    except ValueError:
        raise  HTTPException(status_code=401, detail="Can not create score record")
    return score_entry

# Get top 10 scores
@app.get("/scores", response_model=list[ScorePublic])
def get_top_scores(session: SessionDep, 
                   offset: int = 0,
                   limit: Annotated[int, Query(le=10)] = 10):
    score_service = ScoreService(session)
    score_top = score_service.top(offset, limit)
    return score_top

# Get score for user
@app.get("/scores/{user_id}", response_model=ScorePublic)
def get_score(user_id: int, session: SessionDep):
    score_service = ScoreService(session)
    try:
        score_entry = score_service.scoreById(user_id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Score with user id {user_id} not found")    
    return score_entry
