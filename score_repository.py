from sqlmodel import Session
from score_model import Score, ScoreCreate

class ScoreRepository:
    def __init__(self, dbsession: Session):
        self.session = dbsession

    def get_score_by_id(self, id: int):
        raise NotImplementedError

    def update_score_points(self, score_entry: Score, points: int):
        raise NotImplementedError

    def create_score(self, data: ScoreCreate):
        raise NotImplementedError

    def get_top_scores(self, offset=0, limit=10):
        raise NotImplementedError

    def get_rank_by_score(self, score_entry: Score):
        raise NotImplementedError


class ScoreRepositorySQL(ScoreRepository):    

    def get_score_by_id(self, id: int):
        return self.session.get(Score, id)

    def update_score_points(self, score_entry: Score, points: int):
        score_entry.points += points
        self.session.commit()
        return score_entry

    def create_score(self, data: ScoreCreate):
        score_entry = Score.model_validate(data)
        self.session.add(score_entry)
        self.session.commit()
        self.session.refresh(score_entry)
        return score_entry

    def get_top_scores(self, offset=0, limit=10):
        from sqlalchemy.sql.functions import func
        from sqlmodel import select, desc

        stmt = select(
            Score,
            func.row_number().over(order_by=desc(Score.points)).label("rank")
        ).offset(offset).limit(limit).order_by(desc(Score.points))
        return self.session.exec(stmt).all()

    def get_rank_by_score(self, score_entry: Score):
        from sqlalchemy.sql.functions import func
        from sqlmodel import select

        stmt = select(
            func.count()
        ).where(Score.points >= score_entry.points)
        return self.session.exec(stmt).one()