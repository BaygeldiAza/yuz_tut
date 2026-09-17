from uuid6 import uuid6

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_register_user(client: AsyncClient) -> None:
    email = f"user-{uuid6().hex[:8]}@example.com"

    response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": "testuser",
            "password": "strongpassword123",
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["email"] == email
    assert data["username"] == "testuser"
    assert "id" in data
    assert data["is_active"] is True

    # Password must never be returned by the API.
    assert "password" not in data
    assert "password_hash" not in data


@pytest.mark.asyncio
async def test_register_duplicate_email(client: AsyncClient) -> None:
    email = f"duplicate-{uuid6().hex[:8]}@example.com"

    payload = {
        "email": email,
        "username": "duplicateuser",
        "password": "strongpassword123",
    }

    first_response = await client.post(
        "/auth/register",
        json=payload,
    )

    second_response = await client.post(
        "/auth/register",
        json={
            **payload,
            "username": "anotheruser",
        },
    )

    assert first_response.status_code == 201
    assert second_response.status_code == 409


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient) -> None:
    email = f"login-{uuid6().hex[:8]}@example.com"
    password = "strongpassword123"

    register_response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": "loginuser",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 202

    data = login_response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_with_wrong_password(client: AsyncClient) -> None:
    email = f"wrong-password-{uuid6().hex[:8]}@example.com"

    register_response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": "wrongpassworduser",
            "password": "correctpassword123",
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": "wrongpassword123",
        },
    )

    assert login_response.status_code == 401


@pytest.mark.asyncio
async def test_oauth2_token_endpoint(client: AsyncClient) -> None:
    email = f"token-{uuid6().hex[:8]}@example.com"
    password = "strongpassword123"

    register_response = await client.post(
        "/auth/register",
        json={
            "email": email,
            "username": "tokenuser",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    token_response = await client.post(
        "/auth/token",
        data={
            "username": email,
            "password": password,
        },
    )

    assert token_response.status_code == 200

    data = token_response.json()

    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"