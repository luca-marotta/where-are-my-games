# CRUD Operations for Board Games

class BoardGame:
    def __init__(self, title, genre, year_published):
        self.title = title
        self.genre = genre
        self.year_published = year_published

# Simulating a database with a list
board_games_db = []

# Create
def create_board_game(title, genre, year_published):
    new_game = BoardGame(title, genre, year_published)
    board_games_db.append(new_game)
    return new_game

# Read
def get_board_game(title):
    for game in board_games_db:
        if game.title == title:
            return game
    return None

# Update
def update_board_game(title, genre=None, year_published=None):
    game = get_board_game(title)
    if game:
        if genre:
            game.genre = genre
        if year_published:
            game.year_published = year_published
        return game
    return None

# Delete
def delete_board_game(title):
    game = get_board_game(title)
    if game:
        board_games_db.remove(game)
        return game
    return None

# Example usage
# create_board_game('Catan', 'Strategy', 1995)
