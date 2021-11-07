from zytholic_project.userspace import User, UnknownBeer
import pandas as pd
import os

stef = User('stef',
            'stef@choisirsabiere.fr',
            18)
alix = User('alix',
             'alix@choisirsabiere.fr',
             18)

def test_user_characteristics():
    assert stef.name == 'stef'
    assert isinstance(stef.email, str)
    assert isinstance(stef.age, int)
    assert isinstance(stef.id, int)
    assert isinstance(stef.liked, set)

def test_unique_userid():
    assert stef.id != alix.id
    assert stef.id < alix.id
    
def test_add_liked_beer():
    # Beer in the database
    stef.add_liked_beer("Amber")
    assert "Amber" in stef.liked
    
    # Beer not in the database
    try:
        stef.add_liked_beer("Pepoodo") 
    except UnknownBeer as err:
        assert str(err) == "Pepoodo is not in the database"
    
def test_unlike_beer():
    stef.unlike_beer("Amber")
    assert "Amber" not in stef.liked
    
def test_save_user_to_db():
    stef.save_to_db()
    database = pd.read_csv('assets/mock_db.csv')
    assert database.shape == (1, 5)
    assert database.name[0] == 'stef'
    
    alix.save_to_db()
    database = pd.read_csv('assets/mock_db.csv')
    assert database.shape == (2, 5)
    assert database.name.to_list() == ['stef', 'alix']
    
    # Cleaning mock DB after test
    os.remove('assets/mock_db.csv')
