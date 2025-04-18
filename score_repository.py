import asyncio
from sqlmodel import Session
from score_model import Score, ScoreCreate
from valkey import Valkey

class ScoreRepository:

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



class ScoreRepositoryRedis():

    def __init__(self, dbsession: Valkey):
        self.session = dbsession
        self.dbname = "leaderboard"

    def create_score(self, name: str):
        # by default 0 points assigned
        if name is None:
            raise ValueError("Score name cannot be None")
        return self.session.zadd(self.dbname, {name: 0})


    def get_rank_by_name(self, name: str)->int:
        if name is None:
            raise ValueError("Score name cannot be None")
        rank = self.session.zrevrank(self.dbname, bytes(name, "utf-8"), withscore=False)
        if rank is None:
            raise ValueError("Rank for the user not found")
        if type(rank) is list:
            rank = rank[0]
        return int(rank) + 1

    def update_score(self, name: str, points: int):
        self.session.zadd(self.dbname, {name: points})

class ScoreRepositorySQL(ScoreRepository):    

    def __init__(self, dbsession: Session):
        self.session = dbsession

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
