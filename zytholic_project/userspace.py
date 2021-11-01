import pandas as pd
import os.path

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
        """Take the last user ID and add one"""
        max_db = DB_ID[-1]
        user_id = max_db + 1
        DB_ID.append(user_id)
        return user_id
    
    def add_liked_beer(self, beer_name: str):
        """Add beer name to the set of liked beer"""
        self.liked.add(beer_name)
        
    def unlike_beer(self, beer_name: str):
        """Remove a beer from the liked list"""
        #if beer_name in self.liked:
        self.liked.discard(beer_name)
        
    def save_to_db(self):
        user_data = pd.DataFrame({
                'user_id': [self.id],
                'email' :[self.email],
                'name': [self.name],
                'age' : [self.age],
                'liked_beers' :[self.liked]
            })
        
        # Add user to dabatase if file exists otherwise creates it
        if os.path.isfile('assets/mock_db.csv'):
            database = pd.read_csv('assets/mock_db.csv')
            database = database.append(user_data)
            database.to_csv('assets/mock_db.csv', index=False)
            
        else:
            user_data.to_csv('assets/mock_db.csv', index=False)

# if __name__ == '__main__':
#     pass