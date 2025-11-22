from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime
from schemas import (
    BoardGameCreate,
    BoardGameUpdate,
    BoardGameResponse,
    BoardGameListResponse,
    BorrowGameRequest,
    ReturnGameRequest,
    ErrorResponse
)
from models import GameStatus

router = APIRouter(prefix="/api/games", tags=["games"])

# In-memory storage for games (replace with database later)
games_db = {}
next_id = 1

@router.post("/", response_model=BoardGameResponse, status_code=status.HTTP_201_CREATED)
async def create_game(game: BoardGameCreate):
    """Create a new board game in the inventory."""
    global next_id
    game_id = next_id
    next_id += 1
    
    games_db[game_id] = {
        "id": game_id,
        "title": game.title,
        "description": game.description,
        "status": game.status,
        "owner": game.owner,
        "borrower": game.borrower,
        "borrow_date": game.borrow_date,
        "return_date": game.return_date,
        "genre": game.genre,
        "player_count": game.player_count,
        "play_time_minutes": game.play_time_minutes,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    return games_db[game_id]

@router.get("/", response_model=BoardGameListResponse)
async def list_games(status_filter: Optional[str] = None, owner: Optional[str] = None):
    """Get all board games from the inventory with optional filters."""
    games_list = list(games_db.values())
    
    # Filter by status if provided
    if status_filter:
        games_list = [g for g in games_list if g["status"] == status_filter]
    
    # Filter by owner if provided
    if owner:
        games_list = [g for g in games_list if g["owner"] == owner]
    
    return {
        "total": len(games_list),
        "games": games_list
    }

@router.get("/{game_id}", response_model=BoardGameResponse)
async def get_game(game_id: int):
    """Get a specific board game by ID."""
    if game_id not in games_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    return games_db[game_id]

@router.put("/{game_id}", response_model=BoardGameResponse)
async def update_game(game_id: int, game_update: BoardGameUpdate):
    """Update a board game's information."""
    if game_id not in games_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    
    game = games_db[game_id]
    update_data = game_update.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if value is not None:
            game[field] = value
    
    game["updated_at"] = datetime.utcnow()
    games_db[game_id] = game
    
    return game

@router.delete("/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game(game_id: int):
    """Delete a board game from the inventory."""
    if game_id not in games_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    del games_db[game_id]
    return None

@router.post("/{game_id}/borrow", response_model=BoardGameResponse)
async def borrow_game(game_id: int, borrow_request: BorrowGameRequest):
    """Mark a game as borrowed."""
    if game_id not in games_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    
    game = games_db[game_id]
    
    # Check if game is already borrowed
    if game["status"] == "borrowed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game '{game['title']}' is already borrowed by {game['borrower']}"
        )
    
    game["status"] = "borrowed"
    game["borrower"] = borrow_request.borrower
    game["borrow_date"] = borrow_request.borrow_date
    game["return_date"] = borrow_request.return_date
    game["updated_at"] = datetime.utcnow()
    
    games_db[game_id] = game
    return game

@router.post("/{game_id}/return", response_model=BoardGameResponse)
async def return_game(game_id: int, return_request: ReturnGameRequest):
    """Mark a borrowed game as returned."""
    if game_id not in games_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with ID {game_id} not found"
        )
    
    game = games_db[game_id]
    
    # Check if game is borrowed
    if game["status"] != "borrowed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game '{game['title']}' is not currently borrowed"
        )
    
    game["status"] = "available"
    game["borrower"] = None
    game["borrow_date"] = None
    game["return_date"] = return_request.return_date
    game["updated_at"] = datetime.utcnow()
    
    games_db[game_id] = game
    return game

@router.get("/borrowed/all", response_model=BoardGameListResponse)
async def get_borrowed_games():
    """Get all currently borrowed games."""
    borrowed_games = [g for g in games_db.values() if g["status"] == "borrowed"]
    return {
        "total": len(borrowed_games),
        "games": borrowed_games
    }

@router.get("/available/all", response_model=BoardGameListResponse)
async def get_available_games():
    """Get all games in the user's possession (not borrowed out)."""
    available_games = [g for g in games_db.values() if g["status"] == "available"]
    return {
        "total": len(available_games),
        "games": available_games
    }