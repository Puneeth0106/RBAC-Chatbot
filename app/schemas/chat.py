from pydantic import BaseModel, Field , StringConstraints
from typing import Annotated

class ChatRequest(BaseModel):
    message : Annotated[str,Field(description="Message sent by the user") , StringConstraints(strip_whitespace= True, min_length=1, max_length=2000)]
    session_id :Annotated[str,Field(description="Session Id for each individual chat and holds all the message for that converstaion", min_length=1, max_length=100)]

class SuggestionRequest(BaseModel):
    question: Annotated[str, Field(description="Question asked by the user", min_length= 1)]
    answer: Annotated[str, Field(description="Answer by the chatbot", min_length= 1)]

class SuggestionResponse(BaseModel):
    suggestions: list[str]