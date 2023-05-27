from pydantic import BaseModel, validator
from typing import Optional
import os
import re

def validate_uuid(uuid_string):
    pattern = re.compile(
        r'^[0-9a-fA-F]{8}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{4}-'
        r'[0-9a-fA-F]{12}$'
    )
    return re.match(pattern, uuid_string)


class DocModel(BaseModel):
    dir_path: str
    collection_name: Optional[str] = 'LangChainCollection'

    @validator('dir_path')
    def validate_dir_path(cls, dir_path):
        if not os.path.exists(dir_path):
            raise ValueError('Directory path must start with a forward slash')
        return dir_path


class QueryModel(BaseModel):
    text: str
    session_id: str
    collection_name: Optional[str] = 'LangChainCollection'

    @validator('text')
    def validate_text(cls, text):
        if not text:
            raise ValueError('Text must be provided')
        return text

    @validator('session_id')
    def validate_session_id(cls, session_id):
        if not validate_uuid(session_id):
            raise ValueError('Session ID must be in uuid4 format')
        return session_id


class DeleteSession(BaseModel):
    session_id: str

    @validator('session_id')
    def validate_session_id(cls, session_id):
        if not validate_uuid(session_id):
            raise ValueError('Session ID must be in uuid4 format')
        return session_id
