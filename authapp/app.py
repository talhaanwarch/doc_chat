from fastapi import Depends, FastAPI

from .db import User, create_db_and_tables
from .schemas import UserCreate, UserRead, UserUpdate, Query, Data
from .users import auth_backend, current_active_user, fastapi_users

app = FastAPI()

app.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["auth"]
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


import requests

def send_query(text, client_id):
    url = 'http://app:8000/query'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'text': text,
        'client_id': client_id
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        json_data = response.json()
        # Process the JSON response here
        return json_data
    else:
        print('Error:', response.status_code)


def ingest_data(urls, client_id):
    url = 'http://app:8000/doc_ingestion'
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    payload = {
        'urls': urls,
        'client_id': client_id
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 200:
        json_data = response.json()
        # Process the JSON response here
        return json_data
    else:
        print('Error:', response.status_code)


@app.post("/query")
async def query_route(query: Query, user: User = Depends(current_active_user) ):
    data = send_query(query.text, user.email)
    return data

@app.post("/ingest")
async def data_route(data: Data, user: User = Depends(current_active_user) ):
    data = ingest_data(data.urls, user.email)
    return data



@app.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    
    return {"message": f"Hello {user.email}!"}


@app.on_event("startup")
async def on_startup():
    # Not needed if you setup a migration system like Alembic
    await create_db_and_tables()

