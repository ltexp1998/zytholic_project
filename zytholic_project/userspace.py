from numpy.random.mtrand import choice, rand

DB_ID = [0]

class User:
    """
    A class to handle user beer prefences
    """
    def __init__(self,
                 name: str,
                 mail: str,
                 age: int) -> None:
        self.name = name
        self.email = mail
        self.age = age
        self.id = self.create_user_id()
        self.liked = set()
        
    def create_user_id(self):
        max_db = DB_ID[-1]
        user_id = max_db + 1
        DB_ID.append(user_id)
        return user_id
    
    def add_liked_beer(self, beer_name: str):
        """Add beer name to the set"""
        self.liked.add(beer_name)
        
    def unlike_beer(self, beer_name):
        """Remove a beer from the liked list"""
        #if beer_name in self.liked:
        self.liked.discard(beer_name)

