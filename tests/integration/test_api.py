def test_read_main(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"CAREER OS" in response.content

def test_register_and_login(client, db):
    # Register
    response = client.post("/auth/register", data={"email": "test@example.com", "password": "password123", "full_name": "Test User"})
    assert response.status_code == 200 # Redirects, but testclient follows redirects by default usually, actually wait 302 or 200 depends on client setup
    
    # Login
    response = client.post("/auth/login", data={"email": "test@example.com", "password": "password123"})
    # Should get a cookie and redirect
    assert "access_token" in response.cookies or response.history
