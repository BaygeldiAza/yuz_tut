from uuid6 import uuid6

import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_search_history(client: AsyncClient) -> None:
    email = f"history-{uuid6().hex[:8]}@example.com"
    password = "strongpassword123"

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": "historyuser",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 202

    token = login_response.json()["access_token"]

    response = await client.get(
        "/api/v1/search-history",
        headers={
            "Authorization": f"Bearer {token}",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.asyncio
async def test_get_search_history_requires_authentication(
    client: AsyncClient,
) -> None:
    response = await client.get(
        "/api/v1/search-history",
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_search_history_user_isolation(
    client: AsyncClient,
) -> None:
    user_a_email = f"user-a-{uuid6().hex[:8]}@example.com"
    user_b_email = f"user-b-{uuid6().hex[:8]}@example.com"
    password = "strongpassword123"

    user_a_register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user_a_email,
            "username": "usera",
            "password": password,
        },
    )

    user_b_register = await client.post(
        "/api/v1/auth/register",
        json={
            "email": user_b_email,
            "username": "userb",
            "password": password,
        },
    )

    assert user_a_register.status_code == 201
    assert user_b_register.status_code == 201

    user_a_login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user_a_email,
            "password": password,
        },
    )

    user_b_login = await client.post(
        "/api/v1/auth/login",
        json={
            "email": user_b_email,
            "password": password,
        },
    )

    assert user_a_login.status_code == 202
    assert user_b_login.status_code == 202

    user_a_token = user_a_login.json()["access_token"]
    user_b_token = user_b_login.json()["access_token"]

    user_a_history = await client.get(
        "/api/v1/search-history",
        headers={
            "Authorization": f"Bearer {user_a_token}",
        },
    )

    user_b_history = await client.get(
        "/api/v1/search-history",
        headers={
            "Authorization": f"Bearer {user_b_token}",
        },
    )

    assert user_a_history.status_code == 200
    assert user_b_history.status_code == 200

    assert user_a_history.json() == []
    assert user_b_history.json() == []


@pytest.mark.asyncio
async def test_hide_search_history(
    client: AsyncClient,
) -> None:
    email = f"hide-{uuid6().hex[:8]}@example.com"
    password = "strongpassword123"

    register_response = await client.post(
        "/api/v1/auth/register",
        json={
            "email": email,
            "username": "hideuser",
            "password": password,
        },
    )

    assert register_response.status_code == 201

    login_response = await client.post(
        "/api/v1/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    assert login_response.status_code == 202

    token = login_response.json()["access_token"]