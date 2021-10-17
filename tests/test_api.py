from API.api import app
from fastapi.testclient import TestClient

beer_name = "Amber"

client = TestClient(app)

def test_basic_name():
    call = f'/name_beer?name={beer_name}'
    response = client.get(call)
    assert response.status_code == 200

def test_filter_abv_ibu():
    call = f'/filter_abv_ibu?name={beer_name}&abv={8}&ibu={100}'
    response = client.get(call)
    assert response.status_code == 200
    
if __name__ == '__main__':
    print(test_basic_name())
    print(test_filter_abv_ibu())