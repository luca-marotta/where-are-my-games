from datetime import datetime
from enum import Enum
from typing import Optional

class GameStatus(Enum):
    OWNED = "owned"
    BORROWED = "borrowed"

class BoardGame:
    def __init__(self, id: int, title: str, description: str, status: GameStatus,
                 owner: str, borrower: Optional[str], borrow_date: Optional[datetime],
                 return_date: Optional[datetime], genre: str, player_count: int,
                 play_time_minutes: int):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.owner = owner
        self.borrower = borrower
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.genre = genre
        self.player_count = player_count
        self.play_time_minutes = play_time_minutes
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()