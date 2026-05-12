from pydantic import BaseModel, Field
from typing import Annotated

class ChatRequest(BaseModel):
    message : str = Field(description="Message sent by the user")


