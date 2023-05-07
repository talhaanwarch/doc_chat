from pydantic import BaseModel
from typing import Optional
class DocModel(BaseModel):
    api_key: str
    dir_path: str

class QueryModel(BaseModel):
    api_key: str
    text: str
    working_memory: Optional[list[str]] = None