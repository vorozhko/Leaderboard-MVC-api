import logging
from score_repository import ScoreRepositorySQL, ScoreRepositoryRedis


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
        results = self.repo_sql.get_top_scores(offset, limit)
        return [
            {
                "id": score.id,
                "name": score.name,
                "points": score.points,
                "rank": rank
            }
            for score, rank in results
        ]

    def scoreById(self, id: int):
        score_entry = self.repo_sql.get_score_by_id(id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")        
        try:
            rank = self.repo_valkey.get_rank_by_score(score_entry.name, score_entry.points)
            rank_points = int(rank)
        except (ValueError, TypeError) as e:
            logging.error(f"Invalid rank value: {rank}. Error: {e}")
            raise ValueError("Rank should be a valid integer") from e
        score_entry.rank = rank_points
        return score_entry