from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message : str = Field(description="Message sent by the user")
    session_id : str = Field(description="Session Id for each individual chat and holds all the message for that converstaion")


class ChatResponse(BaseModel):
    answer : str = Field(description="Answer responsed by the AI model")