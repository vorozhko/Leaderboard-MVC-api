from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from score_model import ScoreCreate, ScorePublic
from database import SessionDep, RedisSessionDep, lifespan
from score_service import ScoreService
from score_repository import ScoreRepositorySQL, ScoreRepositoryRedis

app = FastAPI(lifespan=lifespan)

# Update score points
@app.put("/scores", response_model=ScorePublic)
def update_scores(id: int, points: int, session: SessionDep):
    service = ScoreService(ScoreRepositorySQL(session), ScoreRepositoryRedis(RedisSessionDep))
    try:        
        score_entry = service.score(id, points)        
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
    # Refresh the record with current rank
    score_entry = service.scoreById(score_entry.id)
    return score_entry

# Create score record
@app.post("/scores", response_model=ScorePublic)
def create_score(data: ScoreCreate, session: SessionDep):
    service = ScoreService(ScoreRepositorySQL(session), ScoreRepositoryRedis(RedisSessionDep))
    try:
        if not service.isGamerExist(data.name):
            score_entry = service.create(data)    
        else:
            raise ValueError(f"Duplicate name {data.name}")
    except ValueError as e:
        raise  HTTPException(status_code=401, detail=str(e))
    # Refresh the record with current rank
    score_entry = service.scoreById(score_entry.id)
    return score_entry

# Get top 10 scores
@app.get("/scores", response_model=list[ScorePublic])
def get_top_scores(session: SessionDep, 
                   offset: int = 0,
                   limit: Annotated[int, Query(le=10)] = 10):
    service = ScoreService(ScoreRepositorySQL(session), ScoreRepositoryRedis(RedisSessionDep))
    score_top = service.top(offset, limit)
    return score_top

# Get score for user
@app.get("/scores/{id}", response_model=ScorePublic)
def get_score(id: int, session: SessionDep):
    
    service = ScoreService(ScoreRepositorySQL(session), ScoreRepositoryRedis(RedisSessionDep))
    try:
        score_entry = service.scoreById(id)
    except ValueError:
        raise HTTPException(status_code=404, detail=f"Score with id {id} not found")    
    
    return score_entry
