import logging
from score_repository import ScoreRepositorySQL, ScoreRepositoryRedis
import asyncio


class ScoreService:
    def __init__(self, repo_sql: ScoreRepositorySQL, repo_valkey: ScoreRepositoryRedis):
        self.repo_sql = repo_sql
        self.repo_valkey = repo_valkey

    def score(self, id: int, points: int):
        score_entry = self.repo_sql.get_score_by_id(id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")
        self.repo_valkey.update_score(score_entry.name, points)
        return self.repo_sql.update_score_points(score_entry, points)

    def create(self, data):
        entry = self.repo_sql.create_score(data)
        self.repo_valkey.create_score(entry.name)
        return entry

    def top(self, offset=0, limit=10):
        
        top_users = self.repo_valkey.get_top_scores(offset, limit)
        results = self.repo_sql.getScoresByUsers(top_users)

        return results
    
    def scoreById(self, id: int):
        score_entry = self.repo_sql.get_score_by_id(id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")        
        try:
            rank_points = self.repo_valkey.get_rank_by_name(score_entry.name)
        except (ValueError, TypeError) as e:
            logging.error(f"Invalid rank value: {rank_points}. Error: {e}")
            raise ValueError("Rank should be a valid integer") from e
        score_entry.rank = rank_points
        return score_entry
    
    def isGamerExist(self, name: str)->bool:
        score_entry = self.repo_sql.get_score_by_name(name)
        if score_entry:
            return True
        return False