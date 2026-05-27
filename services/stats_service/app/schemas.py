from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class PlayerStatsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    player_id: int
    username: str
    games_played: int
    wins: int
    deaths: int
    floors_reached: int
    best_floor: int
    total_score: int
    play_time_seconds: int
    updated_at: datetime


class PlayerStatsUpdate(BaseModel):
    games_played: int | None = Field(default=None, ge=0)
    wins: int | None = Field(default=None, ge=0)
    deaths: int | None = Field(default=None, ge=0)
    floors_reached: int | None = Field(default=None, ge=0)
    best_floor: int | None = Field(default=None, ge=0)
    total_score: int | None = Field(default=None, ge=0)
    play_time_seconds: int | None = Field(default=None, ge=0)


class GameSessionRecord(BaseModel):
    won: bool = False
    died: bool = False
    floor_reached: int = Field(ge=0, default=0)
    score: int = Field(ge=0, default=0)
    play_time_seconds: int = Field(ge=0, default=0)


class LeaderboardEntry(BaseModel):
    player_id: int
    username: str
    total_score: int
    best_floor: int
    wins: int


class TokenUser(BaseModel):
    user_id: int
    username: str
