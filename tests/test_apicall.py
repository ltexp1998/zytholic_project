from zytholic_project.apicall import check_name, get_most_similar_beers

def test_check_name():
    assert(check_name('Our Special Ale 2019 (Anchor Christmas Ale)') =='Our Special Ale 2019 (Anchor Christmas Ale)')
    assert(check_name('Gaffel Kölsch') == 'Gaffel Kölsch')
    assert(check_name('Donnybrook Stout') == 'Donnybrook Stout')
    assert(check_name('abcde') == 'Invalid Name')
    assert(check_name('Longist Trail Ale') == 'Invalid Name')
    assert(check_name('Gaffel Kolsch') == 'Invalid Name')
    

def test_get_most_similar_beers():
    assert get_most_similar_beers('Gaffel Kölsch', n_beers=5).shape\
            == (5, 4)
    assert get_most_similar_beers('Donnybrook Stout', n_beers=8).shape\
            == (8, 4)
    assert get_most_similar_beers('Donnybaearrook Stout') == None