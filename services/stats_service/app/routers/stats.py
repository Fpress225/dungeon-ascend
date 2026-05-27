from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.deps import get_current_user
from app.models import PlayerStats
from app.schemas import (
    GameSessionRecord,
    LeaderboardEntry,
    PlayerStatsResponse,
    PlayerStatsUpdate,
    TokenUser,
)

router = APIRouter(prefix="/stats", tags=["stats"])


def _get_or_create_stats(db: Session, player_id: int, username: str) -> PlayerStats:
    stats = db.get(PlayerStats, player_id)
    if stats is None:
        stats = PlayerStats(player_id=player_id, username=username)
        db.add(stats)
        db.commit()
        db.refresh(stats)
    elif stats.username != username:
        stats.username = username
        db.commit()
        db.refresh(stats)
    return stats


def _ensure_owner(player_id: int, current_user: TokenUser) -> None:
    if player_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another player's stats",
        )


@router.get("/me", response_model=PlayerStatsResponse)
def get_my_stats(
    current_user: Annotated[TokenUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PlayerStats:
    return _get_or_create_stats(db, current_user.user_id, current_user.username)


@router.get("/{player_id}", response_model=PlayerStatsResponse)
def get_player_stats(
    player_id: int,
    current_user: Annotated[TokenUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PlayerStats:
    _ensure_owner(player_id, current_user)
    return _get_or_create_stats(db, player_id, current_user.username)


@router.put("/{player_id}", response_model=PlayerStatsResponse)
def update_player_stats(
    player_id: int,
    body: PlayerStatsUpdate,
    current_user: Annotated[TokenUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PlayerStats:
    _ensure_owner(player_id, current_user)
    stats = _get_or_create_stats(db, player_id, current_user.username)

    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(stats, field, value)

    db.commit()
    db.refresh(stats)
    return stats


@router.post("/{player_id}/record", response_model=PlayerStatsResponse)
def record_game_session(
    player_id: int,
    body: GameSessionRecord,
    current_user: Annotated[TokenUser, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> PlayerStats:
    _ensure_owner(player_id, current_user)
    stats = _get_or_create_stats(db, player_id, current_user.username)

    stats.games_played += 1
    if body.won:
        stats.wins += 1
    if body.died:
        stats.deaths += 1
    stats.floors_reached += body.floor_reached
    stats.best_floor = max(stats.best_floor, body.floor_reached)
    stats.total_score += body.score
    stats.play_time_seconds += body.play_time_seconds

    db.commit()
    db.refresh(stats)
    return stats


@router.get("/leaderboard/top", response_model=list[LeaderboardEntry])
def leaderboard(
    db: Annotated[Session, Depends(get_db)],
    limit: int = 10,
) -> list[PlayerStats]:
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="limit 1-100")

    rows = (
        db.query(PlayerStats)
        .order_by(PlayerStats.total_score.desc(), PlayerStats.best_floor.desc())
        .limit(limit)
        .all()
    )
    return rows
