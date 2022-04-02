def test_index_page_valid(test_client):
    """
    GIVEN a Flask application is running
    WHEN the '/' home page is requested (HTTP GET request)
    THEN a success response code (200) is received (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200)
    """
    response = test_client.get('/')
    assert response.status_code == 200
