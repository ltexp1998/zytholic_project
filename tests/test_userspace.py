from numpy.lib.arraysetops import isin
from zytholic_project.userspace import User

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
    stef.add_liked_beer("Westmalle")
    assert "Westmalle" in stef.liked
    
def test_unlike_beer():
    stef.unlike_beer("Westmalle")
    assert "Westmalle" not in stef.liked