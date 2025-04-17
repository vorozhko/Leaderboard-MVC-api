from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from score import Score, ScoreCreate, ScorePublic
from database import SessionDep, lifespan
from sqlmodel import select, desc

app = FastAPI(lifespan=lifespan)


# Update score points
@app.put("/scores", response_model=ScorePublic)
def update_scores(user_id: int, points: int,  session: SessionDep):
    score_entry = session.get(Score, user_id)
    if score_entry is None:
        raise HTTPException(status_code=404, detail=f"Score with user id {user_id} not found") 
    score_entry.points += points
    session.commit()
    return score_entry

# Create score record
@app.post("/score", response_model=ScorePublic)
def create_score(user: ScoreCreate, session: SessionDep):
    score_entry = Score.model_validate(user)
    session.add(score_entry)
    session.commit()
    session.refresh(score_entry)
    if not score_entry.id:
         raise  HTTPException(status_code=401, detail="Can not create score record")
    return score_entry

# Get top 10 scores

@app.get("/scores", response_model=list[ScorePublic])
def get_top_scores(session: SessionDep, 
                   offset: int = 0,
                   limit: Annotated[int, Query(le=10)] = 10):
    stmt = select(Score).offset(offset).limit(limit).order_by(desc(Score.points))
    scores = session.exec(stmt).all()
    return scores