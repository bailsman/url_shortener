def test_nonexistent_shortcode(client):
    resp = client.get('/123456')
    assert resp.status_code == 404

def test_nonexistent_shortcode_stats(client):
    resp = client.get('/123456/stats')
    assert resp.status_code == 404

def test_invalid_url(client):
    resp = client.post('/shorten', json={'url': 'http://examplecom'})
    assert resp.status_code != 201

def test_valid_url_missing_shortcode(client):
    resp = client.post('/shorten', json={'url': 'http://example.com'})
    assert resp.status_code == 201
