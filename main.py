from typing import Annotated
from fastapi import FastAPI, HTTPException, Query
from score import Score, ScoreCreate, ScorePublic
from database import SessionDep, lifespan
from sqlmodel import select, desc
from sqlalchemy.sql.functions import func
from sqlalchemy.sql import over


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
@app.post("/scores", response_model=ScorePublic)
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
    stmt = select(
        Score,
        func.row_number().over(order_by=desc(Score.points)).label("rank")
        ).offset(offset).limit(limit).order_by(desc(Score.points))
    results = session.exec(stmt).all()
    return [
        ScorePublic(
            id=score.id,
            name=score.name,
            points=score.points,
            rank=rank
        )
        for score, rank in results
    ]

# Get score for user
@app.get("/scores/{user_id}", response_model=ScorePublic)
def get_score(user_id: int, session: SessionDep):
    score_entry = session.get(Score, user_id)
    if score_entry is None:
        raise HTTPException(status_code=404, detail=f"Score with user id {user_id} not found")
    stmt = select(
        func.count()
    ).where(Score.points >= score_entry.points)
    results = session.exec(stmt).one()
    return ScorePublic(
            id=score_entry.id,
            name=score_entry.name,
            points=score_entry.points,
            rank=results
        )
