from enum import Enum
from pydantic import BaseModel

class GameStatusSchema(str, Enum):
    AVAILABLE = "available"
    BORROWED = "borrowed"

class BoardGameBase(BaseModel):
    title: str
    description: str
    genre: str
    player_count: int
    play_time_minutes: int

class BoardGameCreate(BoardGameBase):
    status: GameStatusSchema
    owner: str
    borrower: str
    borrow_date: str
    return_date: str

class BoardGameUpdate(BoardGameBase):
    status: GameStatusSchema = None
    owner: str = None
    borrower: str = None
    borrow_date: str = None
    return_date: str = None

class BoardGameResponse(BoardGameBase):
    id: int
    status: GameStatusSchema
    owner: str
    borrower: str = None
    dates: str = None
    timestamps: str = None

class BoardGameListResponse(BaseModel):
    total: int
    games: list[BoardGameResponse]

class BorrowGameRequest(BaseModel):
    borrower: str
    borrow_date: str
    return_date: str

class ReturnGameRequest(BaseModel):
    return_date: str

class ErrorResponse(BaseModel):
    detail: str
    status_code: int
