from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message : str = Field(description="Message sent by the user")


class ChatResponse(BaseModel):
    answer : str = Field(description="Answer responsed by the AI model")