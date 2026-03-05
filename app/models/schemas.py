from pydantic import BaseModel
from typing import List, Optional

class GenerateCodeRequest(BaseModel):
    user_query: str
    selected_modules: List[str]

class GenerateCodeResponse(BaseModel):
    connection: str
    micropython_code: str
    mixly_steps: str
