from API.api import app
import requests
from fastapi.testclient import TestClient

url_local = 'http://localhost:1234'
url_docker = 'http://0.0.0.0:5000'
url_gcp = 'https://api-zytholic-project-uq4l4l4m7a-ew.a.run.app'
url_O2 = 'http://thst7353.odns.fr/api/'

beer_name = "Amber"

client = TestClient(app)

def test_basic_name():
    call = f'{url_local}/name_beer?name={beer_name}'
    response = client.get(call)
    assert response.status_code == 200

def test_filter_abv_ibu():
    call = f'{url_local}/filter_abv_ibu?name={beer_name}&abv={8}&ibu={100}'
    response = client.get(call)
    assert response.status_code == 200
    
if __name__ == '__main__':
    test_basic_name()
    test_filter_abv_ibu()