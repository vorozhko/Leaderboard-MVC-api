from sqlmodel import Session
from sqlmodel import select, desc
from sqlalchemy.sql.functions import func
from score_model import Score, ScoreCreate, ScorePublic

class ScoreService:
    def __init__(self, dbsession: Session):
        self.session = dbsession

    def score(self, id:int, points:int)->Score:
        score_entry = self.session.get(Score, id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")
        score_entry.points += points
        self.session.commit()
        return score_entry
    
    def create(self, data: ScoreCreate):
        score_entry = Score.model_validate(data)
        self.session.add(score_entry)
        self.session.commit()
        self.session.refresh(score_entry)
        return score_entry
    
    def top(self, offset=0, limit=10):
        stmt = select(
            Score,
            func.row_number().over(order_by=desc(Score.points)).label("rank")
        ).offset(offset).limit(limit).order_by(desc(Score.points))
        results = self.session.exec(stmt).all()
        
        return [
            ScorePublic(
                id=score.id,
                name=score.name,
                points=score.points,
                rank=rank
            )
            for score, rank in results
        ]

    def scoreById(self, id: int):
        score_entry = self.session.get(Score, id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")            
        stmt = select(
            func.count()
        ).where(Score.points >= score_entry.points)
        results = self.session.exec(stmt).one()

        return ScorePublic(
            id=score_entry.id,
            name=score_entry.name,
            points=score_entry.points,
            rank=results
        )