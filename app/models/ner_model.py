from pydantic import BaseModel
from typing import List

class NERRequest(BaseModel):
    text: str

class NERResponse(BaseModel):
    drugs: List[str]
    diseases: List[str]
    allergies: List[str]
