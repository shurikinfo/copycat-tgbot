from datetime import datetime


class BookModel:
    def __init__(self, title: str, author: str, year: datetime.year):
        self.title = title
        self.author = author
        self.year = year
        self.created_at = datetime.now().isoformat()
