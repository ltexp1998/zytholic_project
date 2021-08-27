from zytholic_project.apicall import check_name

def test_check_name():
    assert(check_name('Our Special Ale 2019 (Anchor Christmas Ale)') =='Our Special Ale 2019 (Anchor Christmas Ale)')
    assert(check_name('Gaffel Kölsch') == 'Gaffel Kölsch')
    assert(check_name('Donnybrook Stout') == 'Donnybrook Stout')
    assert(check_name('abcde') == 'Invalid Name')
    assert(check_name('Longist Trail Ale') == 'Invalid Name')
    assert(check_name('Gaffel Kolsch') == 'Invalid Name')
