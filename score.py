from sqlmodel import SQLModel, Field


class ScoreBase(SQLModel):
    name: str | None = Field(default=None)

class Score(ScoreBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    points: int = Field(default=0)
    
class ScoreCreate(ScoreBase):
    pass

class ScorePublic(ScoreBase):
    id: int
    points: int
    name: str
    rank: int