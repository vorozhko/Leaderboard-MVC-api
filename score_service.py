from score_repository import ScoreRepository

class ScoreService:
    def __init__(self, repository: ScoreRepository):
        self.repository = repository

    def score(self, id: int, points: int):
        score_entry = self.repository.get_score_by_id(id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")
        return self.repository.update_score_points(score_entry, points)

    def create(self, data):
        return self.repository.create_score(data)

    def top(self, offset=0, limit=10):
        results = self.repository.get_top_scores(offset, limit)
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
        score_entry = self.repository.get_score_by_id(id)
        if score_entry is None:
            raise ValueError(f"No Score entry found with id {id}")
        rank = self.repository.get_rank_by_score(score_entry)
        return {
            "id": score_entry.id,
            "name": score_entry.name,
            "points": score_entry.points,
            "rank": rank
        }