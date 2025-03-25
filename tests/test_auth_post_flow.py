# tests/test_auth_post_flow.py

import pytest
import time
from httpx import AsyncClient
from asgi_lifespan import LifespanManager
from main import app

@pytest.mark.asyncio
async def test_signup_login_add_post():
    async with LifespanManager(app):
        async with AsyncClient(app=app, base_url="http://testserver") as ac:
            email = f"unit_test_{int(time.time())}@example.com"
            password = "secure123"

            # 1. Signup
            resp = await ac.post("/auth/signup", json={
                "email": email,
                "password": password
            })
            assert resp.status_code == 200, f"Signup failed: {resp.text}"
            token = resp.json()["access_token"]

            # 2. Login
            resp = await ac.post("/auth/login", json={
                "email": email,
                "password": password
            })
            assert resp.status_code == 200, f"Login failed: {resp.text}"
            token = resp.json()["access_token"]

            # 3. Add Post
            headers = {"Authorization": f"Bearer {token}"}
            resp = await ac.post("/post/add", json={"text": "unit test post"}, headers=headers)
            assert resp.status_code == 200, f"Add post failed: {resp.text}"
            assert "postID" in resp.json()
